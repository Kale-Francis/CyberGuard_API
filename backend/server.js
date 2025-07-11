require("dotenv").config();
const express = require("express");
const { PythonShell } = require("python-shell");
const { Kafka } = require("kafkajs");
const mongoose = require("mongoose");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");
const twilio = require("twilio")(process.env.TWILIO_SID, process.env.TWILIO_TOKEN);
const swaggerUi = require("swagger-ui-express");
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(cors());

const port = process.env.PORT || 3000;

// MongoDB Setup
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true });
const userSchema = new mongoose.Schema({ email: String, password: String });
const User = mongoose.model("User", userSchema);
const logSchema = new mongoose.Schema({ data: Object });
const Log = mongoose.model("Log", logSchema);
const predictionSchema = new mongoose.Schema({ record: Object, prediction: Number });
const Prediction = mongoose.model("Prediction", predictionSchema);

// Initial Admin User
(async () => {
  const admin = await User.findOne({ email: "admin@example.com" });
  if (!admin) {
    const hashedPassword = await bcrypt.hash("your_password", 10);
    await User.create({ email: "admin@example.com", password: hashedPassword });
  }
})();

// Authentication Middleware
const authenticate = (req, res, next) => {
  const { authorization } = req.headers;
  if (!authorization || !authorization.startsWith("Bearer ")) {
    return res.status(401).json({ error: "Unauthorized" });
  }
  jwt.verify(authorization.split(" ")[1], process.env.JWT_SECRET, (err) => {
    if (err) return res.status(401).json({ error: "Invalid token" });
    next();
  });
};

// Endpoints
app.post("/login", async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email });
  if (user && await bcrypt.compare(password, user.password)) {
    const token = jwt.sign({ email }, process.env.JWT_SECRET, { expiresIn: "1h" });
    res.json({ token });
  } else {
    res.status(401).json({ error: "Invalid credentials" });
  }
});

app.post("/logs", authenticate, async (req, res) => {
  const producer = new Kafka({ clientId: "cyberguard", brokers: [process.env.KAFKA_BROKERS] }).producer();
  await producer.connect();
  await producer.send({
    topic: "logs",
    messages: [{ value: JSON.stringify(req.body) }],
  });
  await producer.disconnect();
  await Log.create(req.body);
  res.json({ message: "Log ingested" });
});

app.get("/anomalies", authenticate, async (req, res) => {
  const anomalies = await Prediction.aggregate([{ $group: { _id: "$prediction", count: { $sum: 1 } } }]);
  res.json(anomalies);
});

app.post("/predict", (req, res) => {
  const options = { pythonPath: "venv/bin/python3", args: [JSON.stringify(req.body)] };
  PythonShell.run("scripts/inference.py", options, (err, results) => {
    if (err) throw err;
    res.json(JSON.parse(results[0]));
  });
});

// Swagger UI
const swaggerDocument = {
  swagger: "2.0",
  info: { title: "CyberGuard API", version: "1.0" },
  paths: {
    "/login": { post: { summary: "Authenticate user" } },
    "/logs": { post: { summary: "Ingest logs" } },
    "/anomalies": { get: { summary: "View anomalies" } },
    "/predict": { post: { summary: "Get anomaly prediction" } }
  }
};
app.use("/docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// Kafka Consumer
const kafka = new Kafka({ clientId: "cyberguard", brokers: [process.env.KAFKA_BROKERS] });
const consumer = kafka.consumer({ groupId: "cyberguard" });
(async () => {
  await consumer.connect();
  await consumer.subscribe({ topic: "logs", fromBeginning: true });
  await consumer.run({
    eachMessage: async ({ message }) => {
      const record = JSON.parse(message.value.toString());
      const options = { pythonPath: "venv/bin/python3", args: [JSON.stringify(record)] };
      PythonShell.run("scripts/inference.py", options, (err, results) => {
        if (err) throw err;
        const prediction = JSON.parse(results[0]).prediction;
        if (prediction === 1) {
          twilio.messages.create({
            body: `Anomaly detected: ${JSON.stringify(record)}`,
            from: process.env.TWILIO_PHONE,
            to: "+254716364090" 
          }).then(() => console.log("Alert sent"));
        }
        Prediction.create({ record, prediction });
        console.log("Processed:", { record, prediction });
      });
    },
  });
})().catch(console.error);

app.listen(port, () => {
  console.log("Server running on port", port);
});
