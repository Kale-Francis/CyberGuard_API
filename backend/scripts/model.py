import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset
import torch

def train_model(train_file, test_file):
    """
    Train a Hugging Face transformer model for anomaly detection.
    Args:
        train_file (str): Path to preprocessed training CSV (e.g., 'backend/data/preprocessed/train.csv')
        test_file (str): Path to preprocessed test CSV (e.g., 'backend/data/preprocessed/test.csv')
    """
    # Load preprocessed data
    print("Loading data...")
    train_df = pd.read_csv(train_file).head(1000)
    test_df = pd.read_csv(test_file).head(500)

    # Prepare features and labels
    X_train = train_df.drop('label', axis=1)
    y_train = train_df['label']
    X_test = test_df.drop('label', axis=1)
    y_test = test_df['label']

    # Convert to Hugging Face Dataset
    train_dataset = Dataset.from_pandas(train_df)
    test_dataset = Dataset.from_pandas(test_df)

    # Confirm data loading
    print(f"Loaded train with {len(train_df)} rows, test with {len(test_df)} rows")

    # Load pretrained model and tokenizer
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    # Function to convert numerical features to text for tokenization
    def features_to_text(example):
        features = {k: v for k, v in example.items() if k != 'label'}
        text = " ".join([f"{key}:{value}" for key, value in features.items()])
        return {"text": text}

    # Apply feature conversion
    train_dataset = train_dataset.map(features_to_text)
    test_dataset = test_dataset.map(features_to_text)

    # Tokenize data
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", max_length=128, truncation=True, return_tensors="pt")

    train_dataset = train_dataset.map(tokenize_function, batched=True)
    test_dataset = test_dataset.map(tokenize_function, batched=True)

    # Set format for training
    train_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])
    test_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])

    # Set training arguments
    training_args = TrainingArguments(
        output_dir="backend/models",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_dir="backend/models/logs",
        logging_steps=100,
        load_best_model_at_end=True
    )

    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset
    )

    # Train the model
    print("Training model...")
    trainer.train()

    # Evaluate the model
    print("Evaluating model...")
    eval_results = trainer.evaluate()
    print(f"Evaluation results: {eval_results}")

    # Save the model
    model.save_pretrained("backend/models")
    tokenizer.save_pretrained("backend/models")
    print("Model training complete, saved to backend/models")

if __name__ == "__main__":
    train_file = "backend/data/preprocessed/train.csv"
    test_file = "backend/data/preprocessed/test.csv"
    train_model(train_file, test_file)