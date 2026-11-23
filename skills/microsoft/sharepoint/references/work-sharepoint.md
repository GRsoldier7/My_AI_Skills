# SharePoint site, library and list review

Use for a SharePoint information architecture proposal, slow list view or search for authoritative material. Return a schema/view proposal or a cited answer. Use only the scoped, existing read-only SharePoint reader when requested. Proposed columns, views, permissions and version settings are a draft for the site owner.

| Need | First decision | Deliverable |
|---|---|---|
| Find the approved procedure | Scope site/library, terms, approval state and effective date. Inspect the exact published item and requested section where visible. | Claim plus returned item link or scoped ID, library, version, heading/page, modified or effective date, and access depth. Treat metadata-only hits as leads. |
| Track structured requests | Define one row per request, a stable key, expected volume and primary lookups. Use a list if fields and state drive the work. | Field dictionary with type, required/unique rule, allowed values and owner. Specify default, filtered and exception views. |
| Govern documents | Use a library when the file, its revisions and approved content are the record. Identify canonical library, content owner, review dates, classification and readers. | Proposed metadata, inherited access boundary, version/approval lifecycle and a view of items due for review. Flag permissions or retention settings the owner must confirm. |

**Synthetic design.** A request list has `RequestKey` (unique text), `Status` (single choice), `OpenedOn` (date) and `Owner` (person). Define “Unassigned open requests this month” with a selective indexed date filter first, then status/owner filters. Estimate the rows the first filter admits and test against the actual list size. If it still admits too many, choose a narrower date range or a more selective indexed field. A view filter helps readers navigate. It does not enforce per-item access.

**Evidence and failure checks.** A newer draft cannot establish current policy solely from its modification time. Record “approval unclear” if the reader cannot see the approval state. Record “metadata only” if it cannot open the file. Identical titles in different libraries remain separate until an exact identity and version match. A partial or security-trimmed result cannot establish that a document does not exist. For a schema redesign, include a synthetic sample, affected existing views/apps, a reversible draft migration and the owner who would validate it.

[Microsoft Learn: information architecture](https://learn.microsoft.com/en-us/sharepoint/information-architecture-modern-experience) · [version history](https://learn.microsoft.com/en-us/sharepoint/version-overview) · [indexed filters in large lists](https://learn.microsoft.com/en-us/troubleshoot/sharepoint/lists-and-libraries/fails-filtering-sharepoint-column)
