# Data guide

## Original sources

| Directory | Contents |
| --- | --- |
| `raw/questionnaires/` | Original Word questionnaire and environmental audit |
| `raw/audio/` | Three original interview recordings |
| `raw/photos/` | Original site photographs extracted from the submitted archive |
| `raw/geospatial/` | KML field route and ArcGIS map package |
| `raw/architecture/` | Campus masterplan and architectural plans, elevations, sections |
| `raw/references/` | Display reference and supplied visual references |

## Processed tables

| File in `data/processed/` | Interpretation |
| --- | --- |
| `questionnaire_responses.csv` | Written answers by topic and response code |
| `questionnaire_answer_corpus_zh.txt` | Answer text used for literal keyword counting |
| `keyword_frequencies.csv` | Selected Chinese terms and occurrence counts; other columns preserve the original analysis |
| `token_frequencies.csv` | Tokenizer output, distinct from literal selected-term counts |
| `questionnaire_theme_comparison.csv` | Thematic comparison of questionnaire feedback |
| `environmental_audit_items.csv` | All 35 audit questions with recorded scores |
| `environmental_audit_domains.csv` | Domain grouping and descriptive summary |
| `environmental_audit_en.csv` | English version of the environmental items |
| `activity_observations.csv` | Observed use of places at particular times |
| `timetable_intervals.csv` | Timetable entries and duration calculations |
| `timetable_categories.csv` | Minutes grouped by activity category |
| `interview_theme_index.csv` | Interview topics and transcript locations |
| `audio_inventory.csv` | Recording inventory |
| `photo_inventory.csv` | Photograph inventory |
| `gis_metrics.json` and `gis_site_metrics.json` | Site measurements and geographic attributes |
| `manuscript_bilingual.json` | Structured bilingual manuscript before the final SCI-style Word reorganization |
| `reference_metadata.json` | Stored bibliographic metadata |

CSV files retain the original Chinese column names where applicable. Read them using UTF-8 with optional BOM (`utf-8-sig`). Original source filenames are preserved inside source metadata. Historical local paths are replaced with `${ORIGINAL_WORKSPACE}` or `${ORIGINAL_USER_HOME}`.

## Interpretation

- Word frequency is a count of occurrences in written answers. English cloud labels are translations, not a second independently counted corpus.
- Selected terms can overlap. For example, the substring activity can occur inside volunteering in Chinese. Counts are not additive theme totals.
- Environmental scores follow the wording of individual items. Negatively phrased questions require their original wording when interpreting scores.
- The school timetable spans 870 minutes. Study accounts for 390 minutes; the other groups are meals, activity, midday rest, eye exercises, and intervals.
- Interview transcripts and their JSON time segments are retained alongside the original audio.
- `data/geospatial/layers/` contains shapefile companion files. Keep files with the same basename together.
- `data/layouts/portfolio_en.json` uses repository-relative image paths under `assets/presentation/`.

## Versions

The current English paper reorganizes the earlier manuscript into a journal-style structure and adds word-cloud methodology and figure references. Companion files are preserved without being silently treated as the current English edition.
