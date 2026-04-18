# Movie Recommendation Hackathon 2026

This repository contains the workflow for a Kaggle recommender-systems project based on the Movie Recommendation Hackathon 2026 competition.

Competition page:
https://www.kaggle.com/competitions/movie-recommendation-hackathon-2026/overview

## Project Goal

Build and evaluate movie recommendation models, organize experimentation cleanly, and generate Kaggle-ready submission files.

## Challenge Overview

The competition focuses on predicting movie ratings for user-movie pairs. Recommender systems are central to content platforms because they help users discover relevant items from large catalogs. In this project, the task is to learn user preferences from historical interactions and predict ratings for unseen user-movie combinations.

## Project Structure

```text
data/
  raw/          Original downloaded files
  interim/      Intermediate datasets created during cleaning
  processed/    Final feature tables and model-ready datasets
  external/     External datasets or metadata
notebooks/      Exploration and experiment notebooks
src/
  data/         Data loading and preprocessing code
  features/     Feature engineering logic
  models/       Training, validation, and inference code
  utils/        Shared utilities
  visualization/Plots and reporting helpers
configs/        Configuration files for experiments
models/         Saved model artifacts
reports/        Analysis outputs and figures
references/     Notes, competition rules, and supporting material
scripts/        Reusable command-line scripts
submissions/    Kaggle submission files
tests/          Unit and integration tests
```

## Suggested Workflow

1. Download the competition data and place the original zip files or extracted files in `data/raw/`.
2. Use notebooks for quick exploration and move reusable logic into `src/`.
3. Save cleaned or transformed datasets in `data/interim/` and `data/processed/`.
4. Store trained model artifacts in `models/`.
5. Write Kaggle submission files to `submissions/`.

## Current Dataset Snapshot

The competition files currently available in the workspace include:

- `train.csv` with columns `userId`, `movieId`, `rating`, `timestamp`
- `test.csv` with columns `userId`, `movieId`
- `sample_submission.csv` with columns `Id`, `rating`
- Supporting metadata files such as `movies.csv`, `links.csv`, `imdb_data.csv`, `genome_tags.csv`, `genome_scores.csv`, and `tags.csv`

Observed submission key format:

```text
Id,rating
1_2011,1.0
1_4144,1.0
```

## Competition Notes

The competition overview is linked above. The public page content was not fully accessible from the current environment, so this README intentionally avoids inventing details that should come directly from Kaggle.

Recommended additions after reviewing the competition page:

- Objective and prediction target
- Evaluation metric
- Submission file columns and format
- Team rules and timeline

## Getting Started

Create and activate a Python environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Initial Focus Areas

- Inspect the training and test data schema
- Build a simple popularity-based baseline
- Add a collaborative filtering baseline
- Define a local validation strategy that mirrors the Kaggle metric
- Track experiments and keep submissions reproducible

## Immediate Next Steps

- Move the extracted competition dataset into `data/raw/` when you are ready to normalize the layout
- Run the dataset inspection script to confirm row counts and missing values
- Build a first baseline model before adding richer metadata features

## Process Implemented (Up To Predictions)

The current notebook workflow in `notebooks/Movie Recommendation Project 2026.ipynb` now covers the full path from exploration to large-scale collaborative-filtering predictions.

### 1. Data Loading and Validation

- Loaded core competition files (`train.csv`, `test.csv`, `movies.csv`, `imdb_data.csv`, `genome_tags.csv`, `genome_scores.csv`) using robust path checks.
- Printed dataset shapes early to verify successful reads and avoid path-related runtime issues.

### 2. Exploratory Data Analysis (EDA)

- Analyzed movie catalog size and genre structure.
- Measured genre-count distribution per movie and plotted summary visuals.
- Reviewed train-set rating distribution and average rating behavior.

### 3. User-Based Collaborative Filtering Setup

