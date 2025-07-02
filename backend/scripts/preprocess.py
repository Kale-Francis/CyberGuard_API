# Preprocess UNSW-NB15 dataset for CyberGuard API

import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

def preprocess_data(input_file, output_file):
    """
    Preprocess UNSW-NB15 dataset: load, clean, encode, normalize, and save.
    Args:
        input_file (str): Path to input CSV (e.g., 'backend/data/UNSW_NB15_training-set.csv')
        output_file (str): Path to save processed CSV (e.g., 'backend/data/preprocessed/train.csv')
    """
    # Load CSV file
    df = pd.read_csv(input_file)
    print(f"Loaded {input_file} with {len(df)} rows and {len(df.columns)} columns")

    # Handle missing values
    print("Missing values:", df.isnull().sum())
    df = df.dropna()
    print(f"After dropping missing values, {len(df)} rows remain")

    # Encode categorical columns
    categorical_columns = ['proto', 'service', 'state']
    df = pd.get_dummies(df, columns=categorical_columns, prefix=categorical_columns)
    print(f"After encoding, dataset has {len(df.columns)} columns")

    # Normalize numerical columns
    numerical_columns = ['dur', 'spkts', 'dpkts', 'sbytes', 'dbytes']
    scaler = StandardScaler()
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
    print("Numerical columns normalized")

    # Save preprocessed data
    df.to_csv(output_file, index=False)
    print(f"Saved preprocessed data to {output_file}")

if __name__ == "__main__":
    # Define file paths
    train_input = "backend/data/UNSW_NB15_training-set.csv"
    train_output = "backend/data/preprocessed/train.csv"
    test_input = "backend/data/UNSW_NB15_testing-set.csv"
    test_output = "backend/data/preprocessed/test.csv"

    # Create output directory if it doesn't exist
    os.makedirs("backend/data/preprocessed", exist_ok=True)

    # Preprocess training and testing datasets
    preprocess_data(train_input, train_output)
    preprocess_data(test_input, test_output)
    print("Preprocessing complete. Files saved to backend/data/preprocessed/")