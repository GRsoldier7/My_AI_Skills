#!/usr/bin/env python3
"""Behavioral checks for staging, provenance and platform boundaries."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location('delivery',Path(__file__).with_name('library-delivery.py'))
delivery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(delivery)


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'repo'
        self.root.mkdir()
        self.manifest = {'schema_version':1,'skills':[],'profiles':{'demo':{'skills':[],'includes':[],'allow_trial':True}}}
        self.config = {'catalog_path':'docs/20261029 - Test - Catalog.md','bundles':{'demo':{'platforms':['chatgpt','copilot','hermes','codex'],'title':'Demo','description':'Synthetic delivery','prompt':'Use the selected skill.'}},'skills':{}}
        self.artifacts = {'schema_version':1,'artifacts':[]}
        self.add_skill('sample')
        self.save()

    def put(self,path,text):
        target = self.root / path
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(text)
        return target

    def add_skill(self,name,category='core',body='Use synthetic data.'):
        path = f'skills/{category}/{name}'
        self.put(path+'/SKILL.md',f'---\nname: {name}\ndescription: Synthetic skill.\n---\n# {name}\n\n{body}\n')
        self.put(path+'/LICENSE','Synthetic license fixture.\n')
        entry = {'id':name,'name':name,'path':path,'status':'trial','dependencies':[],'provenance':{'kind':'owner-authored'},'package_sha256':delivery.sets.package_hash(self.root/path)}
        self.manifest['skills'].append(entry)
        self.manifest['profiles']['demo']['skills'].append(name)
        return entry

    def save(self):
        self.put('platform-configs/skill-sets/manifest.json',json.dumps(self.manifest))
        self.put('platform-configs/library-delivery.json',json.dumps(self.config))
        self.put('platform-configs/artifact-sources.json',json.dumps(self.artifacts))
        (self.root/'docs').mkdir(exist_ok=True)

    def export(self,platform='copilot',name='out'):
        return delivery.export(self.root,'demo',platform,self.base/name)

    def artifact(self,path,text):
        self.put(path,text)
        self.artifacts['artifacts'].append({'path':path,'sha256':delivery.sha(text.encode()),'type':'adapter'})

    def test_export_is_deterministic_and_receipted(self):
        first = self.export(name='one')
        second = self.export(name='two')
        self.assertEqual(Path(first['archive']).read_bytes(),Path(second['archive']).read_bytes())
        output = Path(first['output'])
        receipt = json.loads((output/'SOURCES.json').read_text())
        for path,digest in receipt['files'].items():
            self.assertEqual(delivery.sha((output/path).read_bytes()),digest)
        self.assertIn('Library delivery boundaries',(output/'.github/skills/sample/SKILL.md').read_text())

    def test_existing_output_is_preserved(self):
        self.export()
        with self.assertRaisesRegex(ValueError,'already exists'): self.export()

    def test_existing_archive_is_preserved(self):
        (self.base/'out.zip').write_text('keep')
        with self.assertRaisesRegex(ValueError,'already exists'): self.export()
        self.assertEqual((self.base/'out.zip').read_text(),'keep')

    def test_modified_package_is_rejected(self):
        self.put('skills/core/sample/LICENSE','changed')
        with self.assertRaisesRegex(ValueError,'Package changed'): self.export()

    def test_package_symlink_is_rejected(self):
        (self.root/'skills/core/sample/link').symlink_to('/etc/passwd')
        with self.assertRaisesRegex(ValueError,'Symlink'): self.export()

    def test_output_symlink_parent_is_rejected(self):
        (self.base/'alias').symlink_to(self.base,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'symlink'): self.export(name='alias/out')

    def test_tracked_tree_output_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'Stage outside'): self.export(name='repo/generated')

    def test_unsupported_platform_is_rejected(self):
        self.config['bundles']['demo']['platforms']=['copilot']; self.save()
        with self.assertRaisesRegex(ValueError,'not available'): self.export('chatgpt')

    def test_blocked_skill_is_rejected(self):
        self.config['skills']['sample']={'copilot':{'mode':'blocked','reason':'MCP required'}}; self.save()
        with self.assertRaisesRegex(ValueError,'MCP required'): self.export()

    def test_cross_category_links_are_relocated(self):
        second = self.add_skill('second','design','See [sample](../../core/sample/SKILL.md).')
        second['dependencies']=['sample']; self.save()
        out=Path(self.export()['output'])
        self.assertIn('](../sample/SKILL.md)',(out/'.github/skills/second/SKILL.md').read_text())

    def test_instruction_override_excludes_runtime(self):
        self.put('skills/core/sample/scripts/run.py','raise RuntimeError("Never execute me")\n')
        self.manifest['skills'][0]['package_sha256']=delivery.sets.package_hash(self.root/'skills/core/sample')
        path='platform-configs/adapters/sample/chatgpt.md'
        self.artifact(path,'---\nname: sample\ndescription: Portable.\n---\nUse supplied evidence only.\n')
        self.config['skills']['sample']={'chatgpt':{'mode':'instructions','override':path}}; self.save()
        out=Path(self.export('chatgpt')['output'])
        self.assertFalse((out/'skills/sample/scripts').exists())
        self.assertTrue((out/'skills/sample/LICENSE').exists())
        self.assertIn('Instruction-only',(out/'skills/sample/SKILL.md').read_text())
        self.assertIn('com.openai',json.loads((out/'plugin.json').read_text())['extensions'])

    def test_unregistered_override_is_rejected(self):
        path='platform-configs/adapters/sample/chatgpt.md'; self.put(path,'manual guidance')
        self.config['skills']['sample']={'chatgpt':{'mode':'instructions','override':path}}; self.save()
        with self.assertRaisesRegex(ValueError,'Unregistered'): self.export('chatgpt')

    def test_missing_override_is_rejected(self):
        self.config['skills']['sample']={'chatgpt':{'mode':'instructions'}}; self.save()
        with self.assertRaisesRegex(ValueError,'needs an override'): self.export('chatgpt')

    def test_provider_variant_requires_own_hash(self):
        self.put('platform-configs/variants/sample/SKILL.md','---\nname: sample\n---\nVariant.\n')
        self.config['skills']['sample']={'codex':{'mode':'full','source':'platform-configs/variants/sample'}}; self.save()
        with self.assertRaisesRegex(ValueError,'Unverified provider'): self.export('codex')

    def test_agent_mcp_tools_are_rejected(self):
        self.artifact('agents/demo.md','---\nname: demo\n---\nReview.\n')
        self.config['bundles']['demo']['agents']=[{'path':'agents/demo.md','name':'demo','description':'Review','tools':['mcp/anything']}]; self.save()
        with self.assertRaisesRegex(ValueError,'Unapproved'): self.export()

    def test_agent_export_is_named_and_readonly(self):
        self.artifact('agents/demo.md','---\nname: upstream\n---\nReview.\n')
        self.config['bundles']['demo']['agents']=[{'path':'agents/demo.md','name':'demo-reviewer','description':'Review'}]; self.save()
        out=Path(self.export()['output'])
        text=(out/'.github/agents/demo-reviewer.agent.md').read_text()
        self.assertIn('name: demo-reviewer',text)
        self.assertIn('tools: ["read", "search"]',text)

    def test_catalog_drift_detection(self):
        with self.assertRaisesRegex(ValueError,'stale'): delivery.catalog(self.root)
        path=delivery.catalog(self.root,True)
        self.assertEqual(path,delivery.catalog(self.root))
        self.assertTrue(Path(path).read_text().startswith('# 20261029 - Test - Catalog\n'))


if __name__=='__main__': unittest.main()
