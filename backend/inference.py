import sys
import json
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch


model_path = "backend/models"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

def predict(data):
    text = " ".join([f"{key}:{value}" for key, value in data.items()])
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.argmax(torch.softmax(outputs.logits, dim=1)).item()
    return prediction

if __name__ == "__main__":
    input_data = json.load(sys.stdin)
    prediction = predict(input_data)
    print(json.dumps({"prediction": prediction}))
