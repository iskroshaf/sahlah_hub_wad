from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pickle
import onnxruntime as ort
import pandas as pd
import re
from tensorflow.keras.preprocessing.sequence import pad_sequences


MAXLEN = 423



def preprocess_ingredients(raw_text):
    body = raw_text.replace(r'\n', '\n')
    body = re.sub(r'^INGREDIENTS:\s*', '', body, flags=re.IGNORECASE)
    body = body.split("ALLERGEN INFORMATION:")[0]
    body = body.replace('\n', ' ').lower()
    body = re.sub(r'[()]', '', body)
    body = re.sub(r'[^a-z\s]', '', body)
    body = re.sub(r'\s+', ' ', body).strip()
    return body



halal_df = pd.read_csv("_product_app/halal_api/data/halal_keywords.csv")
halal_keywords = halal_df['keyword'].str.lower().tolist()

haram_df = pd.read_csv("_product_app/halal_api/data/haram_keywords.csv")
haram_keywords = haram_df['keyword'].str.lower().tolist()



def rule_based_predict(text):
    text = text.lower()
    if any(word in text for word in haram_keywords):
        return "Haram"
    elif any(word in text for word in halal_keywords):
        return "Halal"
    else:
        return "Unknown"



with open("model_A.I/tokenizer.pickle", "rb") as handle:
    tokenizer = pickle.load(handle)

onnx_model_path = "model_A.I/lstm_haram.onnx"
session = ort.InferenceSession(onnx_model_path)



app = FastAPI()

class InputData(BaseModel):
    text: str

@app.post("/predict/")
async def predict(input_data: InputData):
    try:
        clean_text = preprocess_ingredients(input_data.text)
        
        seq = tokenizer.texts_to_sequences([clean_text])
        padded_seq = pad_sequences(seq, maxlen=MAXLEN, padding='post')

        inputs = {session.get_inputs()[0].name: padded_seq.astype(np.int32)}
        outputs = session.run(None, inputs)
        prediction = np.argmax(outputs[0])
        
        label_map = {0: "Halal", 1: "Haram", 2: "Mashbooh"}
        halal_status = label_map[prediction]

        return {
            "input_text": input_data.text,
            "cleaned": clean_text,
            "halal_status": halal_status,
            "mode": "AI Model"
        }

    except Exception as e:
        fallback = rule_based_predict(input_data.text)
        return {
            "input_text": input_data.text,
            "halal_status": fallback,
            "error": str(e),
            "mode": "Rule-based fallback"
        }