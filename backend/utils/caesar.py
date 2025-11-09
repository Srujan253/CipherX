# utils/caesar.py
import sys, os, nltk
from nltk.corpus import words
from collections import Counter
from importlib import import_module

# === Try importing the English Scorer ===
try:
    # Try relative import first (when used as package)
    try:
        from . import english_scorer
    except ImportError:
        # Fall back to absolute import (add current dir to path)
        import sys
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        import english_scorer
    
    if hasattr(english_scorer, "hybrid_score"):
        smart_score = english_scorer.hybrid_score
        print("✅ Using advanced english_scorer.hybrid_score for Caesar scoring.")
    elif hasattr(english_scorer, "cheap_score"):
        smart_score = english_scorer.cheap_score
        print("✅ Using english_scorer.cheap_score for Caesar scoring.")
    else:
        raise AttributeError("No hybrid_score or cheap_score found in english_scorer")
except Exception as e:
    print("⚠️ english_scorer not found or invalid, using fallback:", e)
    smart_score = None

# === Setup ===
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

ENGLISH_WORDS = set(words.words())

ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.49, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}

# === Caesar Cipher Core ===
def caesar_encrypt(plaintext, shift):
    result = []
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)

def caesar_decrypt(ciphertext, shift):
    result = []
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base - shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)

# === Lightweight Fallback Scorer ===
def fallback_score(text):
    words_list = text.split()
    if not words_list:
        return 0
    valid = sum(1 for w in words_list if w.lower() in ENGLISH_WORDS)
    return valid / len(words_list)

# === Caesar Auto-Detector ===
def detect_caesar(ciphertext, top_n=3):
    results = []
    for shift in range(26):
        decrypted = caesar_decrypt(ciphertext, shift)
        try:
            score = smart_score(decrypted) if smart_score else fallback_score(decrypted)
        except Exception:
            score = fallback_score(decrypted)
        results.append({
            "shift": shift,
            "text": decrypted,
            "score": round(score, 4)
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    print(f"\n🔍 Caesar Auto-Decryption for: '{ciphertext}'")
    for i, r in enumerate(results[:min(10, len(results))], 1):
        print(f"{i:2d}. shift={r['shift']:2d} → {r['text']}  (score={r['score']:.4f})")

    return results[:top_n]

# === Demo ===
if __name__ == "__main__":
    tests = [
        "dpnqvufs",      # computer
        "tdjfodf",       # science
        "tfdvsjuz",      # security fails
        "ibdlfs",       # hacker
        "ebub",          # data
        "ofuxpsl",      # network
        "fodszqujpo",    # encryption
        "buubdl",       # attack
        "efgfotf",     # defense
        "ufdiopmphz"  # technology fails
    ]
    for text in tests:
        best = detect_caesar(text)
        print(f"✅ Best guess: {best[0]['text']} (shift={best[0]['shift']})\n")
