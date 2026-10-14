# Reproducing and checking the project

## Verify the archive

From the repository root:

```bash
python src/verify_project.py
```

This checks the size and SHA-256 of each file in `docs/file_manifest.csv`, confirms that directory names are ASCII, and reports missing or modified files.

## Recount keywords

```bash
python src/recount_keywords.py
```

The script reads `data/processed/questionnaire_answer_corpus_zh.txt` and the term mapping in `figures/wordclouds/Word_Cloud_Data.csv`. It writes `build/recounted_wordcloud_frequencies.csv` and checks the published word-cloud counts. This is a literal substring count, matching the original analysis.

## Document and presentation sources

`src/legacy/` preserves the production history, including manuscript polishing, layout generation, document creation, and PowerPoint exports. These scripts originally ran on Windows with Microsoft Word, PowerPoint, local fonts, and the Codex presentation runtime. They are archived source code, not a portable one-command build.

Machine-specific paths have been replaced with named placeholders. Before reusing a historical script, configure paths and dependencies for the local environment. `requirements.txt` lists the main Python document and plotting libraries; the proprietary presentation runtime is not included.

The final editable Word document and PowerPoint are included directly in `outputs/`, so reviewing or editing the deliverables does not require rebuilding them.

## Repository publication

Create a private GitHub repository named `kuzhi-yucai-campus-research`, then push the project directory:

```bash
git remote add origin https://github.com/YOUR_ACCOUNT/kuzhi-yucai-campus-research.git
git push -u origin main
```

Use your normal GitHub authentication. Do not place access tokens in project files.
