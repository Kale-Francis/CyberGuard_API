""" Import required libraries """

import panda as pd 
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
import torch
from kafka import KafkaConsumer
import pymongo
from fastapi import FastApi
from datasets import dataset

""" Function to load and train the transformer."""

def train_model(train_file, test_file):
    """ 
    Holds trainig logic: 
    train_file(str) = "backend/data/preprocessed/train.csv"
    test_file(str) = "backend/data/preprocessed/test.csv"  
    """

    #Load preprocessed Data 
    train_df = pd.read_csv(train_file)
    test_df = pd.read_csv(test_file)

    #Prepare features and labels
    train_df.drop('label', axis=1)
    test_df.drop('label', axis=1)
    train_df['label']    
    test_df['label']

    #Convert to HuggingFace Dataset
    Dataset.from_pandas(train_df)
    Dataset.from_pandas(test_df)

    #Confirm Data Loading
    len(train_df)
    len(test_df)
    print(f"Loaded train with{rows}rows, test with{rows}rows.")

    #Load Pretrained MOdel and Tokenizer
    AutoTokenizer.from_pretrained("bert-base-uncased")
    AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
    
    #Tokenize Data
    train_df.drop('label', axis=1).to_string()
    test_df.drop('label', axis=1).to_string()
    tokenizer(text, padding=True, truncation=True, return_tensors="pt")

    #Set Training Arguments
    TrainingArguments(output_dir="backend/models",num_train_epochs=3,per_device_train_batch_size=8, per_device_eval_batch_size=8)

    #Train the model
    Trainer(model=model, args=training_args,train_dataset=train_dataset, eval_dataset=test_dataset)
    triner.train()
    
    #Confirm training
    print("Model training complete, saved to backend/models")




if __name__ == "__main__":
    train_file = "backend/data/preprocessed/train.csv"
    test_file = "backend/data/preprocessed/test.csv" 
    train_model(train_file, test_file)