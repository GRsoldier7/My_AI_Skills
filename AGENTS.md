# AI Skills repository guidance

Edit canonical sources at the paths indexed in `registry/skills.json`. Owner project workflows live in `skills/aarons-latest/`. Read one selected `SKILL.md` and its required references. Keep private context and identifying client, employer, faith-group and household records in the intended private project.

## Project lifecycle

Use `skills/aarons-latest/project-router/SKILL.md` for startup, next-step selection, resumption, rescoping, cleanup and readiness. Give each task one owner. For a domain task, use the appropriate skill directly. On a host with no verified native invocation, read and apply the instructions as a manual pack. Label live actions, draft outputs and packaging checks accurately.

## Maintain the library

- Keep canonical packages intact, including licenses, references and assets. Edit the existing set of canonical paths when a use case spans domains.
- Curation lives in `registry/curation.json`. Regenerate `registry/skills.json` and the five agent index tables from a complete checkout with `python scripts/generate-skill-registry.py --registry`. Preserve registry caps, the compatibility map and host fences.
- Run `python scripts/check-library.py` before releasing changes. Use the contribution guide for the Linux installer and additional checks. Device or account activation is a separate operation.
- Preserve the seven-skill distribution owned by `scripts/project-router.py`. Use `python scripts/project-router.py build` for the private plugin. Keep personal settings, external servers and unrelated skills outside its build. See `platform-configs/openai/project-router/README.md`.
- Name dated plans, reports and handoffs `YYYYMMDD - {Tool/Project} - {Short Concise Description}`. Match the Markdown H1 to the filename stem. Stable interface files such as `SKILL.md`, `README.md`, scripts and set manifests keep their conventional names.
