# import torch
# import pandas as pd
# from datasets import Dataset
# from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification, Trainer, TrainingArguments
# import evaluate
# import numpy as np
# from sklearn.model_selection import train_test_split


# df = pd.read_csv("data/halal_haram.csv")


# train_texts, test_texts, train_labels, test_labels = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42)


# MODEL_NAME = "xlm-roberta-base"
# tokenizer = XLMRobertaTokenizer.from_pretrained(MODEL_NAME)


# def encode_texts(texts):
#     return tokenizer(texts.tolist(), padding=True, truncation=True, max_length=128)

# train_encodings = encode_texts(train_texts)
# test_encodings = encode_texts(test_texts)


# train_dataset = Dataset.from_dict({
#     "input_ids": train_encodings["input_ids"],
#     "attention_mask": train_encodings["attention_mask"],
#     "labels": train_labels.tolist()
# })

# test_dataset = Dataset.from_dict({
#     "input_ids": test_encodings["input_ids"],
#     "attention_mask": test_encodings["attention_mask"],
#     "labels": test_labels.tolist()
# })


# model = XLMRobertaForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3)


# training_args = TrainingArguments(
#     output_dir="./xlm_model",
#     eval_strategy="epoch", 
#     save_strategy="epoch",
#     logging_dir="./logs",
#     num_train_epochs=3,
#     per_device_train_batch_size=8,
#     per_device_eval_batch_size=8,
#     warmup_steps=500,
#     weight_decay=0.01,
#     logging_steps=10,
#     load_best_model_at_end=True,
# )


# accuracy_metric = evaluate.load("accuracy")

# def compute_metrics(eval_pred):
#     logits, labels = eval_pred
#     predictions = np.argmax(logits, axis=-1)
#     return accuracy_metric.compute(predictions=predictions, references=labels)


# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=train_dataset,
#     eval_dataset=test_dataset,
#     compute_metrics=compute_metrics,
# )

# trainer.train()


# model.save_pretrained("./fine_tuned_xlm")
# tokenizer.save_pretrained("./fine_tuned_xlm")

# print("✅ Latihan selesai! Model telah disimpan di ./fine_tuned_xlm")





#!/usr/bin/env python
"""Fine‑tune XLM‑Roberta on a trilingual halal/haram/masbooh dataset.

Usage:
  python train_xlm_roberta_fixed.py \
      --csv ../data/halal_haram_masbooh_trilingual_large.csv \
      --output ./fine_tuned_xlm

If no CLI args are given, defaults are used.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from sklearn.model_selection import train_test_split
from transformers import (
    AutoTokenizer,
    XLMRobertaForSequenceClassification,
    TrainingArguments,
    Trainer,
)
import evaluate

# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--csv", type=str, default="data/halal_haram.csv",
                    help="Path to the CSV dataset. Must contain columns 'text' and 'label'.")
parser.add_argument("--output", type=str, default="./fine_tuned_xlm",
                    help="Directory to save checkpoints and final model.")
parser.add_argument("--epochs", type=int, default=3)
parser.add_argument("--batch", type=int, default=8)
parser.add_argument("--fp16", action="store_true", help="Enable mixed‑precision training (needs Ampere/Turing GPU).")
args = parser.parse_args()

csv_path = Path(args.csv)
assert csv_path.exists(), f"CSV file not found: {csv_path}"

# -----------------------------------------------------------------------------
# Load & preprocess
# -----------------------------------------------------------------------------
print("🗃️  Loading dataset …")
df = pd.read_csv(csv_path)

# Map string labels → int IDs
label2id = {"halal": 0, "haram": 1, "masbooh": 2}
id2label = {v: k for k, v in label2id.items()}
if df["label"].dtype != int:
    df["label_id"] = df["label"].map(label2id)
else:
    # Already numeric (0/1/2) – rename for clarity
    df["label_id"] = df["label"]

train_texts, test_texts, train_labels, test_labels = train_test_split(
    df["text"], df["label_id"], test_size=0.20, random_state=42, stratify=df["label_id"]
)

MODEL_NAME = "xlm-roberta-base"
print("🔤 Loading tokenizer …")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

max_length = 128

def encode(texts):
    return tokenizer(texts.tolist(), truncation=True, padding="max_length", max_length=max_length)

train_enc = encode(train_texts)
test_enc = encode(test_texts)

train_ds = Dataset.from_dict({
    "input_ids": train_enc["input_ids"],
    "attention_mask": train_enc["attention_mask"],
    "labels": train_labels.tolist(),
})

test_ds = Dataset.from_dict({
    "input_ids": test_enc["input_ids"],
    "attention_mask": test_enc["attention_mask"],
    "labels": test_labels.tolist(),
})

# -----------------------------------------------------------------------------
# Model
# -----------------------------------------------------------------------------
print("🧠 Loading model …")
model = XLMRobertaForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=3,
    id2label=id2label,
    label2id=label2id,
)

# -----------------------------------------------------------------------------
# Training setup
# -----------------------------------------------------------------------------
print("⚙️  Setting up Trainer …")
accuracy = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return accuracy.compute(predictions=preds, references=labels)

training_args = TrainingArguments(
    output_dir=args.output,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    metric_for_best_model="accuracy",
    load_best_model_at_end=True,
    num_train_epochs=args.epochs,
    per_device_train_batch_size=args.batch,
    per_device_eval_batch_size=args.batch,
    warmup_ratio=0.05,
    weight_decay=0.01,
    logging_steps=25,
    fp16=args.fp16,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=test_ds,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# -----------------------------------------------------------------------------
# Train
# -----------------------------------------------------------------------------
print("🚀 Starting fine‑tuning …")
trainer.train()

# -----------------------------------------------------------------------------
# Save
# -----------------------------------------------------------------------------
print(f"💾 Saving best model to {args.output} …")
model.save_pretrained(args.output)
tokenizer.save_pretrained(args.output)
print("✅ Training complete!")
