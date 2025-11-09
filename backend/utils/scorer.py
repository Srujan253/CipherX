from transformers import AutoTokenizer, AutoModelForCausalLM
from nltk.corpus import words
import nltk, torch
from wordfreq import zipf_frequency
from collections import Counter
import re

try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

ENGLISH_WORDS = set(words.words())
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

def gpt2_score(text):
    """GPT-2 perplexity-based fluency scoring."""
    if not text.strip(): return 0
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        loss = model(**inputs, labels=inputs["input_ids"]).loss
    return -loss.item() * 100  # higher = more natural

def dict_score(text):
    """Simple dictionary coverage."""
    words_list = re.findall(r"[A-Za-z]+", text)
    if not words_list: return 0
    return sum(1 for w in words_list if w.lower() in ENGLISH_WORDS) / len(words_list) * 100

def hybrid_score(text):
    """Combine dictionary + GPT-2 fluency."""
    return 0.4 * dict_score(text) + 0.6 * gpt2_score(text)
