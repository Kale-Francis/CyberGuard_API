# Preprocess UNSW-NB15 dataset for CyberGuard API
""" Imports for DataFrame, Numerical Handling, Categorial Encoding, File Paths"""
import pandas
import numpy
import sklearn.preprocessing.OneHotEncoder
import sklearn.preprocessing.StandardScaler
import os

""" Function to preprocess input/output paths """
def preprocess_data (input_path, output_path):
    self.input_path = data/UNSW_NB15_training-set.csv
    self.output_path = data/preprocessed/train.csv
# 1. Load CSV files (UNSW_NB15_training-set.csv, UNSW_NB15_testing-set.csv)
""" Load data using pandas and read the files """
    pandas.read_csv(input_path)
# 2. Handle missing values (e.g., drop or impute with mean/median)
# 3. Encode categorical features (e.g., protocol, service) using one-hot encoding
# 4. Normalize numerical features (e.g., bytes, packets) using StandardScaler
# 5. Save preprocessed data to data/preprocessed/