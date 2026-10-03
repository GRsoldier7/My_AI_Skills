# Project Router: ChatGPT and Codex

## Architecture

One canonical source: `skills/aarons-latest/` in `GRsoldier7/My_AI_Skills`.
One private, skills-only plugin: **Project Router | by AARON**.
Seven workflows: the router plus builder, rescope, continuity, execution,
project cleanup, and directory organization. Required references travel with
them. No new server, credentials, external connection, paid service, permission
change, or recurring background process is required.

`plugin.json` here is a build manifest, not an already installed plugin.
`python scripts/project-router.py build` packages the canonical SKILL.md files,
references, and OpenAI skill metadata into a self-contained, deterministic ZIP.
The ZIP records SHA-256 hashes in SOURCES.json. Generated copies are not committed
as a second source of truth. Tests/evals are retained in source, not loaded as
runtime workflow instructions.

## Account-scoped ChatGPT access

Save the generated ZIP as a private plugin using Plugin Creator. Open the saved
plugin in the same account, install it if prompted, then start a new chat and
select **Project Router | by AARON** with the plugin picker or @ mention.

Use:

```text
Use project-router in assess mode for this project.
Determine the next justified workflow from current evidence. Do not change files.
```

Or authorize a bounded slice:

```text
Use project-router in continue mode for the next ready task in the approved plan.
Preserve scope and unrelated work. Stop at a verified task boundary or missing approval.
```

Account storage is not a claim that every client supports the plugin or that
local files become accessible from web/mobile. Availability, installation, and
sync can differ between ChatGPT and Codex. Reuse the saved account plugin where
supported. Do not install duplicate raw skills on a client already loading the
same plugin skills. Tool access remains subject to each host's connections and
permissions. A skill cannot turn a phone into a local repository runner.

## Local Codex: all projects for one OS user

For a client that does not load the account plugin, use a complete checkout of
this repository and Python 3.10 or newer. Run from the repository root:

```sh
# Preview; writes nothing.
python3 scripts/project-router.py install --global-guidance

# Install the seven skills and scoped user-wide routing guidance.
python3 scripts/project-router.py install --apply --global-guidance
```

On Windows, use `python` or `py -3` in place of `python3` as appropriate.
The destination is `~/.agents/skills/`. Optional guidance is appended to
`~/.codex/AGENTS.md`, or the existing `AGENTS.override.md` when present. Existing
instruction bytes are preserved. This only scopes project lifecycle selection;
it does not replace unrelated preferences or change Codex permissions.

The installer preflights every target, rejects symlink redirection, skips matching
skills, preserves extra existing files, and refuses differing skills or modified
managed guidance before installation. It does not silently overwrite, delete,
or replace local customizations. Review and back up any reported conflicting
skill before choosing whether to replace it. Run only one installer at a time.
If an I/O failure interrupts installation, inspect the reported paths and rerun;
already matching completed skills are skipped.

With a custom CODEX_HOME, omit --global-guidance and merge the small GUIDANCE
block from the script into the active global instruction file yourself. Skill
installation still targets the documented user skill directory.

Restart Codex, then test:

```text
$project-router assess
Identify the next appropriate workflow. Do not modify files.
```

Repeat the local setup on each independent computer/OS user or cloud environment
that does not inherit the account plugin. This repository and the account plugin
do not remotely modify device home directories. No device installation is claimed
until that device has run the setup and exposed the skill in its selector.

## Maintenance

Edit only the canonical sources. After reviewing updates, run:

```sh
python3 scripts/test-project-router.py
python3 scripts/project-router.py build --output ../project-router-plugin.zip
```

The builder refuses to overwrite a different existing ZIP; use a fresh versioned
output name for a changed release. Bump this plugin manifest's semantic version
before publishing changed bundled content. Ask Plugin Creator to update the
existing **Project Router | by AARON**, preserving its identity and private audience.
Do not create a second plugin for routine updates. GitHub commits do not by
themselves update an uploaded private plugin; no automatic GitHub/account sync is
configured by this integration.

For local installations, pull approved repository changes with `git pull --ff-only`,
preview the installer, and reconcile reported differences before reinstalling.
Do not reset or discard uncommitted work. The full library's existing generated
master registry can be refreshed with its existing generator from a complete
checkout; this integration's scoped entrypoint is AGENTS.md and the seven-skill
index, not a manually edited generated block.

## Verification boundaries

Distribution tests cover seven-skill inclusion, ZIP integrity, read-only preview,
repeat-run idempotence, collision handling, instruction preservation, symlink
rejection, conflicting guidance, and missing sources. The 24 routing scenarios
in `skills/aarons-latest/project-router/tests/acceptance.md` still require runs
inside real target hosts. Packaging tests are not proof of agent adherence,
mobile support, successful deployments, or universal reliability.

## Official documentation checked 2026-10-03

- OpenAI plugin packages: https://developers.openai.com/plugins/build/plugins
- Codex skill locations and discovery: https://developers.openai.com/codex/skills
- Plugins in ChatGPT: https://help.openai.com/en/articles/20001256-plugins-in-chatgpt
- Skills and surface differences: https://help.openai.com/en/articles/20001066-skills-in-chatgpt
