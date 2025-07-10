import sys
import json
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Load model and tokenizer
model_path = "backend/models"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

def predict(data):
    # Convert input data to text string (e.g., "dur:0.1 proto_tcp:1")
    text = " ".join([f"{key}:{value}" for key, value in data.items()])
    
    # Tokenize
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    
    # Get prediction
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        prediction = torch.argmax(torch.softmax(logits, dim=1)).item()
    
    return prediction

if __name__ == "__main__":
    # Read JSON input from stdin (e.g., from python-shell in server.js)
    input_data = json.load(sys.stdin)
    prediction = predict(input_data)
    print(json.dumps({"prediction": prediction}))