# Release a Power Platform solution

Use this contract to move a canvas app and its solution-aware flows from development through QA to production. The maker supplies an export from an actual Dataverse environment. Work ChatGPT can prepare the component inventory, redacted settings worksheet, operator commands and acceptance record. A user or an approved runner with target access performs and signs the export, imports and runtime tests. A ZIP assembled from instructions or example JSON is insufficient release evidence.

## 1. Freeze the source in development

1. In Power Apps or Power Automate, select the named **development** environment and open **Solutions**. Use a custom **unmanaged** solution with the intended publisher and unique name. Record the source tenant/environment ID and Dataverse URL, publisher prefix, unique name and four-part version. Increment the version above the deployed baseline.
2. Include the published canvas app, every flow it calls, parents and children, connection references, environment variable definitions, tables, choices, custom connectors and other directly required components. Inspect **Show dependencies**. Record imported prerequisite solutions and minimum versions when they are delivered separately. Create parent and child flows together in the solution. Configure supported embedded connections for child flows. Check the app's flow trigger parameters/return contract and actual data source bindings. [Child flows](https://learn.microsoft.com/en-us/power-automate/create-child-flows) · [Connection references](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-connection-reference)
3. Save and publish the intended app version, save the flow changes, and publish solution customizations with the responsible maker's approval. Run Solution checker and resolve blocking findings. Remove development-specific current values from the export where appropriate. Record intentional defaults, required overrides, source commit or source artifact, and published revision. Keep the editable source in development. [Export a solution](https://learn.microsoft.com/en-us/power-automate/export-flow-solution)
4. In **Solutions → Export**, choose the approved version and **Managed**. Save the ZIP once in a restricted release directory. Record the file's SHA-256. A standalone flow package, app package or `.msapp` cannot substitute. QA and production receive identical ZIP bytes. [Managed solution lifecycle](https://learn.microsoft.com/en-us/power-platform/alm/basics-alm)

The equivalent PAC command below assumes an already approved identity, a verified development environment URL in `$DevUrl`, and a new, writable local release directory. Use the actual unique name and version in place of the example. Set the version in development before export. Run each command from that directory. A failed native process must halt the release.

```powershell
$Name = 'WorkRequests'
$Version = '1.2.0.0'
$Zip = ".\${Name}_${Version}_managed.zip"
$Template = '.\pac-template.json'
pac solution export --environment $DevUrl --name $Name --path $Zip --managed
if ($LASTEXITCODE -ne 0) { throw 'Managed export failed' }
pac solution create-settings --solution-zip $Zip --settings-file $Template
if ($LASTEXITCODE -ne 0) { throw 'Template generation failed' }
Get-FileHash -Algorithm SHA256 -LiteralPath $Zip,$Template
```

