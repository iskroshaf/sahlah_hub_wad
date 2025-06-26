from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# -------------------------------------------------
# Load fine-tuned model
# -------------------------------------------------
MODEL_PATH = "model_A.I/fine_tuned_xlm_roberta"  # Folder model hasil training tadi

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

label_map = {0: "Halal", 1: "Haram"}

# -------------------------------------------------
# FastAPI setup
# -------------------------------------------------
app = FastAPI()

class InputData(BaseModel):
    text: str

@app.post("/predict/")
async def predict(input_data: InputData):
    try:
        inputs = tokenizer(input_data.text, return_tensors="pt", truncation=True, padding=True, max_length=128)
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=-1)
            prediction = torch.argmax(probs, dim=-1).item()
            confidence = probs[0][prediction].item()

        return {
            "input_text": input_data.text,
            "halal_status": label_map[prediction],
            "confidence": round(float(confidence), 4)
        }

    except Exception as e:
        return {
            "error": str(e),
            "status": "Inference failed"
        }
