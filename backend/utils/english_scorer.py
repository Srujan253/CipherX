"""
english_scorer.py
-----------------
Advanced hybrid English-likeness scoring system optimized for
classical cipher decryption ranking.

Combines:
- Dictionary word ratio
- Word frequency (Zipf)
- Bigram presence
- Character entropy
- Language probability (langdetect)
- Optional GPT-2 semantic fluency scoring

Fast scoring for brute-force use (cheap_score)
+
Transformer-based re-ranking for top candidates (refine_with_transformer)
"""

import re, math, torch
from collections import Counter
from functools import lru_cache
from wordfreq import zipf_frequency
from nltk.corpus import words
from langdetect import detect_langs, DetectorFactory
from transformers import AutoTokenizer, AutoModelForCausalLM
import nltk

# ====================== SETUP ======================
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

ENGLISH_WORDS = set(words.words())
DetectorFactory.seed = 0

COMMON_BIGRAMS = {
    "TH","HE","IN","ER","AN","RE","ON","AT","EN","ND","TI","ES","OR","TE","OF",
    "ED","IS","IT","AL","AR","ST","TO","NT","HA"
}

_MODEL, _TOKENIZER = None, None
_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ====================== CONFIG ======================
WEIGHTS = {
    "word_ratio": 0.35,
    "freq": 0.20,
    "bigrams": 0.15,
    "entropy": 0.10,
    "lang": 0.15,
    "len_penalty": 0.05
}

# ====================== UTILITIES ======================

def _ensure_model():
    """Lazy-load GPT-2 only once."""
    global _MODEL, _TOKENIZER
    if _MODEL is None or _TOKENIZER is None:
        print("🔹 Loading GPT-2 small model for refinement...")
        _TOKENIZER = AutoTokenizer.from_pretrained("gpt2")
        _MODEL = AutoModelForCausalLM.from_pretrained("gpt2").to(_DEVICE)
        _MODEL.eval()
        print(f"✅ GPT-2 ready on {_DEVICE}")

