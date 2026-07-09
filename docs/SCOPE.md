# Scope: what counts as "publicly available" here

This catalog only includes resources that meet **at least one** of these bars:

1. **Open interactive portal** — anyone can query gene/variant/phenotype/region without logging in (e.g., FinnGen PheWeb, GWAS Catalog, Open Targets, Genebass, AZ PheWAS, BioBank Japan PheWeb).
2. **Open bulk download / API** — full summary statistics or a documented API are downloadable by anyone, with at most a free account or API token (no committee review, no data-use agreement requiring justification of a specific project) — e.g., OpenGWAS, Pan-UKB, GBMI, MVP PheWAS summary release on dbGaP, T2DKP/CVDKP.
3. **Open public tier of a larger controlled resource** — e.g., the All of Us **Data Browser** (aggregate summaries, no login) is included even though the All of Us Researcher Workbench (individual-level data, free registration + training) is a separate, more involved tier not itself catalogued here as if it were a simple portal.

Resources are **excluded** if the *only* way to see any data — even summary-level — is through a formal application to a data access/ethics committee that evaluates the requester's project, institution, or credentials. That describes several major biobanks that nonetheless deserve a mention, since researchers often assume (incorrectly) that they have a public browser:

| Biobank | Why it's excluded | Where its data *does* surface publicly |
|---|---|---|
| deCODE genetics | No public interactive portal or standing bulk-download page | Individual published GWAS often deposited to the GWAS Catalog per-study |
| Estonian Biobank | Individual-level data requires Estonian Biobank Access Committee approval | Summary statistics released alongside individual publications (check the paper, not a portal) |
| Taiwan Biobank | Requires application to the TWB Data Access Committee | Some published GWAS summary statistics deposited to the GWAS Catalog |
| HUNT Study (Norway) | Requires HUNT Data Access Committee approval | Contributes summary statistics to consortium meta-analyses, e.g. GBMI |
| China Kadoorie Biobank | Requires formal CKB Data Access application | Some GWAS summary statistics deposited per publication |
| National Biobank of Korea / KoGES | Requires application via the Korea Biobank Network | Contributes to GBMI and individual consortium papers |
| Genomics England / 100,000 Genomes Project | Individual-level WGS only inside the controlled Research Environment | No public summary-statistics browser |
| iPSYCH (Denmark) | Individual-level data requires application | Case counts contribute to Psychiatric Genomics Consortium (PGC) meta-analyses, which **are** public (see the `pgc-download` entry in this catalog) |

If one of these institutions launches a genuine public browser or open bulk-download page, please open a PR — see [`CONTRIBUTING.md`](../CONTRIBUTING.md) — and it will move from this exclusion list into the main catalog.

## A note on partial public tiers

A few entries in the catalog (`mvp-dbgap`, `allofus-databrowser`) sit inside larger resources that also have a controlled-access tier. In these cases the catalog entry, its `url`, and its `license`/`notes` fields refer **specifically** to the openly accessible component (e.g., the MVP PheWAS summary-statistics release on dbGaP, or the All of Us public Data Browser) — not to the full individual-level dataset, which still requires separate registration/application and is out of scope for this catalog.
