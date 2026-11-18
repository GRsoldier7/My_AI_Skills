#!/usr/bin/env python3
"""Interpret immutable scan evidence with exact, repository-owned review records."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def tree_hash(package):
    """Bind decisions to all regular input bytes, not only a matched line."""
    records = []
    for path in sorted(package.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symlink in scanner input')
        if path.is_file():
            records.append([path.relative_to(package).as_posix(), digest(path.read_bytes())])
    return digest(json.dumps(records, separators=(',', ':')).encode())


def fingerprint(issue):
    # No semantic guessing or blanket rule suppression. Match the actual evidence.
    evidence = {key: issue.get(key) for key in
                ['id', 'severity', 'location', 'finding', 'code_snippet']}
    return digest(json.dumps(evidence, sort_keys=True, separators=(',', ':')).encode())


def load_reviews():
    return json.loads((HERE / 'reviewed-findings.json').read_text())['exceptions']


def decide(report, package, package_key, scanned_tree, scanner_exit, reviews):
    """Return policy separately; never mutate the source report or run candidate code."""
    current_tree = tree_hash(package)
    result = {'decision': 'REVIEW', 'input_sha256': current_tree,
              'raw_scanner_exit': scanner_exit, 'policy_version': 1,
              'review_registry_sha256': digest(json.dumps(reviews, sort_keys=True).encode()),
              'reviewed_findings': [],
              'unresolved_findings': [], 'reasons': [], 'automatic_install': False}
    if not isinstance(report, dict):
        result.update(decision='ERROR', reasons=['Malformed scan report'])
        return result
    issues = report.get('issues')
    metadata = report.get('metadata', {})
    coverage = report.get('analysis_completeness', {})
    if not isinstance(issues, list) or not isinstance(metadata, dict) or not isinstance(coverage, dict):
        result.update(decision='ERROR', reasons=['Malformed scan report'])
        return result
    if scanner_exit not in (0, 1) or report.get('execution_successful') is False:
        result.update(decision='ERROR', reasons=['Scanner execution failed'])
        return result
    if metadata.get('llm_requested') is not False or metadata.get('inference_usage', []) != []:
        result.update(decision='ERROR', reasons=['Unexpected scan mode or inference usage'])
        return result
    if not scanned_tree or scanned_tree != current_tree:
        result['reasons'].append('Input changed or report is not bound to this source snapshot')
    complete = (coverage.get('is_complete') is True and report.get('execution_successful') is True)
    if not complete:
        result['reasons'].append('Scan coverage or successful completion is unverified')
    for index, issue in enumerate(issues):
        if not isinstance(issue, dict) or issue.get('severity') not in ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', 'INFO'):
            result.update(decision='ERROR', reasons=['Malformed finding or unknown severity'])
            return result
        location = issue.get('location', {})
        name = location.get('file') if isinstance(location, dict) else None
        path = package / name if isinstance(name, str) else package
        # Only relative in-package files can receive a reviewed disposition.
        file_hash = None
        if isinstance(name, str) and not Path(name).is_absolute() and path.resolve().is_relative_to(package.resolve()) and path.is_file():
            file_hash = digest(path.read_bytes())
        match = next((entry for entry in reviews
                      if entry.get('package') == package_key
                      and entry.get('tree_sha256') == current_tree == scanned_tree
                      and entry.get('file') == name and file_hash is not None
                      and entry.get('file_sha256') == file_hash
                      and entry.get('rule') == issue.get('id')
                      and entry.get('finding_sha256') == fingerprint(issue)
                      and entry.get('disposition') == 'false_positive'
                      and entry.get('rationale') and entry.get('reviewed_by')), None)
        detail = {'index': index, 'rule': issue.get('id'), 'file': name,
                  'severity': issue['severity'], 'finding_sha256': fingerprint(issue)}
        if match:
            detail.update(review_id=match['review_id'], rationale=match['rationale'])
            result['reviewed_findings'].append(detail)
        else:
            result['unresolved_findings'].append(detail)
    if any(i['severity'] in ('HIGH', 'CRITICAL') for i in result['unresolved_findings']):
        result['decision'] = 'BLOCK'
        result['reasons'].append('Unresolved high or critical finding requires source review and explicit disposition')
    elif result['unresolved_findings']:
        result['reasons'].append('Unresolved findings require review; score alone is not an install decision')
    elif result['reasons']:
        pass
    elif scanner_exit == 1 and not issues:
        result['reasons'].append('Unexplained nonzero scanner exit')
    else:
        result['decision'] = 'ALLOW'
        result['reasons'].append('Complete enabled static coverage; no unresolved findings')
    return result
