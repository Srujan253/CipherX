# utils/caesar.py
from collections import Counter
import nltk
from nltk.corpus import words
from wordfreq import zipf_frequency

# Ensure English dictionary is available
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


def caesar_decrypt(ciphertext, shift):
    """Decrypt Caesar cipher by shifting backwards."""
    result = ""
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result


def word_score(text):
    """Counts how many valid English words appear."""
    words_list = text.split()
    valid = [w for w in words_list if w.lower() in ENGLISH_WORDS]
    return len(valid)


def freq_score(text):
    """Compare frequency of letters with English norms."""
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
    """Uses wordfreq to calculate how common the words are in real English."""
    words_list = text.split()
    if not words_list:
        return 0
    total = sum(zipf_frequency(w.lower(), 'en') for w in words_list)
    return (total / len(words_list)) * 10  # scale up


def repetition_penalty(text):
    """Apply small penalty for too many repeated letters (e.g., AAAA, DARA)."""
    letters = [c for c in text.upper() if c.isalpha()]
    if not letters:
        return 0
    duplicates = sum(letters.count(c) - 1 for c in set(letters))
    penalty = max(0, 10 - duplicates)  # higher duplicates → lower penalty
    return penalty


def english_score(text):
    """
    Hybrid score emphasizing dictionary accuracy:
    - Heavier weight on real English words
    - Slightly higher bonus for full English matches
    """
    ws = word_score(text) * 15         # ↑ dictionary weight
    fs = freq_score(text)
    ps = probability_score(text)
    rp = repetition_penalty(text)
    bonus = 20 if text.strip().lower() in ENGLISH_WORDS else 0  # ↑ stronger boost

    # Weighted hybrid scoring
    total = ws + (fs * 0.6) + (ps * 1.2) + rp + bonus
    return round(total, 2)


def detect_caesar(ciphertext, top_n=3):
    """Try all 26 Caesar shifts and return top N decryptions ranked by score."""
    results = []
    for shift in range(26):
        decrypted = caesar_decrypt(ciphertext, shift)
        score = english_score(decrypted)
        results.append({
            "shift": shift,
            "text": decrypted,
            "score": score
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]