def clean_text(text: str) -> str:
    text = re.sub(r"[^A-Za-z\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

# ====================== METRIC COMPONENTS ======================

@lru_cache(maxsize=2048)
def word_ratio(text: str) -> float:
    words_list = re.findall(r"[A-Za-z]+", text)
    if not words_list:
        return 0.0
    valid = sum(1 for w in words_list if w.lower() in ENGLISH_WORDS)
    return valid / len(words_list)

@lru_cache(maxsize=2048)
def freq_score(text: str) -> float:
    words_list = re.findall(r"[A-Za-z]+", text)
    if not words_list:
        return 0.0
    avg_zipf = sum(zipf_frequency(w.lower(), "en") for w in words_list) / len(words_list)
    return avg_zipf / 7.0  # normalize (Zipf 0–7)

@lru_cache(maxsize=2048)
def bigram_score(text: str) -> float:
    t = text.upper()
    bigrams = [t[i:i+2] for i in range(len(t) - 1) if t[i:i+2].isalpha()]
    if not bigrams:
        return 0.0
    return sum(1 for b in bigrams if b in COMMON_BIGRAMS) / len(bigrams)

def entropy_score(text: str) -> float:
    freq = Counter(text)
    if not freq:
        return 0.0
    probs = [v / len(text) for v in freq.values()]
    entropy = -sum(p * math.log2(p) for p in probs if p > 0)
    # Normalize: English ≈ 3.5–4.5 bits/char
    return max(0.0, 1 - abs(4 - entropy) / 4)

@lru_cache(maxsize=1024)
def lang_score(text: str) -> float:
    text = text.strip()
    if len(text) < 4:
        return 0.0
    try:
        langs = detect_langs(text)
        for lang in langs:
            if lang.lang == "en":
                return lang.prob
        return 0.0
    except Exception:
        return 0.0

def avg_word_length(text: str) -> float:
    words_list = text.split()
    if not words_list:
        return 0.0
    avg_len = sum(len(w) for w in words_list) / len(words_list)
    return max(0.0, 1 - abs(4.5 - avg_len) / 4.5)

# ====================== COMPOSITE SCORE ======================

def cheap_score(text: str) -> float:
    """Hybrid fast score used during brute-force decryption."""
    text = clean_text(text)
    if not text:
        return 0.0

    w = word_ratio(text)
    f = freq_score(text)
    b = bigram_score(text)
    e = entropy_score(text)
    l = lang_score(text)
    lp = avg_word_length(text)

    score = (
        WEIGHTS["word_ratio"] * w +
        WEIGHTS["freq"] * f +
        WEIGHTS["bigrams"] * b +
        WEIGHTS["entropy"] * e +
        WEIGHTS["lang"] * l +
        WEIGHTS["len_penalty"] * lp
    )

    # Short-text boost if most words valid
    if len(text.split()) <= 3 and w > 0.5:
        score += 0.15

    return round(score, 4)

# Alias for backward compatibility
def hybrid_score(text: str) -> float:
    """Alias for cheap_score - provides hybrid English-likeness scoring."""
    return cheap_score(text)

# ====================== GPT-2 REFINEMENT ======================

@lru_cache(maxsize=512)
def transformer_score(text: str) -> float:
    text = clean_text(text)
    if len(text) < 4:
        return 0.0
    try:
        _ensure_model()
        inputs = _TOKENIZER(text, return_tensors="pt", truncation=True, max_length=128).to(_DEVICE)
        with torch.no_grad():
            outputs = _MODEL(**inputs, labels=inputs["input_ids"])
            loss = float(outputs.loss.cpu().item())
        # Convert loss to positive “fluency” score
        return max(0.0, 1 / (1 + loss))
    except Exception as e:
        print("⚠️ GPT-2 scoring failed:", e)
        return 0.0

def refine_with_transformer(candidates, top_k=5):
    """
    Re-rank top candidates using GPT-2 fluency.
    candidates: [{'text':..., 'score':...}, ...]
    """
    if not candidates:
        return []
    candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)
    top_candidates = candidates[:top_k]

    for cand in top_candidates:
        ai_score = transformer_score(cand["text"])
        cand["ai"] = ai_score
        cand["final_score"] = round(cand["score"] + 0.6 * ai_score, 4)

    # Non-top candidates remain unchanged
    for cand in candidates[top_k:]:
        cand["ai"] = 0
        cand["final_score"] = cand["score"]

    candidates.sort(key=lambda x: x["final_score"], reverse=True)
    return candidates

# ====================== RANKING UTILITY ======================

def rank_decryptions(decryptions: dict, top_n=10, show_console=True):
    """
    decryptions: {'key=1': 'abc text', 'key=2': 'xyz text', ...}
    Returns top_n candidates sorted by score.
    """
    scored = []
    for key, text in decryptions.items():
        s = cheap_score(text)
        if s > 0.15 and len(text.split()) > 1:
            scored.append({"key": key, "text": text, "score": s})

    scored.sort(key=lambda x: x["score"], reverse=True)

    if show_console:
        print("\n🔝 Top Candidates:")
        for i, c in enumerate(scored[:top_n], 1):
            print(f"{i:2d}. {c['key']:>8} → {c['text'][:60]} (score={c['score']:.4f})")

    return scored[:top_n]

# ====================== DEMO ======================

if __name__ == "__main__":
    examples = {
        "key=3": "hello world",
        "key=5": "jgnnq yqtnf",
        "key=8": "asdf qwert",
        "key=15": "good morning",
        "key=22": "qwe asd zxc"
    }

    results = rank_decryptions(examples)
    refined = refine_with_transformer(results[:5])
    print("\n✅ Final ranked (refined):")
    for r in refined[:3]:
        print(f"{r['key']}: {r['text']}  → final_score={r['final_score']:.4f}")