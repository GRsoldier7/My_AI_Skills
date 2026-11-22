# PowerShell for Windows analytics operations

Confirm Windows PowerShell 5.1 or PowerShell 7, the available modules and the approved path. For an inventory, return objects with predictable fields. Use literal paths for supplied file names, `-ErrorAction Stop` when errors must enter a catch block, and explicit encodings for text interchange. Distinguish an empty result from an access failure.

```powershell
function Get-ReportInventory {
    [CmdletBinding()]
    param([Parameter(Mandatory)][string] $Folder)
    Get-ChildItem -LiteralPath $Folder -File -ErrorAction Stop |
        Where-Object { $_.Extension -eq '.csv' } |
        Sort-Object Name |
        Select-Object Name, Length
}
```

Try an empty fixture directory, a directory with two CSVs plus one unrelated file, and a directory name containing square brackets. Expect 0, 2 and normal literal-path results. A missing folder should produce an error. Do not present a blank report as successful discovery.

For a mutating function, separate enumeration and selection from writing, expose `SupportsShouldProcess`, and call `$PSCmdlet.ShouldProcess(...)` at the actual side effect. Verify `-WhatIf`, an existing target, partial failure and a second execution on disposable files. Never include secrets or full work records in transcript examples. Pester and PSScriptAnalyzer can supplement checks on an approved workstation. [Microsoft PSScriptAnalyzer](https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/overview)
