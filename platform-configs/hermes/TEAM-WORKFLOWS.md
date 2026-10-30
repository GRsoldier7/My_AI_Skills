# Team role selection and host acceptance

`team-selections.json` lists candidates, not auto-enabled agents. Hermes remains
the coordinator. ECC and Addy provide alternative review/planning specialists;
Agency supplies on-demand domain personas. Avoid duplicate reviewers doing the
same pass. The source collection may describe autonomous behavior or memory;
those claims do not establish runtime permissions, durable storage, or access.

Use independent read-only specialists in parallel when their results can be
combined by the lead. Give each a concrete task, source/revision, allowed scope,
available tools, budget, and report contract. Dependent work stays sequential.
The four ECC adapters in agents/hermes map Claude-style personas to task briefs.
The four Addy personas use their linked workflow skills; they do not spawn one
another. The Addy meta-skill is an explicit alternative controller only.

Agency Copilot candidates are listed with target *.agent.md names. The exporter
must render portable name/description fields, include the selected canonical
body and source/license attribution, and apply the work boundary: no MCP,
auto-installation, hooks, broader credential access, or unrequested publishing.
This file alone does not create Copilot registrations.

Native-host acceptance follows staging: verify discovery of only selected roles;
run a harmless task, a failed child, cancellation, and a missing-tool case; check
that tool/credential scope is inherited from the approved host. Verify no duplicate
workflow owner is injected. Keep profile config, memory, session transcripts,
authentication artifacts, and actual employer/client evidence outside Git.
The repository's fake lifecycle tests do not establish durable restart recovery.
