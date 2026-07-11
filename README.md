# 🧬 GWAS / PheWAS / Biobank Portal Catalog
![](data/GWAS.png)

[![Check Links](https://github.com/bahlolab/GWAS-PheWAS-Biobank-Portal/actions/workflows/check-links.yml/badge.svg)](https://github.com/bahlolab/GWAS-PheWAS-Biobank-Portal/actions/workflows/check-links.yml)
[![Update Metadata](https://github.com/bahlolab/GWAS-PheWAS-Biobank-Portal/actions/workflows/update-metadata.yml/badge.svg)](https://github.com/bahlolab/GWAS-PheWAS-Biobank-Portal/actions/workflows/update-metadata.yml)
![Portals cataloged](https://img.shields.io/badge/portals-<!-- PORTAL_COUNT_START -->30<!-- PORTAL_COUNT_END -->-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A community-maintained, structured index of publicly available **GWAS**, **PheWAS**, and **biobank-derived web portals** — built so that geneticists, statistical geneticists, and bioinformaticians can quickly find the right tool for a gene, variant, phenotype, or region query without re-discovering the same resources from scratch every time.

> **Scope: public access only.** Every entry in this catalog can be queried or its summary statistics downloaded **without a formal data-access application** — free registration for an API token or Researcher Workbench (e.g., FinnGen, OpenGWAS, All of Us) is fine, but resources whose *only* access route is a controlled-access committee (e.g., dbGaP full individual-level data, UK Biobank RAP, most national biobanks without a public browser) are intentionally excluded. See [`docs/SCOPE.md`](docs/SCOPE.md) for the exact inclusion rule and a list of notable biobanks left out for this reason.

> Last refreshed: <!-- LAST_UPDATED_START -->2026-07-09<!-- LAST_UPDATED_END --> · See [`data/portals.csv`](data/portals.csv) / [`data/portals.json`](data/portals.json) for the machine-readable database and [`data/link_status.json`](data/link_status.json) for the latest automated link-check report.

---

## Table of contents

- [Introduction](#introduction)
- [Motivation](#motivation)
- [Quick start](#quick-start)
- [Portal comparison table](#portal-comparison-table)
- [Feature comparison matrix](#feature-comparison-matrix)
- [Categories](#categories)
- [Search tips](#search-tips)
- [Repository structure](#repository-structure)
- [Keeping this catalog current](#keeping-this-catalog-current)
- [Contributing](#contributing)
- [Citation](#citation)
- [License](#license)
- [Disclaimer](#disclaimer)

---

## Introduction

Over the last fifteen years, national and international biobanks (UK Biobank, FinnGen, Biobank Japan, the Million Veteran Program, All of Us, and dozens of others) have released an enormous and rapidly growing collection of **GWAS summary statistics**, **PheWAS browsers**, **gene-burden/rare-variant portals**, and **multi-omic (eQTL/pQTL) resources**. Each is built on a different platform (PheWeb, custom Django/React apps, Hail-backed browsers, GraphQL APIs...), hosted at a different institution, and documented (or not) in a different way.

This repository catalogs those resources in one place, with a consistent metadata schema, so that a researcher who needs to ask "does gene *X* have a rare-variant burden association with disease *Y*, and is that visible anywhere without a data-access application?" can find the answer in minutes rather than hours.

## Motivation

- **Discovery is hard.** Many excellent portals (JENGER, LAVAA, MMP, CARTaGENE PheWeb, FinMetSeq...) are only known within their home consortium and rarely surface in general search.
- **Access models vary wildly.** Some portals are fully open (GWAS Catalog, Open Targets), some require free registration (FinnGen PheWeb, OpenGWAS API tokens), and some require formal data-access applications (dbGaP, UK Biobank, most national biobanks). Knowing this *before* you start is valuable.
- **Feature sets are inconsistent.** Not every portal supports gene search, region search, bulk download, or an API — this catalog captures that explicitly so you can filter for what you actually need.
- **Metadata goes stale.** Releases increment (FinnGen R5 → R13...), URLs change, and portals occasionally disappear. This repo is designed to be *maintainable*: a CSV/JSON database, scripts to validate links, and CI automation, rather than a static list that rots after one commit.

## Quick start

```bash
git clone https://github.com/bahlolab/GWAS-PheWAS-Biobank-Portal.git
cd REPO

# Explore the database directly
python3 -c "import csv; [print(r['name'], '-', r['url']) for r in csv.DictReader(open('data/portals.csv'))]"

# Or query with jq / pandas / R as you prefer:
jq '.[] | select(.rare_variant=="Y") | .name' data/portals.json
```

No dependencies beyond the Python 3 standard library are required to read the data. `scripts/validate_links.py` and `scripts/build_database.py` are also stdlib-only, so the catalog is trivial to fork and adapt.

---

## Portal comparison table

Legend: ✅ = yes, ◐ = partial/conditional, — = no / not applicable.

<!-- PORTAL_TABLE_START -->
| Portal | Institution | Country | Cohort | Sample Size | Ancestry | Summary Stats | API | Bulk DL |
|---|---|---|---|---|---|---|---|---|
| [All of Us Data Browser (Public Tier)](https://databrowser.researchallofus.org/) | US National Institutes of Health (NIH) | United States | All of Us Research Program | 413,000+ (WGS, 2024 release); target 1,000,000+ enrolled | Highly diverse, majority historically underrepresented in biomedical research | ◐ | — | — |
| [AstraZeneca PheWAS Portal](https://azphewas.com/) | AstraZeneca Centre for Genomics Research | United Kingdom / Global (industry) | UK Biobank whole-exome sequencing | ~470,000 exomes (v5 release) | Predominantly European, multi-ancestry subsets included | ✅ | — | ✅ |
| [BioBank Japan PheWeb (PheWeb.jp)](https://pheweb.jp/) | BioBank Japan (Univ. of Tokyo IMSUT) / RIKEN IMS / Osaka University | Japan | BioBank Japan (BBJ) | ~260,000 (47-51 target diseases) | East Asian (Japanese) | ✅ | — | ✅ |
| [Cardiovascular Disease Knowledge Portal (CVDKP)](https://cvd.hugeamp.org/) | Broad Institute / CVDKP Consortium | United States (international consortium) | Aggregates GWAS across cardiovascular/metabolic cohorts | Varies by dataset (aggregator) | Multi-ancestry (aggregated) | ✅ | ✅ | ✅ |
| [CARTaGENE PheWeb](https://cerc-genomic-medicine.ca/pheweb/cartagene/) | CERC in Genomic Medicine (Univ. of Michigan / Univ. de Montréal) | Canada (Québec) | CARTaGENE | ~20,000 (European-ancestry subset analysed) | European (analysis restricted to EUR ancestry in this release) | ✅ | — | ✅ |
| [DICE (Database of Immune Cell Expression, eQTLs and Epigenomics)](https://dice-database.org/) | La Jolla Institute for Immunology | United States | Healthy human donors, sorted immune cell subsets | ~91 donors, 15+ immune cell types | Not the primary axis (small reference cohort) | ✅ | — | ✅ |
| [EpiGraphDB](https://epigraphdb.org/) | MRC Integrative Epidemiology Unit, University of Bristol | United Kingdom | Graph database integrating OpenGWAS, literature, and other epidemiological resources | N/A (integrative knowledge graph) | N/A | ◐ | ✅ | ◐ |
| [FinMetSeq PheWeb](https://pheweb.sph.umich.edu/FinMetSeq/) | University of Michigan (SPH) / University of Eastern Finland (METSIM) | Finland / United States | METSIM (Metabolic Syndrome in Men) | ~6,136 Finnish men (metabolomics GWAS on 1,391 metabolites) | European (Finnish) | ✅ | — | ✅ |
| [FinnGen PheWeb (latest release)](https://r13.finngen.fi) | FinnGen Consortium (HUS, Univ. Helsinki, THL, biobanks) | Finland | FinnGen (Finnish biobanks + national health registries) | ~500,000 | European (Finnish founder population) | ✅ | ◐ | ✅ |
| [Genebass](https://app.genebass.org/) | Broad Institute (Neale Lab / MacArthur Lab) | United States | UK Biobank whole-exome sequencing | ~400,000+ exomes | Multi-ancestry (predominantly European) | ✅ | — | ✅ |
| [Global Biobank Meta-analysis Initiative (GBMI) results browser](https://www.globalbiobankmeta.org/resources) | GBMI (23+ biobanks consortium, coordinated via Broad/Massachusetts General Hospital) | International (4 continents) | 23 member biobanks (UKB, FinnGen, BBJ, MVP, and others) | ~2,200,000 consented individuals with genetic data | Multi-ancestry (explicit goal of diversity) | ✅ | — | ✅ |
| [GTEx Portal (Genotype-Tissue Expression)](https://gtexportal.org/home/) | Broad Institute / NIH Common Fund | United States | GTEx (postmortem tissue donors) | ~950 donors, 54 tissues | Predominantly European (US donor pool) | ✅ | ✅ | ✅ |
| [GWAS ATLAS (Complex Trait Genetics Lab)](https://atlas.ctglab.nl/) | Complex Trait Genetics Lab, VU Amsterdam | Netherlands | Curated repository of thousands of GWAS summary statistics | Varies by study (aggregator, 4,000+ GWAS) | Multi-ancestry (aggregated) | ✅ | — | ✅ |
| [GWASLab / CTG Catalog (meta-index of sumstats resources)](https://catalog.gwaslab.org/) | GWASLab (community-maintained) | International | Meta-index of biobanks and consortium GWAS | N/A (index of other resources) | N/A (index) | ◐ | — | — |
| [JENGER (Japanese ENcyclopedia of GEnetic associations by Riken)](http://jenger.riken.jp/en/) | RIKEN Center for Integrative Medical Sciences | Japan | BBJ + IMM, JPHC, J-MICC, TMM cohorts | ~200,000+ (combined collaborators) | East Asian (Japanese) | ✅ | — | ✅ |
| [LAVAA (volcano plot PheWAS viewer)](https://geneviz.aalto.fi/LAVAA/) | Aalto University / FinnGen | Finland | FinnGen and user-imported GWAS/PheWAS (e.g., OpenGWAS) | Varies | Varies | — | — | — |
| [Million Veteran Program (MVP) PheWAS/GWAS summary results via dbGaP](https://www.ncbi.nlm.nih.gov/gap/) | US Department of Veterans Affairs | United States | Million Veteran Program | ~1,000,000 enrolled; ~650,000+ genotyped | Multi-ancestry (EUR, AFR, AMR, EAS HARE groups) | ✅ | — | ◐ |
| [MRC IEU OpenGWAS (gwas.mrcieu.ac.uk / MR-Base)](https://gwas.mrcieu.ac.uk/) | MRC Integrative Epidemiology Unit, University of Bristol | United Kingdom | Aggregates 40,000+ GWAS datasets (biobanks, consortia, UKB) | Varies by dataset (aggregator) | Multi-ancestry (aggregated) | ✅ | ✅ | ✅ |
| [Multiple Manhattan Plot (MMP)](https://mmp.finngen.fi/) | FinnGen Consortium | Finland | FinnGen / user-supplied GWAS | Varies (custom uploads) | Varies | — | — | — |
| [Neale Lab UK Biobank GWAS (rounds 1-2, historical)](http://www.nealelab.is/uk-biobank) | Broad Institute (Neale Lab) | United States | UK Biobank (European ancestry) | ~337,000 (round 2) | European | ✅ | — | ✅ |
| [NHGRI-EBI GWAS Catalog](https://www.ebi.ac.uk/gwas/) | EMBL-EBI / NHGRI | United Kingdom / United States (international) | Curated from >45,000 published GWAS across thousands of cohorts | Varies by study (aggregates >45,000 studies) | Multi-ancestry (curated, historically Euro-centric) | ✅ | ✅ | ✅ |
| [Open Targets Genetics (legacy, merged into Platform)](https://genetics.opentargets.org/) | EMBL-EBI / Wellcome Sanger / GSK | United Kingdom (international) | GWAS Catalog + UK Biobank fine-mapping | 133,000+ study-loci associations (historical) | Multi-ancestry | ✅ | ✅ | ✅ |
| [Open Targets Platform](https://platform.opentargets.org/) | EMBL-EBI / Wellcome Sanger / GSK / other industry partners | United Kingdom (international consortium) | Integrates GWAS Catalog, UK Biobank, FinnGen, gene-burden studies (Genebass, Regeneron, AZ PheWAS), ChEMBL, ClinVar, etc. | Aggregates data across hundreds of cohorts/studies | Multi-ancestry (aggregated) | ◐ | ✅ | ✅ |
| [Pan-UK Biobank (Pan-UKB)](https://pan.ukbb.broadinstitute.org/) | Broad Institute (Neale Lab / Atkinson / Martin labs) | United States / United Kingdom | UK Biobank, multi-ancestry | ~488,000 (7,221+ phenotypes analysed) | 6 continental ancestry groups (EUR, AFR, AMR, EAS, SAS, MID) | ✅ | — | ✅ |
| [PheWeb.org instance directory (Univ. Michigan-hosted browsers)](https://pheweb.org/) | University of Michigan (Boehnke/Abecasis groups) and PheWeb open-source project | United States (hosts multiple international cohorts) | Multiple (varies per instance) | Varies per instance | Varies per instance | ✅ | — | ✅ |
| [PsychENCODE Knowledge Portal](http://resource.psychencode.org/) | PsychENCODE Consortium (NIMH-funded) | United States | Postmortem human brain tissue (multiple psychiatric-disease and control cohorts) | ~2,000 brain samples (combined studies) | Predominantly European (US cohorts) | ✅ | — | ✅ |
| [Psychiatric Genomics Consortium (PGC) Downloads](https://pgc.unc.edu/for-researchers/download-results/) | Psychiatric Genomics Consortium (international collaboration) | International | Meta-analyses across 100+ contributing cohorts (incl. iPSYCH, UKB, deCODE, FinnGen) | Varies by disorder (largest analyses >1,000,000 combined with UKB/23andMe) | Predominantly European; increasing multi-ancestry (PGC3+ waves) | ✅ | — | ✅ |
| [Risteys (FinnGen + FinRegistry endpoint browser)](https://risteys.finngen.fi/) | FinnGen / FinRegistry (THL, FIMM, Univ. Helsinki) | Finland | FinnGen + FinRegistry | 500,000 (FinnGen); ~7,000,000 (FinRegistry) | European (Finnish) | — | — | ◐ |
| [Type 2 Diabetes Knowledge Portal (T2DKP) / CMDKP](https://t2d.hugeamp.org/) | Broad Institute / AMP-T2D Consortium | United States (international consortium) | Aggregates 380+ GWAS datasets across T2D/metabolic cohorts | Varies by dataset (aggregator) | Multi-ancestry (aggregated) | ✅ | ✅ | ✅ |
| [UK Biobank Pharma Proteomics Project (UKB-PPP) pQTL browser](https://research.regeneron.com/ukb-ppp) | UK Biobank / Regeneron / GSK / Pharma consortium (13 companies) | United Kingdom / International industry consortium | UK Biobank (Olink proteomics subset) | ~54,000 participants, ~3,000 proteins | Multi-ancestry (predominantly European) | ✅ | — | ✅ |
<!-- PORTAL_TABLE_END -->

> The full record for each portal — including query types supported, license/access restrictions, documentation links, and free-text notes — is in [`data/portals.csv`](data/portals.csv) / [`data/portals.json`](data/portals.json). The table above shows only a summary slice.

## Feature comparison matrix

Legend: ✅ = yes, ◐ = partial/conditional, — = no.

<!-- FEATURE_MATRIX_START -->
| Portal | GWAS | PheWAS | WES | WGS | CNV | Rare Var. | Burden | eQTL | pQTL | TWAS | Lab | Imaging | Drug Tgt | Multi-omics |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [All of Us Data Browser (Public Tier)](https://databrowser.researchallofus.org/) | ◐ | — | — | ✅ | ◐ | ✅ | — | — | — | — | ✅ | — | — | ◐ |
| [AstraZeneca PheWAS Portal](https://azphewas.com/) | — | ✅ | ✅ | — | — | ✅ | ✅ | — | — | — | ✅ | — | ✅ | — |
| [BioBank Japan PheWeb (PheWeb.jp)](https://pheweb.jp/) | ✅ | ✅ | — | — | — | — | — | — | — | — | ✅ | — | — | — |
| [Cardiovascular Disease Knowledge Portal (CVDKP)](https://cvd.hugeamp.org/) | ✅ | ◐ | ✅ | ◐ | — | ✅ | ✅ | ✅ | — | — | ✅ | — | ✅ | ◐ |
| [CARTaGENE PheWeb](https://cerc-genomic-medicine.ca/pheweb/cartagene/) | ✅ | ✅ | — | — | — | — | — | — | — | — | ✅ | — | — | — |
| [DICE (Database of Immune Cell Expression, eQTLs and Epigenomics)](https://dice-database.org/) | — | — | — | — | — | — | — | ✅ | — | — | — | — | — | ✅ |
| [EpiGraphDB](https://epigraphdb.org/) | ◐ | ◐ | — | — | — | — | — | ✅ | ✅ | — | — | — | ✅ | ✅ |
| [FinMetSeq PheWeb](https://pheweb.sph.umich.edu/FinMetSeq/) | ✅ | ◐ | — | — | — | ◐ | — | — | — | — | ✅ | — | — | ✅ |
| [FinnGen PheWeb (latest release)](https://r13.finngen.fi) | ✅ | ✅ | — | — | — | ◐ | ✅ | — | ✅ | — | ✅ | — | ◐ | ◐ |
| [Genebass](https://app.genebass.org/) | — | ✅ | ✅ | — | — | ✅ | ✅ | — | — | — | ✅ | — | — | — |
| [Global Biobank Meta-analysis Initiative (GBMI) results browser](https://www.globalbiobankmeta.org/resources) | ✅ | — | — | — | — | — | — | — | — | — | — | — | — | — |
| [GTEx Portal (Genotype-Tissue Expression)](https://gtexportal.org/home/) | — | — | — | ✅ | — | ◐ | — | ✅ | — | ✅ | — | — | — | ✅ |
| [GWAS ATLAS (Complex Trait Genetics Lab)](https://atlas.ctglab.nl/) | ✅ | ✅ | — | — | — | — | — | — | — | — | ✅ | ◐ | — | — |
| [GWASLab / CTG Catalog (meta-index of sumstats resources)](https://catalog.gwaslab.org/) | ✅ | ◐ | — | — | — | — | — | — | — | — | — | — | — | — |
| [JENGER (Japanese ENcyclopedia of GEnetic associations by Riken)](http://jenger.riken.jp/en/) | ✅ | — | — | — | — | — | — | — | — | — | ✅ | — | — | — |
| [LAVAA (volcano plot PheWAS viewer)](https://geneviz.aalto.fi/LAVAA/) | — | ✅ | — | — | — | — | — | — | — | — | — | — | — | — |
| [Million Veteran Program (MVP) PheWAS/GWAS summary results via dbGaP](https://www.ncbi.nlm.nih.gov/gap/) | ✅ | ✅ | — | — | — | — | — | — | — | ✅ | ✅ | — | — | — |
| [MRC IEU OpenGWAS (gwas.mrcieu.ac.uk / MR-Base)](https://gwas.mrcieu.ac.uk/) | ✅ | ✅ | — | — | — | — | — | ✅ | ✅ | — | ✅ | ✅ | — | ◐ |
| [Multiple Manhattan Plot (MMP)](https://mmp.finngen.fi/) | ✅ | — | — | — | — | — | — | — | — | — | — | — | — | — |
| [Neale Lab UK Biobank GWAS (rounds 1-2, historical)](http://www.nealelab.is/uk-biobank) | ✅ | — | — | — | — | — | — | — | — | — | ✅ | — | — | — |
| [NHGRI-EBI GWAS Catalog](https://www.ebi.ac.uk/gwas/) | ✅ | ◐ | ◐ | ◐ | ✅ | ◐ | ◐ | — | — | — | ✅ | ✅ | — | — |
| [Open Targets Genetics (legacy, merged into Platform)](https://genetics.opentargets.org/) | ✅ | — | — | — | — | — | — | ✅ | ◐ | — | — | — | ✅ | ◐ |
| [Open Targets Platform](https://platform.opentargets.org/) | ✅ | ✅ | ✅ | ◐ | ◐ | ✅ | ✅ | ✅ | ✅ | ◐ | ✅ | — | ✅ | ✅ |
| [Pan-UK Biobank (Pan-UKB)](https://pan.ukbb.broadinstitute.org/) | ✅ | ✅ | — | — | — | — | — | — | — | — | ✅ | — | — | — |
| [PheWeb.org instance directory (Univ. Michigan-hosted browsers)](https://pheweb.org/) | ✅ | ✅ | — | — | — | — | — | — | — | — | ◐ | — | — | ◐ |
| [PsychENCODE Knowledge Portal](http://resource.psychencode.org/) | — | — | — | ✅ | ◐ | ◐ | — | ✅ | — | ✅ | — | — | — | ✅ |
| [Psychiatric Genomics Consortium (PGC) Downloads](https://pgc.unc.edu/for-researchers/download-results/) | ✅ | — | — | — | ◐ | ◐ | — | — | — | ◐ | — | — | — | — |
| [Risteys (FinnGen + FinRegistry endpoint browser)](https://risteys.finngen.fi/) | — | ✅ | — | — | — | — | — | — | — | — | ✅ | — | — | — |
| [Type 2 Diabetes Knowledge Portal (T2DKP) / CMDKP](https://t2d.hugeamp.org/) | ✅ | ◐ | ✅ | ◐ | — | ✅ | ✅ | ✅ | — | — | ✅ | — | ✅ | ◐ |
| [UK Biobank Pharma Proteomics Project (UKB-PPP) pQTL browser](https://research.regeneron.com/ukb-ppp) | — | — | — | — | — | ◐ | — | — | ✅ | — | — | — | ✅ | ✅ |
<!-- FEATURE_MATRIX_END -->

---

## Categories

Portals in this catalog are tagged (see the `tags` field in `data/portals.json`) with one or more of:

| Tag | Meaning |
|---|---|
| `GWAS` | Hosts or links to genome-wide association summary statistics |
| `PheWAS` | Supports phenome-wide (variant → many phenotypes) lookups |
| `Biobank` | Is (or is backed by) a population/health-system biobank |
| `Rare Variant` | Includes rare-variant association results |
| `CNV` | Includes copy-number-variant data |
| `WES` | Built on whole-exome sequencing data |
| `WGS` | Built on whole-genome sequencing data |
| `Burden Test` | Supports gene-level collapsing/burden association tests |
| `eQTL` / `pQTL` | Expression or protein quantitative trait loci |
| `Multi-omics` | Integrates more than one -omics layer |
| `Drug Discovery` | Oriented toward target identification/validation |
| `Imaging` | Includes imaging-derived phenotypes |
| `Public API` | Offers a documented, machine-queryable API |
| `Index` | A meta-resource that indexes/links to other portals rather than hosting primary data itself |

Use these tags to filter `data/portals.json`, e.g.:

```bash
jq '.[] | select(.tags | contains("Public API")) | {name, url}' data/portals.json
```

## Search tips

1. **Start broad, then narrow by access model.** If you just want to eyeball an association, prefer fully open portals (GWAS Catalog, Open Targets, FinnGen PheWeb, BioBank Japan PheWeb, AZ PheWAS, Genebass) before applying for controlled-access data (dbGaP, UK Biobank RAP, national biobank committees).
2. **Gene vs. variant vs. region queries are not interchangeable.** PheWeb-family portals (FinnGen, BBJ, CARTaGENE, FinMetSeq) support gene, variant, *and* region search; some knowledge portals (Risteys, LAVAA) are phenotype/variant-centric only. Check the `query_*` columns before assuming a search type is supported.
3. **For rare-variant/gene-burden questions**, go directly to the AZ PheWAS Portal, Genebass, or the burden-test datasource in Open Targets Platform rather than a standard GWAS browser — common-variant PheWebs generally will not have collapsing-analysis results.
4. **For drug-target prioritization**, Open Targets Platform and the HuGeAMP family (T2DKP/CVDKP) are purpose-built for genetics → target → tractability workflows; a plain PheWeb is not.
5. **Cross-check summary statistics across resources.** The same GWAS is often deposited in more than one place (e.g., a UK Biobank trait may appear in Pan-UKB, the GWAS Catalog, and OpenGWAS with different QC/formatting) — compare sample sizes and release dates rather than assuming any single source is canonical.
6. **Mind ancestry composition.** Many of the largest legacy resources (Neale Lab UKB round 1/2, early GWAS Catalog entries) are European-ancestry-only; if ancestry diversity matters for your question, prefer Pan-UKB, MVP, GBMI, or biobank-specific multi-ancestry releases.
7. **Watch release versioning.** FinnGen alone has had 13+ data freezes with distinct public PheWebs (`r5.finngen.fi` ... `r13.finngen.fi`); always record which release/version you queried for reproducibility.

---

## Repository structure

```
.
├── README.md                    # you are here
├── data/
│   ├── portals.csv              # canonical machine-readable database (flat)
│   ├── portals.json             # canonical machine-readable database (structured, same content)
│   └── link_status.json         # generated by scripts/validate_links.py (CI-refreshed)
├── docs/
│   ├── _portal_table.md         # generated table fragment (spliced into README)
│   ├── _feature_matrix.md       # generated matrix fragment (spliced into README)
│   ├── SCOPE.md                 # exact public-access inclusion rule + notable exclusions
│   └── SCHEMA.md                # field-by-field description of the database schema
├── scripts/
│   ├── build_database.py        # source of truth: curated Python list -> CSV/JSON
│   ├── generate_tables.py       # CSV/JSON -> Markdown table fragments
│   ├── update_readme.py         # splices fragments into README.md, updates badges/date
│   └── validate_links.py        # HTTP-checks every portal URL, writes link_status.json
├── .github/workflows/
│   ├── check-links.yml          # scheduled + PR link-health CI
│   └── update-metadata.yml      # scheduled regeneration of tables/README
├── CONTRIBUTING.md
└── LICENSE
```

## Keeping this catalog current

This repo is deliberately built around **one source of truth** (`scripts/build_database.py`, which generates `data/portals.csv` and `data/portals.json`) so the CSV, JSON, and README tables never drift apart:

```bash
# 1. Edit the PORTALS list in scripts/build_database.py (add/update a portal)
python3 scripts/build_database.py        # regenerates data/portals.csv + data/portals.json

# 2. Regenerate the Markdown fragments and splice them into README.md
python3 scripts/generate_tables.py
python3 scripts/update_readme.py

# 3. Check that no URLs are broken
python3 scripts/validate_links.py --fail-on-broken
```

Two GitHub Actions automate the maintenance burden:

- **`check-links.yml`** — runs weekly (and on every PR touching `data/`), reports broken/unreachable portal URLs as a workflow annotation and updates `data/link_status.json`.
- **`update-metadata.yml`** — runs monthly, regenerates the README tables from `data/portals.json` and opens a PR if anything changed (catches manual edits to `portals.json`/`portals.csv` that weren't run through `build_database.py`).

## Contributing

New portals, corrected metadata, and dead-link reports are all welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full guide. In short:

1. Add or edit an entry in the `PORTALS` list in `scripts/build_database.py` (this is the single source of truth — please don't hand-edit `portals.csv`/`portals.json` directly, as they get overwritten by the build script).
2. Run `python3 scripts/build_database.py && python3 scripts/generate_tables.py && python3 scripts/update_readme.py`.
3. Run `python3 scripts/validate_links.py` and confirm your new URL resolves.
4. Open a PR. Please cite the portal's own "about"/documentation page for any non-obvious metadata (sample size, ancestry, license) in the PR description.

## Citation

If this catalog is useful in your work, please cite the repository:

```
GWAS/PheWAS/Biobank Portal Catalog Contributors. (2026).
GWAS / PheWAS / Biobank Portal Catalog [Software/Data set].
GitHub. https://github.com/bahlolab/GWAS-PheWAS-Biobank-Portal
```

A `CITATION.cff` file is included for GitHub's built-in "Cite this repository" feature.

Please also cite the **original portal and its underlying publication(s)** (linked in each entry's `documentation` field) whenever you actually use data retrieved from that portal — this catalog is an index, not a substitute for citing primary sources.

## License

- **Code** (scripts, workflows) in this repository is released under the [MIT License](LICENSE).
- **Curated metadata** in `data/portals.csv` / `data/portals.json` is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — attribution to this repository is appreciated when reused.
- This repository does **not** redistribute any portal's underlying genetic data. Each portal retains its own license/access terms, summarized (to the best of contributors' knowledge) in the `license` field of each entry — always confirm current terms on the portal's own site before use.

## Disclaimer

This is a **community-maintained index**, not an official product of any biobank, consortium, or institution named herein. Metadata (sample sizes, release versions, feature availability) changes frequently and may be out of date despite the automated link/metadata checks — always verify critical details (especially access restrictions and current data-freeze version) directly on the source portal before relying on them for a publication or analysis plan. Corrections via PR or issue are very welcome.
