from fastapi import FastAPI
from pydantic import BaseModel
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification
import torch

app = FastAPI()

class InputData(BaseModel):
    text: str

#MODEL_PATH = "xlm-roberta-base"
# offkan sebab model trainning terlalu besar.. 
MODEL_PATH = "./_product_app/fine_tuning/fine_tuned_xlm"
# kene train model didalam fine_tuned.
tokenizer = XLMRobertaTokenizer.from_pretrained(MODEL_PATH)
model = XLMRobertaForSequenceClassification.from_pretrained(MODEL_PATH, num_labels=3)
model.eval()

label_map = {0: "Halal", 1: "Haram", 2: "Mashbooh"}

@app.post("/predict/")
async def predict(input_data: InputData):
    text = input_data.text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        prediction = torch.argmax(logits, dim=-1).item()

    return {"text": text, "halal_status": label_map[prediction]}
