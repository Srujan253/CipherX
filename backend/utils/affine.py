# utils/affine.py
from collections import Counter
from math import gcd
from wordfreq import zipf_frequency
from nltk.corpus import words
import nltk

# Ensure dictionary
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


# ---------------- Affine Core ---------------- #

def mod_inverse(a, m):
    """Return modular inverse of a under modulo m if it exists."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def affine_decrypt(ciphertext, a, b):
    """Decrypt Affine cipher with given keys a, b."""
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return ""
    result = ""
    for ch in ciphertext.upper():
        if ch.isalpha():
            x = ord(ch) - ord('A')
            plain_val = (a_inv * (x - b)) % 26
            result += chr(plain_val + ord('A'))
        else:
            result += ch
    return result


# ---------------- Scoring System ---------------- #

def word_score(text):
    words_list = text.split()
    valid = [w for w in words_list if w.lower() in ENGLISH_WORDS]
    return len(valid)


def freq_score(text):
    letters = [c for c in text.upper() if c.isalpha()]
    if not letters:
        return 0
    freq = Counter(letters)
    total = sum(freq.values())
    score = 0
    for letter, count in freq.items():
        expected = ENGLISH_FREQ.get(letter, 0)
        actual = (count / total) * 100
        score += 100 - abs(expected - actual)
    return score / len(freq)


def probability_score(text):
    words_list = text.split()
    if not words_list:
        return 0
    total = 0
    for w in words_list:
        freq = zipf_frequency(w.lower(), 'en')
        if w[0].isupper() and not w.isupper():
            freq *= 0.8
        if w.lower() not in ENGLISH_WORDS:
            freq *= 0.6
        total += freq
    return (total / len(words_list)) * 10


def repetition_penalty(text):
    letters = [c for c in text.upper() if c.isalpha()]
    if not letters:
        return 0
    duplicates = sum(letters.count(c) - 1 for c in set(letters))
    return max(0, 10 - duplicates)


def english_score(text):
    """Weighted English-likeness scoring system."""
    ws = word_score(text) * 15
    fs = freq_score(text)
    ps = probability_score(text)
    rp = repetition_penalty(text)
    bonus = 20 if text.strip().lower() in ENGLISH_WORDS else 0
    total = ws + (fs * 0.6) + (ps * 1.3) + rp + bonus
    return round(total, 2)


# ---------------- Affine Detector ---------------- #

def detect_affine(ciphertext, top_n=3):
    """
    Try all valid (a, b) combinations and rank by English score.
    """
    valid_a_values = [a for a in range(1, 26) if gcd(a, 26) == 1]
    results = []

    for a in valid_a_values:
        for b in range(26):
            decrypted = affine_decrypt(ciphertext, a, b)
            score = english_score(decrypted)
            results.append({
                "a": a,
                "b": b,
                "text": decrypted,
                "score": score
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]
