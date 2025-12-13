# CSV Bias & SMOTE Analysis Platform

A full-stack web application that:
- Accepts CSV datasets
- Automatically detects target variables
- Performs bias analysis
- Applies SMOTE for class imbalance
- Generates fairness-weighted datasets
- Returns downloadable output files

## Tech Stack
- Frontend: Next.js + Tailwind CSS
- Backend: FastAPI + Pandas
- ML: Scikit-learn, Imbalanced-learn
- Hosting: Render

## Features
- CSV upload via web UI
- Automated bias detection
- SMOTE-based balancing
- Sample weighting for fairness
- Downloadable processed datasets

## Deployment
- Frontend and backend deployed as separate Render services from the same repository.

## Usage
1. Upload a CSV file
2. System processes dataset
3. Download generated files