- Merged movie titles into the train interactions for interpretability.
- Built a memory-efficient sparse user-item matrix with `scipy.sparse.csr_matrix`.
- Encoded users/movies via factorization and reduced memory pressure with compact dtypes.
- Mean-centered user ratings and trained a cosine-similarity nearest-neighbors model (`NearestNeighbors`, brute-force).

### 4. Prediction Functions

- Implemented reusable helper functions for:
  - neighbor retrieval with similarity caching,
  - weighted user-neighbor rating prediction per `(userId, movieId)` pair,
  - safe fallback to global mean for cold-start cases or weak neighbor signal.
- Clipped predictions to the rating bounds `[0.5, 5.0]`.

### 5. Scalable Test-Set Scoring and Resume Logic

- Scored `test_df` in chunks to handle very large inference volume safely.
- Saved per-chunk checkpoints in `submissions/user_cf_checkpoints/`.
- Added resume support so interrupted runs can continue from missing chunks.
- Recombined all chunk outputs deterministically and wrote the final Kaggle-format file (`Id`, `rating`).

## Collaborative Filtering Submission Result

Final file generated:

`submissions/user_cf_submission.csv`

### Submission Summary Report

- Total prediction rows: 5,800,019
- Total users: 162,350
- Total movies: 39,643
- Average recommendation by user: 3.5740
- Average recommendation by movie: 3.4798
- Highest recommendation: 4.9998
- Lowest recommendation: 0.5000

This confirms the full collaborative-filtering prediction pipeline completed successfully at competition scale.

## Reproducible Runbook

Use this checklist to reproduce the same submission process end to end.

### 1. Environment Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If your environment is Conda-based, you can alternatively run:

```powershell
conda env create -f environment.yml
conda activate <env-name>
```

### 2. Data Placement

Ensure competition files are present in:

```text
data/movie-recommendation-hackathon-2026/
```

Required files used by the notebook:

- `train.csv`
- `test.csv`
- `movies.csv`
- `imdb_data.csv`
- `genome_tags.csv`
- `genome_scores.csv`

### 3. Run Notebook In Order

Open `notebooks/Movie Recommendation Project 2026.ipynb` and run cells sequentially from top to bottom.

Critical stages to run in order:

1. Package imports and dataset loading.
2. EDA and rating/genre summaries.
3. Sparse user-item matrix creation.
4. User-similarity model training (`NearestNeighbors`).
5. CF prediction helper functions.
6. Chunked scoring cell with checkpoint resume support.

### 4. Resume-Safe Chunked Inference

The scoring cell writes partial outputs to:

- `submissions/user_cf_checkpoints/`

If a run is interrupted, rerun the same scoring cell. It skips completed chunks and continues missing ones.

### 5. Final Submission Artifact

After all chunks are available, the notebook combines checkpoints and writes:

- `submissions/user_cf_submission.csv`

Expected output schema:

```text
Id,rating
```

Where:

- `Id = userId_movieId`
- `rating` is clipped to `[0.5, 5.0]`

### 6. Sanity Checks

Before uploading to Kaggle, verify:

1. File exists at `submissions/user_cf_submission.csv`.
2. Header is exactly `Id,rating`.
3. Row count matches test rows (5,800,019 in the current run).
4. Ratings are within `[0.5, 5.0]`.

You can run all checks automatically:

```powershell
python scripts/validate_submission.py --file submissions/user_cf_submission.csv --expected-rows 5800019
```

The validator checks:

- exact columns (`Id`, `rating`)
- row count (when provided)
- missing or non-numeric ratings
- rating bounds (`0.5` to `5.0`, configurable)
- duplicate `Id` values

### 7. Current Reproduced Result (Reference)

- Output file: `submissions/user_cf_submission.csv`
- Submission shape: `(5800019, 2)`
- Total users: `162,350`
- Total movies: `39,643`
- Average recommendation by user: `3.5740`
- Average recommendation by movie: `3.4798`
- Highest recommendation: `4.9998`
- Lowest recommendation: `0.5000`