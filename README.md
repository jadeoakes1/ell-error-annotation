# Error Annotation for English Language Learning

This project developed a linguistic annotation scheme for identifying English learner writing errors and mapping error patterns to broad CEFR-aligned proficiency levels.

The project focused on written English learner data from L1 Spanish speakers and was designed to support research in English language learning, proficiency estimation, and automated grammatical error analysis.

## Project Goals

- Design an annotation schema for grammatical and lexical errors in English learner writing
- Map observed error patterns to proficiency levels: Basic, Intermediate, and Advanced
- Create clear annotation guidelines to improve consistency across annotators
- Develop a weighted error scoring system for estimating proficiency from error type and frequency
- Coordinate annotation workflow, data splits, and documentation

## Annotation Categories

The schema includes error labels such as:

- Preposition errors
- Article errors
- Pronoun case errors
- Subject-verb agreement errors
- Verb tense errors
- Subject or expletive omission errors
- Subject-verb order errors
- Nominalization errors
- Number agreement errors
- Other grammatical or lexical errors

Spelling, punctuation, and capitalization errors were treated as pre-annotated or lower-priority categories so annotators could focus on grammar and word choice.

## Proficiency Scoring

The project used a weighted error scoring system where more severe errors contributed more heavily to proficiency estimation. Error density was calculated based on weighted error counts relative to text length, then mapped to broad proficiency levels.

## My Contributions

- Led project design and annotation workflow
- Developed the annotation schema, label hierarchy, and guidelines
- Created a weighted scoring method for proficiency estimation
- Preprocessed and curated learner corpus data
- Created balanced subsets and annotator-specific data splits
- Managed documentation, revision tracking, and team coordination

## Repository Contents

- `annotation_scheme/`: Final annotation guidelines and revision notes
- `docs/`: Project summaries and design notes
- `examples/`: Small illustrative examples of the annotation schema

## Tools & Methods

- Label Studio
- Linguistic annotation
- Error analysis
- CEFR-aligned proficiency classification
- Dataset curation
- Annotation guideline design

## Note on Data

The original learner corpus data is not included in this repository due to licensing restrictions. This repository contains project documentation, annotation design materials, and illustrative examples only.
