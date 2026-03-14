# Biohacking & Health Data API Catalog

A curated reference of data sources for the biohacking platform. For each source, check current availability and terms before building a pipeline — APIs change frequently.

## Table of Contents
1. [Supplement & Compound Data](#supplement--compound-data)
2. [Biomedical Research](#biomedical-research)
3. [Lab & Biomarker Data](#lab--biomarker-data)
4. [Nutrition & Food Data](#nutrition--food-data)
5. [Wearable & Device Data](#wearable--device-data)
6. [Drug Interaction Data](#drug-interaction-data)

---

## Supplement & Compound Data

### PubChem API (NIH)
- **URL:** https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
- **What it has:** Chemical compound data, bioactivity, safety data, molecular structures
- **Access:** Free, no API key required
- **Rate limit:** 5 requests/second
- **Format:** JSON, XML, CSV
- **Best for:** Compound-level data (what's in supplements at a molecular level)

### Open Targets Platform
- **URL:** https://platform.opentargets.org/
- **What it has:** Drug-target associations, disease associations, evidence from literature
- **Access:** Free, GraphQL API
- **Best for:** Understanding what compounds affect which biological targets

### Examine.com
- **URL:** Check their current API/data access options
- **What it has:** Supplement summaries, human effect matrices, dosage recommendations, research summaries
- **Access:** May require paid subscription for API access
- **Best for:** Human-readable supplement efficacy data with evidence ratings

### Natural Medicines Database (TRC)
- **URL:** https://naturalmedicines.therapeuticresearch.com/
- **What it has:** Comprehensive supplement monographs, safety ratings, effectiveness ratings, interactions
- **Access:** Paid subscription, check for API availability
- **Best for:** Clinical-grade supplement safety and efficacy data

## Biomedical Research

### PubMed / NCBI E-utilities
- **URL:** https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **What it has:** 35M+ biomedical citations, abstracts, full-text links
- **Access:** Free, API key recommended (increases rate limit)
- **Rate limit:** 3/sec without key, 10/sec with key
- **Best for:** Research evidence for supplement/protocol claims

### Semantic Scholar API
- **URL:** https://api.semanticscholar.org/
- **What it has:** Academic paper search, citation graphs, paper summaries
- **Access:** Free tier available, API key for higher limits
- **Best for:** Finding and analyzing research papers programmatically

### ClinicalTrials.gov API
- **URL:** https://clinicaltrials.gov/api/
- **What it has:** Clinical trial data, results, conditions studied
- **Access:** Free
- **Best for:** Evidence of supplement/compound efficacy from clinical trials

## Lab & Biomarker Data

### LOINC (Logical Observation Identifiers)
- **URL:** https://loinc.org/
- **What it has:** Universal coding system for lab tests and biomarkers
- **Access:** Free with registration
- **Best for:** Standardizing biomarker identifiers across different lab providers

### HL7 FHIR Resources
- **URL:** https://www.hl7.org/fhir/
- **What it has:** Healthcare data interoperability standard, including lab result formats
- **Access:** Free specification
- **Best for:** Structuring lab result imports in a healthcare-standard format

## Nutrition & Food Data

### USDA FoodData Central API
- **URL:** https://fdc.nal.usda.gov/api-guide.html
- **What it has:** Comprehensive food nutrient data, branded products, foundation foods
- **Access:** Free, API key required
- **Rate limit:** 1000 requests/hour
- **Best for:** Nutritional data for dietary protocol recommendations

### Open Food Facts API
- **URL:** https://world.openfoodfacts.org/data
- **What it has:** Crowdsourced food product data, ingredients, nutrition labels
- **Access:** Free, open data
- **Best for:** Product-level data (what's in specific supplement brands/products)

## Wearable & Device Data

### Oura Ring API
- **URL:** https://cloud.ouraring.com/docs/
- **What it has:** Sleep, readiness, activity, heart rate, HRV, temperature
- **Access:** OAuth2, user-authorized
- **Best for:** Sleep quality and recovery data

### Whoop API
- **URL:** Check current developer access
- **What it has:** Strain, recovery, sleep, HRV
- **Access:** Developer program
- **Best for:** Training load and recovery optimization

### Apple HealthKit (via export)
- **What it has:** Aggregated health data from all Apple Health sources
- **Access:** User exports XML, you parse it
- **Best for:** Comprehensive user health data import

### Google Fit REST API
- **URL:** https://developers.google.com/fit/rest
- **What it has:** Activity, body measurements, nutrition, sleep
- **Access:** OAuth2
- **Best for:** Android user health data

## Drug Interaction Data

### RxNorm API (NIH)
- **URL:** https://rxnav.nlm.nih.gov/RxNormAPIs.html
- **What it has:** Normalized drug names, relationships, NDC codes
- **Access:** Free
- **Best for:** Standardizing drug names for interaction checking

### DrugBank (if accessible)
- **URL:** https://go.drugbank.com/
- **What it has:** Comprehensive drug-drug and drug-supplement interaction data
- **Access:** Academic access may be free, commercial requires license
- **Best for:** Interaction data between supplements and medications

### OpenFDA API
- **URL:** https://open.fda.gov/apis/
- **What it has:** Adverse event reports, drug labels, recalls
- **Access:** Free, API key recommended
- **Best for:** Safety signal detection for supplements and drugs

---

## Integration priority

For building the initial biohacking platform, recommended integration order:

1. **PubChem + USDA FoodData** — free, reliable, foundational compound and nutrition data
2. **PubMed E-utilities** — evidence base for all recommendations
3. **LOINC** — standardize biomarker coding from the start
4. **RxNorm + OpenFDA** — drug interaction safety (critical for responsible recommendations)
5. **Examine.com** — human-friendly supplement data (check current access terms)
6. **Wearable APIs** — add when user health data features are built

Always verify current API terms, availability, and pricing before building a pipeline. This catalog is a starting point — search for updates and new sources regularly.
