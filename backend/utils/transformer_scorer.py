# utils/transformer_scorer.py
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

print("🔹 Loading GPT-2 model for English scoring...")
tokenizer = AutoTokenizer.from_pretrained("gpt2")     # ← full GPT-2
model = AutoModelForCausalLM.from_pretrained("gpt2")
model.eval()
print("✅ GPT-2 loaded successfully!")

def gpt2_score(text: str) -> float:
    """
    Return an English-likeness score using GPT-2 perplexity.
    Higher = more fluent English.
    """
    if not text.strip():
        return 0.0
    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
        with torch.no_grad():
            outputs = model(**inputs, labels=inputs["input_ids"])
            loss = outputs.loss
        perplexity = torch.exp(loss).item()
        score = max(0, 400 - perplexity)   # invert so higher = better
        return round(score, 2)
    except Exception as e:
        print("⚠️ GPT-2 scoring failed:", e)
        return 0.0