Generate the template in a fresh directory **from this exact ZIP**. Keep that original PAC template and its hash paired with the ZIP hash in a protected release record. PAC deployment-settings JSON does not carry the source ZIP hash. Pin the PAC version for repeatable generation. If the export changes, generate a new template and repeat QA. [PAC solution commands](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/solution) · [Deployment settings format](https://learn.microsoft.com/en-us/power-platform/alm/conn-ref-env-variables-build-tools)

## 2. Bind each target deliberately

Make separate copies of the generated template for QA and production. Do not promote QA's populated settings file into production. For each target, the owner checks the following items in the approved environment and signs its settings file hash **after** reviewing the actual values.

| Inventory item | Decision and evidence |
|---|---|
| Target | Confirm tenant ID, environment ID/URL, intended installation or upgrade, baseline version, owner and approved change window against the change record. |
| Connection reference | Match the template's `LogicalName` and `ConnectorId`. Populate `ConnectionId` from the target's Connections UI. Verify the identity, ownership/sharing, connector, permissions, licenses and any gateway for the importing identity and actual flow owner. A structurally valid connection ID can still belong to the wrong environment. |
| Environment variable | Match `SchemaName` and set the target's intended `Value`. Preserve PAC-generated metadata and data-source relationships. Confirm current/default precedence in the target. For secrets use the supported vault reference and authorized target identity. Keep secret material out of prompts, release logs and version control. |
| SharePoint data | Preprovision the target site/list, internal column names and types, required fields, choices, lookup relationships, indexes and permissions. Verify the schema with the app and flow identities. For a canvas SharePoint data source map the site and list data-source variables to the target site and the target list GUID. Provision content and seed/reference data separately when needed. [SharePoint data-source variables](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables-data-source-canvas-apps) |
| Policy and access | Check the target DLP policy and connector combinations, premium licensing/entitlements, solution import privileges, connection sharing, flow/run-only access, app sharing, Dataverse roles and downstream data permissions. Record who owns flow activation, support and recovery. |

The optional [offline checker](../scripts/check-solution.py) uses Python 3 and the standard library. Its strict path covers **explicit bindings**. Every schema/logical name listed by PAC must have one populated target row, connector IDs must match and common unresolved tokens block the check. Zero and false are valid values. Keep generated extension fields for PAC. The checker does not interpret extension-specific settings, validate Dataverse types or resolve tenant data. If a release intentionally inherits an optional/default/current value, uses managed secret resolution without an explicit value, or delegates binding to the import wizard, record the schema name, method, expected effective result and accountable reviewer. Verify the effective binding in QA and production. Mark the release **manual binding review** where the strict check cannot apply. Never add a dummy value to obtain a pass. [Environment variable types and defaults](https://learn.microsoft.com/en-us/power-automate/environment-variables)

Run this in the restricted deployment workspace. Point `$Checker` to the packaged script. For app/flow releases, capture expected canvas app schema names and cloud workflow GUIDs from the approved source inventory, including each parent and child. Set `$AppSchema`, `$ParentWorkflowId` and `$ChildWorkflowId` from that inventory. Repeat the corresponding switches for additional components. Omit a switch only for a component type outside the release. `$TargetSettings` names the intended target file. Read `$ApprovedTargetSettingsSha` from that target owner's review record, not by hashing the input on the verification run.

```powershell
$CheckArgs = @('--solution', $Zip, '--name', $Name, '--version', $Version,
               '--template', $Template, '--settings', $TargetSettings,
               '--settings-sha256', $ApprovedTargetSettingsSha,
               '--canvas-app', $AppSchema, '--cloud-flow', $ParentWorkflowId,
               '--cloud-flow', $ChildWorkflowId)
python $Checker @CheckArgs
if ($LASTEXITCODE -ne 0) { throw 'Stop and resolve preflight findings' }
```

Exit 0 records the inspected name, version, entry counts and file fingerprints. Exit 1 identifies a file or mapping issue. Exit 2 indicates an invalid command line. For requested components it checks root component type 300 plus a nonempty matching canvas app member, and type 29 plus a matching modern workflow JSON with triggers and actions. These checks establish presence only. The checker reads the manifest and requested workflow JSON, each up to 8 MiB. For another package layout, document the manual component review and demonstrate the runtime calls. This local check cannot establish template origin or approve actual connection targets, imported components or runtime behavior. QA records the tested ZIP and paired original template hashes **after** both acceptance paths pass. Production verifies those hashes together with the independently approved production settings hash:

```powershell
python $Checker @CheckArgs --sha256 $QaSignedZipSha --template-sha256 $QaSignedTemplateSha
if ($LASTEXITCODE -ne 0) { throw 'Stop promotion and reconcile release records' }
```

Rebuild `$CheckArgs` for each target, with that target's independently approved settings digest. For a maker-only release, use **Get-FileHash** or the organization's approved checksum tool, retain the archive and paired template if available, review each effective binding in the maker portal with a second operator, and record the manual checks performed.

## 3. Import and prove both QA paths

| Target condition | Operator action |
|---|---|
| Clean QA install | Start with a disposable, authorized Dataverse environment with documented platform prerequisites and target data sources, without this solution. In **Solutions → Import**, upload the managed ZIP, inspect dependencies, bind the intended connections and variables, then import. PAC equivalent appears below. |
| Upgrade from N−1 | In a separate QA sandbox or restored representative copy, install the current production baseline, seed representative records and settings, and capture counts/relationships. Import the candidate with the production-intended upgrade mode. Check removed components, retained/configured bindings, data, dependencies and migration outcomes. If removals are intended, test an actual upgrade. An update retains obsolete components. A first-ever release records that no prior baseline exists. |
| Production | Require both QA results or a documented first-release exception, approved target values, change authorization and a recovery point. Match the signed ZIP/template hashes. Confirm the actual target URL, tenant, installed baseline and upgrade mode immediately before import. Use the same managed ZIP and the production settings. |

The examples below are **alternative operations**. Run only the one approved for this target. Set `$TargetUrl` to its verified explicit Dataverse URL. Check `$LASTEXITCODE` immediately after the selected command, then inspect solution history and the import job result in the target. A timeout requires checking the existing job before retrying. [Import solutions](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/import-update-export-solutions/) · [Update and upgrade behavior](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/update-solutions)

**Clean install**

```powershell
pac solution import --environment $TargetUrl --path $Zip --settings-file $TargetSettings --async
if ($LASTEXITCODE -ne 0) { throw 'Inspect the import job in the intended target' }
```

**Approved upgrade of an existing installation** (can delete removed components)

```powershell
pac solution import --environment $TargetUrl --path $Zip --settings-file $TargetSettings --async --stage-and-upgrade
if ($LASTEXITCODE -ne 0) { throw 'Inspect the upgrade job before any further action' }
```

In the wizard select the corresponding update/upgrade action for the installed baseline. Investigate dependency or unmanaged-layer conflicts at the source. Keep dependency and overwrite protections enabled. Where Microsoft suppresses a wizard prompt because a target/solution already supplies a value, inspect the effective target value after import.

## 4. Accept, recover and hand over

- Record the imported unique name, version, managed state, job ID, warnings, timestamp, environment, owner and tested artifact hash. Check app sharing, app-to-flow binding, first-run consent, run-only identity and child then parent flow activation. Open the published app as a realistic first-time user with minimum access. Complete the critical app transaction through the parent and child and verify the write in the intended target and the response back in the app. Also test that an unauthorized role is denied.
- Exercise an invalid input and a controlled connector failure in QA. Check error feedback, redacted diagnostics, correlation/run IDs and alert delivery. Replay with the same business key and verify that retries avoid duplicate records, approvals or notifications. Confirm upgrade data and existing users' effective permissions survive.
- Test the primary task using keyboard only, a screen reader with meaningful labels and announcement of errors, and high zoom on the target display. Record task outcome, defect severity, tester and date. Capture sanitized run evidence and the release decision. Label unexecuted cases **pending tenant verification**.
- Before production, assign a recovery owner, stop criteria, backup/restore point and a separate SharePoint/external-data recovery plan. During an incident pause triggers/intake with authorization, retain run IDs, identify any downstream side effects and reconcile queued/replayed items. Prefer a corrected higher-version managed build through QA when time permits. If full environment restore is necessary, an authorized admin uses the supported environment-type restore procedure and coordinates downtime, intervening writes, external data and revalidation. A managed uninstall can remove components/data. A lower-version import is not a rollback plan. Make fixes in development and repeat promotion. [Backup and restore](https://learn.microsoft.com/en-us/power-platform/admin/backup-restore-environments)
- Close the record with QA/install and QA/upgrade verdicts, signed file hashes, production smoke-test outcome, support owner and rollback decision. A plan or offline pass alone leaves the import and acceptance verdict pending.
