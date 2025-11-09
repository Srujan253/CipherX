"""
vigenere.py
-----------
Smart Vigenère cipher auto-decryption system with AI-based English scoring.

Features:
- Limited brute-force key search using short English words + frequency-seeded keys.
- Optional key-length estimation via Index of Coincidence (IC).
- AI-based English scoring (hybrid_score) + transformer refinement.
"""

import itertools
import string
import re
import math
import nltk
from nltk.corpus import words
from wordfreq import zipf_frequency

# ===== English scoring imports =====
try:
    from utils.english_scorer import hybrid_score, refine_with_transformer
except ImportError:
    import sys, os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    from english_scorer import hybrid_score, refine_with_transformer

# ===== Setup =====
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

ENGLISH_WORDS = set(words.words())

# ===== Vigenère Core =====
def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt Vigenère cipher using provided key."""
    result = []
    key = key.upper()
    key_index = 0
    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('A')
            result.append(chr((ord(ch) - base - shift) % 26 + base))
            key_index += 1
        else:
            result.append(ch)
    return ''.join(result)


# ===== Key Estimation Utility =====
def index_of_coincidence(text: str) -> float:
    """Compute the Index of Coincidence (IC) to estimate whether text is English-like."""
    text = ''.join(ch.upper() for ch in text if ch.isalpha())
    n = len(text)
    if n < 2:
        return 0
    freq = {ch: text.count(ch) for ch in set(text)}
    ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    return ic


# ===== Key Generator =====
def generate_keys(max_len=4, max_extra_words=300):
    """Return a balanced, diverse list of short potential keys."""
    common_keys = [
        "KEY", "LOCK", "CODE", "DATA", "TIME", "TEST", "WORD", "LOVE", "PASS",
        "NOTE", "PLAN", "TEAM", "STAR", "SUN", "DAY", "SAFE", "GOOD", "WORK",
        "CRYPTO", "SECURE", "INFO", "NET", "SYS"
    ]

    short_candidates = [w.upper() for w in ENGLISH_WORDS if w.isalpha() and 2 <= len(w) <= max_len]
    scored = []
    for w in short_candidates:
        try:
            f = zipf_frequency(w.lower(), 'en')
        except Exception:
            f = -10.0
        scored.append((f, w))
    scored.sort(reverse=True)
    top_words = [w for _, w in scored[:max_extra_words]]

    # small generated patterns
    top_letters = "ETAOINSHRDLU"
    generated = []
    for L in range(2, max_len + 1):
        for p in itertools.product(top_letters[:5], repeat=L):
            generated.append(''.join(p))

    all_keys = list(dict.fromkeys(common_keys + top_words + generated))
    return all_keys


# ===== Auto-Detection with Hybrid Scoring =====
def detect_vigenere(ciphertext: str, max_key_len=4, top_n=5, refine_top_k=5):
    """
    Smart auto-decryptor for Vigenère cipher.
    Uses hybrid English scoring + optional transformer re-ranking.
    """
    ciphertext_clean = ''.join(ch for ch in ciphertext if ch.isalpha() or ch.isspace())
    if not ciphertext_clean:
        return []

    # Guess if text even looks like Vigenère
    ic = index_of_coincidence(ciphertext_clean)
    if ic < 0.045:
        print(f"⚠️ Low IC={ic:.3f}: ciphertext may not be Vigenère/English.")
    else:
        print(f"🔍 Estimated IC={ic:.3f}: plausible for Vigenère cipher.")

    candidate_keys = generate_keys(max_len=max_key_len, max_extra_words=400)

    results = []
    for key in candidate_keys:
        if len(key) > max_key_len:
            continue
        decrypted = vigenere_decrypt(ciphertext_clean, key)
        score = hybrid_score(decrypted)
        if score > 0.05:  # filter gibberish
            results.append({"key": key, "text": decrypted, "score": score})

    if not results:
        return []

    results.sort(key=lambda x: x["score"], reverse=True)
    shortlist = results[:60]  # top few dozen candidates

    # refine top ones using transformer scoring
    refined = refine_with_transformer(shortlist, top_k=refine_top_k)
    refined.sort(key=lambda x: x.get("final_score", x["score"]), reverse=True)

    top = refined[:top_n]
    return [
        {
            "key": r["key"],
            "text": r["text"],
            "score": round(r.get("final_score", r["score"]), 4)
        }
        for r in top
    ]


# ===== Demo =====
if __name__ == "__main__":
    sample = "jvjah ewtcb"  # Ciphertext for HELLOWORLD with key=LEMON
    print("\n=== 🔍 Vigenère Cipher Auto-Detection ===")
    results = detect_vigenere(sample, max_key_len=5, top_n=5)
    for i, r in enumerate(results, 1):
        print(f"{i}. key={r['key']:<6} | score={r['score']:>7} | text={r['text'][:50]}")
