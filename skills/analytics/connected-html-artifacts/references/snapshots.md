# Excel and CSV snapshots

For CSV, parse quoted delimiters/newlines and escaped quotes; validate a header,
consistent row width, required columns and field types. Use file input, not file
paths typed into a browser fetch. Bound file size and row count before parsing.
Render text safely; preserve leading zeros and explicit date/timezone semantics.

For XLSX, use an employer-approved, pinned browser parser or an authorized host
spreadsheet capability. Select the worksheet explicitly, distinguish formulas
from cached values, and preserve numeric/date types. A browser parser cannot
assume formula recalculation. Use the approved document provider; this library
does not redistribute the restricted Anthropic XLSX implementation.

OneDrive/SharePoint: prefer approved authenticated file download for read-only
snapshots. Graph driveItem content supports delegated Files.Read. Workbook range
GET instead requires delegated Files.ReadWrite and has no application permission
support. Do not silently expand scopes for a read-only report. Preauthenticated
download URLs are short-lived secrets; do not store or print them in artifacts.

Display filename or approved source label, capture time, data-as-of time if known,
and the manual refresh procedure. Export visible filtered rows; verify exported
content and neutralize spreadsheet formulas in untrusted string cells.

Sources reviewed 2026-10-29:
- [Graph file download](https://learn.microsoft.com/en-us/graph/api/driveitem-get-content?view=graph-rest-1.0)
- [Graph range read](https://learn.microsoft.com/en-us/graph/api/range-get?view=graph-rest-1.0)
