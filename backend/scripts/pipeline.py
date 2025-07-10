# Data pipeline for CyberGuard API

import pandas as pd
from kafka import KafkaProducer
import pymongo
import json

def run_pipeline(input_file, kafka_topic, mongo_db, mongo_collection):
    """
    Load preprocessed data, send to Kafka, and store in MongoDB.
    Args:
        input_file (str): Path to preprocessed CSV (e.g., 'backend/data/preprocessed/train.csv')
        kafka_topic (str): Kafka topic name (e.g., 'logs')
        mongo_db (str): MongoDB database name (e.g., 'cybergard')
        mongo_collection (str): MongoDB collection name (e.g., 'logs')
    """
    # Load preprocessed CSV
    df = pd.read_csv(input_file)
    print(f"Loaded {input_file} with {len(df)} rows")

    # Initialize Kafka producer
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                            value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    # Send each row to Kafka
    for _, row in df.iterrows():
        producer.send(kafka_topic, row.to_dict())
    producer.flush()
    print(f"Sent {len(df)} records to Kafka topic {kafka_topic}")

    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[mongo_db]
    collection = db[mongo_collection]
    # Insert records
    records = df.to_dict('records')
    collection.insert_many(records)
    print(f"Inserted {len(records)} records into MongoDB {mongo_db}.{mongo_collection}")

if __name__ == "__main__":
    # Define inputs
    input_file = "backend/data/preprocessed/train.csv"
    kafka_topic = "logs"
    mongo_db = "cybergard"
    mongo_collection = "logs"

    # Run pipeline
    run_pipeline(input_file, kafka_topic, mongo_db, mongo_collection)
    print("Pipeline completed")