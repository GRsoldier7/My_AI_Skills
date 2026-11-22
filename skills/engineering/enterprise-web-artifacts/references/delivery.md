# Choose an artifact host

| Need | Recommended route | What to verify |
| --- | --- | --- |
| One-off internal briefing with an approved snapshot | One self-contained HTML document with inline styles, data and optional script | Open from disk with the network unavailable. Verify the static content when scripts are disabled. Distribution of a snapshot conveys its embedded data. |
| Interactive metrics already modeled in Power BI | Secure Power BI web part on a modern SharePoint page | Verify both SharePoint access and Power BI report access, including the intended viewer's RLS result. Private data must never use Publish to web. |
| App-like behavior on a modern SharePoint page | Approved SPFx web part using supported packaging and the target site context | Confirm the app catalog route and approver. A site owner may lack deployment authority. Test the reader role, access denial and recovery in QA. |
| Durable data entry, approvals or a workflow button | Power Apps plus a solution-aware flow or an approved component | Define validation, authorization and duplicate-submit behavior before designing the button. A Power Apps code component uses PCF. |

A downloaded HTML file is a snapshot. Browser edits to it do not automatically update an Excel workbook or SharePoint List. For an ongoing report-out, use an approved list, database or semantic model as the source. For an approved write-back design, put authentication and input validation at the controlled service or app boundary. Keep tokens, signed trigger URLs and confidential row data out of HTML. If the host cannot run scripts, supply the static brief or native Power BI page.

[Microsoft SharePoint web parts](https://learn.microsoft.com/en-us/sharepoint/dev/spfx/web-parts/overview-client-side-web-parts) · [Power BI in SharePoint](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-embed-report-spo) · [Power Apps component framework](https://learn.microsoft.com/en-us/power-apps/developer/component-framework/overview)
