import torch
import pandas as pd
from datasets import Dataset
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification, Trainer, TrainingArguments
import evaluate
import numpy as np
from sklearn.model_selection import train_test_split


df = pd.read_csv("data/halal_haram_dataset.csv")


train_texts, test_texts, train_labels, test_labels = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42)


MODEL_NAME = "xlm-roberta-base"
tokenizer = XLMRobertaTokenizer.from_pretrained(MODEL_NAME)


def encode_texts(texts):
    return tokenizer(texts.tolist(), padding=True, truncation=True, max_length=128)

train_encodings = encode_texts(train_texts)
test_encodings = encode_texts(test_texts)


train_dataset = Dataset.from_dict({
    "input_ids": train_encodings["input_ids"],
    "attention_mask": train_encodings["attention_mask"],
    "labels": train_labels.tolist()
})

test_dataset = Dataset.from_dict({
    "input_ids": test_encodings["input_ids"],
    "attention_mask": test_encodings["attention_mask"],
    "labels": test_labels.tolist()
})


model = XLMRobertaForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3)


training_args = TrainingArguments(
    output_dir="./xlm_model",
    eval_strategy="epoch", 
    save_strategy="epoch",
    logging_dir="./logs",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_steps=10,
    load_best_model_at_end=True,
)


accuracy_metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return accuracy_metric.compute(predictions=predictions, references=labels)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics,
)

trainer.train()


model.save_pretrained("./fine_tuned_xlm")
tokenizer.save_pretrained("./fine_tuned_xlm")

print("✅ Latihan selesai! Model telah disimpan di ./fine_tuned_xlm")
