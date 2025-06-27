# CyberGuard API

## Description
CyberGuard API is a RESTful backend system that leverages AI agents to detect cybersecurity threats in real-time by analyzing network traffic and system logs. It is powered by:
- Hugging Face transformers for anomaly detection
- Apache Kafka for real-time stream processing
- MongoDB for data storage
- Twilio for alerting via SMS or email

Built in response to Kenya’s 300% surge in cybercrime, CyberGuard helps Nairobi-based tech hubs, startups, and SMEs secure their infrastructure. The API provides secure JWT-based authentication, supports log ingestion, detects anomalies, and gives admins access to analytics.

## Installation

1. **Clone the repository:**

git clone https://github.com/kale-francis/CyberGuard_API.git
cd CyberGuard_API

2. **Install backend dependencies:**


npm install

3. **Configure environment variables :**

cp .env.example .env

Then update .env with:

MONGO_URI

JWT_SECRET

HUGGINGFACE_API_KEY

TWILIO_SID

TWILIO_TOKEN

TWILIO_PHONE

KAFKA_BROKERS

4. **Install local services:**

MongoDB: https://www.mongodb.com/docs/manual/installation/

Apache Kafka: https://kafka.apache.org/quickstart

5.**Start the server:**

npm start

# Usage
# Start server

npm start

# Authenticate (Login) :

curl -X POST http://localhost:3000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"your_password"}'

# Ingest Logs :

curl -X POST http://localhost:3000/logs \
  -H "Authorization: Bearer <your_jwt>" \
  -H "Content-Type: application/json" \
  -d '{"ip":"192.168.1.1","port":80,"protocol":"TCP","timestamp":"2025-06-27T15:00:00Z"}'

# View Anomalies : 

curl -X GET http://localhost:3000/anomalies \
  -H "Authorization: Bearer <your_jwt>"

# API Documentation :

Visit: http://localhost:3000/docs (Swagger UI coming soon)

# Technologies Used :

Node.js/Express – RESTful API framework

MongoDB – NoSQL database for logs, anomalies, and users

Apache Kafka – Real-time message streaming and log processing

Hugging Face Transformers – Inference API for AI-based anomaly detection

Twilio – SMS/Email alerts for detected threats

JWT & bcrypt – Authentication and password hashing

Jest & Supertest – Unit and integration testing

Swagger – API documentation (planned)

Heroku – Optional deployment target

# Resources :

Node.js Docs

Express.js Guide

MongoDB Documentation

Kafka Quickstart

Hugging Face Inference API

Twilio SMS API

UNSW-NB15 Dataset

Jest Docs

Swagger