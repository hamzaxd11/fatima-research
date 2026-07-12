# Manuscript Submission Plan

## Purpose

This document records the scientific and editorial revision plan used to correct the analysis package and prepare a transparent manuscript.

## Audit Findings

The manuscript and supporting artifacts were reviewed against the final source bundle:

- `../../output/analysis_20260712_224950/`
- `../analysis/ANALYSIS_METHODOLOGY.md`
- `../analysis/DATA_ANALYSIS_SUMMARY.md`
- `../../doc.md`
- verified journal metadata and DOI records

The review identified six high-priority issues.

First, the maternal education labels used in the manuscript and in some generated outputs were not aligned with the original SPSS value labels. The source file codes maternal education as Illiterate, Primary, Middle, Secondary, and Intermediate and above. The manuscript had instead used shifted labels such as Illiterate/Primary and Higher. This was the most important interpretation risk because it affected the naming of the primary exposure variable.

Second, the paper still contained report-style bullet lists in sections that should be written as flowing scientific prose. This reduced journal readiness and did not meet standard manuscript conventions.

Third, the methods section underused protocol information available in `doc.md`, particularly the school setting, study period, sampling approach, consent framework, questionnaire administration approach, and interview duration.

Fourth, the reference list required verification against real-world sources. DOI-bearing references needed exact metadata confirmation, and non-DOI references needed stable official URLs.

Fifth, the manuscript figures embedded from the analysis output folder inherited the outdated education labels. New manuscript-ready figures were therefore needed without overwriting the preserved original output bundle.

Sixth, the manuscript still required a final submission QA pass for typography, internal consistency, and traceability back to the analysis outputs.

## Revision Plan

The revision plan consisted of the following steps.

### 1. Protect the analytical record

The final manuscript should reference the corrected output bundle in `../../output/analysis_20260712_224950/`. Superseded output bundles were removed after verification.

### 2. Correct exposure labeling everywhere relevant

Update maternal education labels to match the original SPSS coding:

- 1 = Illiterate
- 2 = Primary
- 3 = Middle
- 4 = Secondary
- 5 = Intermediate and above

Apply the correction to the manuscript text, manuscript tables, manuscript figure labels, and any code responsible for future label rendering.

### 3. Rewrite the paper into full manuscript prose

Remove report-style bullets from the final paper except where unavoidable in references and table structures. Rewrite abstract, methods, results, discussion, and conclusion as paragraph-based scientific prose following IMRAD expectations.

### 4. Strengthen methods reporting

Integrate protocol details available in `../../doc.md`, including setting, study timeframe, sampling description, questionnaire administration, and interview procedure. Where the protocol bundle lacks an ethics approval identifier, state this cautiously and transparently rather than fabricating one.

### 5. Standardize references

Verify all DOI-bearing references through Crossref. Use canonical DOI links in the format `https://doi.org/...`. For institutional sources without DOIs, use stable official URLs and add access dates.

### 6. Generate manuscript-specific figures

Create corrected figures for manuscript use in a separate folder so that original outputs remain preserved. Update the manuscript to use the corrected figure paths.

### 7. Regenerate the final DOCX

Rebuild `RESEARCH_PAPER.docx` from the revised Markdown manuscript after all scientific and formatting corrections are complete.

### 8. Run final QA

Before considering the paper submission-ready, verify the following:

- all key numbers match the final output bundle;
- all figure labels and table labels are correct;
- all references are real and formatted consistently;
- the Word document uses submission-appropriate typography and layout;
- no unsupported methodological or ethical claims are made.

## Remaining Submission-Critical Items

Three items require author confirmation or documentation before journal submission.

The first is evidence that ethics approval and menstrual-hygiene-specific parental consent were obtained. The archived protocol contains planned procedures but no approval record, and its appended consent text concerns bullying.

The second is author acceptance of the adjudicated menstruation-process scoring correction and its protocol-deviation disclosure.

The third is target-journal formatting, including title-page affiliations, running title, corresponding author details, abstract word limits, and any journal-specific declaration language.

## Deliverables

The final deliverables for this revision cycle are:

- `../../RESEARCH_PAPER_RAW.md`
- `../../RESEARCH_PAPER.docx`
- `REFERENCES_VERIFICATION.md`
- manuscript-specific corrected figures
