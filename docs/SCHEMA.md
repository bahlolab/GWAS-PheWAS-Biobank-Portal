# Database schema

`data/portals.csv` and `data/portals.json` share an identical schema (one row / object per portal). Both are generated from the single source of truth, the `PORTALS` list in `scripts/build_database.py` — do not hand-edit the CSV/JSON directly.

Boolean-ish fields use a 3-value convention rather than strict true/false, because portal capabilities are frequently partial or conditional:

| Code | Meaning |
|---|---|
| `Y` | Yes / fully supported |
| `P` | Partial — conditional, indirect, or only for a subset of data |
| `N` | No / not supported |
| `U` | Unknown / could not be verified at time of writing |

## Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Stable slug identifier, used as the primary key. Lowercase, hyphenated. |
| `name` | string | Display name of the portal. |
| `url` | string | Primary URL of the portal (checked by `validate_links.py`). |
| `institution` | string | Owning/operating institution(s) or consortium. |
| `country` | string | Country or countries of the operating institution / cohort. |
| `cohort` | string | Underlying cohort(s) or data source(s) powering the portal. |
| `sample_size` | string | Approximate sample size, as free text (units vary — participants, exomes, genomes — see the string itself). |
| `ancestry` | string | Ancestry composition of the underlying cohort. |
| `gwas` | Y/P/N | Common-variant GWAS summary statistics available. |
| `phewas` | Y/P/N | Phenome-wide association (variant → many phenotypes) supported. |
| `wes` | Y/P/N | Whole-exome sequencing data underlies the resource. |
| `wgs` | Y/P/N | Whole-genome sequencing data underlies the resource. |
| `cnv` | Y/P/N | Copy-number variant data included. |
| `rare_variant` | Y/P/N | Rare-variant association results available. |
| `burden_test` | Y/P/N | Gene-level burden/collapsing association tests available. |
| `eqtl` | Y/P/N | Expression QTL data/results available. |
| `pqtl` | Y/P/N | Protein QTL data/results available. |
| `twas` | Y/P/N | Transcriptome-wide association study results available. |
| `lab_traits` | Y/P/N | Clinical laboratory trait phenotypes included. |
| `imaging` | Y/P/N | Imaging-derived phenotypes included. |
| `drug_targets` | Y/P/N | Portal is oriented toward / supports drug target identification. |
| `multi_omics` | Y/P/N | Integrates 2+ distinct -omics data types. |
| `query_gene` | Y/P/N | Supports searching/filtering by gene symbol. |
| `query_variant` | Y/P/N | Supports searching by variant (rsID or chr:pos:ref:alt). |
| `query_phenotype` | Y/P/N | Supports searching/browsing by phenotype/endpoint. |
| `query_region` | Y/P/N | Supports searching by genomic region (chr:start-end). |
| `query_trait` | Y/P/N | Supports searching/filtering by trait (may overlap with phenotype for quantitative traits). |
| `summary_stats` | Y/P/N | Full GWAS summary statistics (not just top hits) are available. |
| `api_available` | Y/P/N | A documented, machine-queryable API exists. |
| `bulk_download` | Y/P/N | Bulk/flat-file download of the underlying data is available. |
| `license` | string | Free-text description of license/access terms as understood at time of writing. **Always verify on the source site** — this field is a summary, not a legal reference. |
| `last_updated` | string | Most recent known release/version or update, as free text. |
| `documentation` | string (URL) | Link to the portal's own documentation/about page. |
| `github` | string (URL) | Link to the portal's public source-code repository, if one exists. |
| `tags` | string | Semicolon-separated list of category tags (see README § Categories). |
| `notes` | string | Free-text notes: caveats, relationships to other portals, what makes this resource distinctive. |

## Adding a new portal

Append a new `dict(...)` entry to the `PORTALS` list in `scripts/build_database.py`, following the existing style. All fields in `FIELDS` are required (the build script will raise a `ValueError` listing any that are missing). Use `"U"` rather than guessing if a boolean-ish field is genuinely unknown, and say so in `notes` if it matters.
