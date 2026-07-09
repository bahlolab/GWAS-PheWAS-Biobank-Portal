# Contributing

Thanks for helping keep this catalog accurate and useful. Contributions fall into a few common categories — pick the one that matches what you're doing.

## 1. Adding a new portal

1. Check `data/portals.json` (or the README table) first to make sure it isn't already listed under a different name.
2. Open `scripts/build_database.py` and add a new `dict(...)` entry to the `PORTALS` list, filling in every field listed in [`docs/SCHEMA.md`](docs/SCHEMA.md). Copy an existing similar entry as a template.
   - Prefer the portal's own "About"/documentation page as your source for sample size, ancestry, and license fields. Link it in the `documentation` field.
   - If a field is genuinely unclear (e.g., you can't tell whether bulk download is offered), use `"U"` rather than guessing, and explain in `notes`.
   - Keep `notes` factual and specific — what makes this portal different from similar ones already in the catalog, any caveats about data curation/beta status, and its relationship to other entries (e.g., "built on the PheWeb framework used by FinnGen").
3. Regenerate everything:
   ```bash
   python3 scripts/build_database.py
   python3 scripts/generate_tables.py
   python3 scripts/update_readme.py
   python3 scripts/validate_links.py
   ```
4. Open a PR. In the PR description, briefly say how you verified the metadata (e.g., "confirmed sample size and license from the portal's About page, linked above").

## 2. Correcting existing metadata

Same workflow as above — edit the relevant `dict(...)` entry in `scripts/build_database.py` (not the generated CSV/JSON files directly, they will just get overwritten), regenerate, and open a PR explaining what changed and why (a new data release, a corrected sample size, a license change, etc.).

## 3. Reporting a broken link

- Fastest: open an issue with the portal name and the URL that's failing.
- Better: run `python3 scripts/validate_links.py`, confirm the failure locally, and open a PR that either fixes the URL (if the portal moved) or, if the portal appears genuinely discontinued, updates its entry's `notes` field to say so (please don't delete entries for discontinued portals outright — mark them and let maintainers decide, since historical portals are still useful reference points, e.g. superseded FinnGen release browsers).

## 4. Adding a script/workflow feature

PRs to `scripts/` or `.github/workflows/` are welcome (e.g., additional export formats, smarter link-check retry logic, badge generation). Please keep scripts dependency-free (Python 3 standard library only) unless there's a strong reason not to — this keeps the repo easy to fork and run anywhere without a package manager.

## Style notes

- Portal `id` values are lowercase, hyphenated slugs (e.g., `finngen-pheweb`), and are used as stable keys — please don't change an existing `id` without a good reason, since external references may depend on it.
- Keep `sample_size` and `ancestry` as short free-text strings (not fully structured) — precision matters less here than staying current, and different portals report these very differently.
- The `tags` field is semicolon-separated and pulled from the fixed vocabulary in the README's Categories section — please don't invent new tags without discussing in the PR first, so the tag list stays a useful, finite filter set.

## Code of conduct

Be constructive and specific. This is a niche technical resource maintained by volunteers in the genetics/bioinformatics community — corrections and additions are almost always welcome, but please back metadata claims with a link to the primary source.
