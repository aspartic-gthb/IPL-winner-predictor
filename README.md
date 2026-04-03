# 🏏 IPL Match Winner Predictor

A Machine Learning project that predicts IPL match winners using Random Forest.

## Dataset
- [IPL Complete Dataset on Kaggle](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020)
- Download `matches.csv` and place it in the project folder

## How to run
1. Install dependencies
pip install pandas numpy matplotlib seaborn scikit-learn xgboost

2. Open the notebook
jupyter notebook ipl_winner_prediction.ipynb

## What it does
- Loads and cleans IPL match data (2008-2020)
- Encodes team names and venues into numbers
- Trains a Random Forest model
- Predicts match winner given two teams, toss info and venue

## Current Accuracy
~49% (improving with more features)

## Tech Stack
- Python, pandas, scikit-learn, XGBoost, Jupyter Notebook