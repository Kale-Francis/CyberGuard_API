const express = require("express");
const { PythonShell } = require("python-shell");
const { Kafka } = require("kafkajs");
const mongoose = require("mongoose");

const app = express();
app.use(express.json());

const port = 3000;

// MongoDB Setup
mongoose.connect("mongodb://localhost:27017/cybergard", { useNewUrlParser: true });
const predictionSchema = new mongoose.Schema({ record: Object, prediction: Number });
const Prediction = mongoose.model("Prediction", predictionSchema);

// Kafka Setup
const kafka = new Kafka({ clientId: "cyberguard", brokers: ["localhost:9092"] });
const consumer = kafka.consumer({ groupId: "cyberguard" });

async function consumeKafka() {
  await consumer.connect();
  await consumer.subscribe({ topic: "logs", fromBeginning: true });
  await consumer.run({
    eachMessage: async ({ message }) => {
      const record = JSON.parse(message.value.toString());
      const options = {
        pythonPath: "backend/venv/bin/python3",
        args: [JSON.stringify(record)]
      };
      PythonShell.run("scripts/inference.py", options, (err, results) => {
        if (err) throw err;
        const prediction = JSON.parse(results[0]).prediction;
        Prediction.create({ record, prediction });
        console.log("Processed:", { record, prediction });
      });
    },
  });
}

consumeKafka().catch(console.error);

// /predict Endpoint
app.post("/predict", async (req, res) => {
  const data = req.body;
  const options = {
    pythonPath: "backend/venv/bin/python3",
    args: [JSON.stringify(data)]
  };
  PythonShell.run("scripts/inference.py", options, (err, results) => {
    if (err) throw err;
    const prediction = JSON.parse(results[0]).prediction;
    res.json({ prediction });
  });
});

app.listen(port, () => {
  console.log("Server running on port", port);
});