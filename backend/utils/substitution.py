from textblob import TextBlob
from collections import Counter
import string, random, math, re
import nltk
from nltk.corpus import words
from wordfreq import zipf_frequency  # ✅ for realistic English scoring

# Ensure English corpus is available
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

COMMON_BIGRAMS = [
    "TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND",
    "TI", "ES", "OR", "TE", "OF", "ED", "IS", "IT", "AL", "AR"
]


# -------------------- Core Decryptor -------------------- #

def substitution_decrypt(ciphertext, mapping):
    """Decrypt ciphertext using a substitution mapping dict."""
    result = ""
    for char in ciphertext.upper():
        if char.isalpha():
            result += mapping.get(char, char)
        else:
            result += char
    return result


# -------------------- English Scoring -------------------- #

def word_score(text):
    """Reward real English words."""
    words_list = text.split()
    valid = [w for w in words_list if w.lower() in ENGLISH_WORDS]
    return len(valid) * 15


def freq_score(text):
    """Compare frequency distribution to English norms."""
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


def bigram_score(text):
    """Reward common English bigrams (TH, HE, IN, etc.)."""
    text = text.upper()
    bigrams = [text[i:i+2] for i in range(len(text) - 1) if text[i:i+2].isalpha()]
    if not bigrams:
        return 0
    matches = sum(1 for b in bigrams if b in COMMON_BIGRAMS)
    return (matches / len(bigrams)) * 100


def probability_score(text):
    """Reward realistic English word probabilities using wordfreq."""
    words_list = text.split()
    if not words_list:
        return 0
    total = 0
    for w in words_list:
        freq = zipf_frequency(w.lower(), 'en')
        if len(w) > 2 and w.lower() not in ENGLISH_WORDS:
            freq *= 0.6  # penalize nonsense words
        total += freq
    return (total / len(words_list)) * 10


def english_score(text):
    """Smarter hybrid score using frequency + linguistic patterns."""
    ws = word_score(text)
    fs = freq_score(text)
    bs = bigram_score(text)
    ps = probability_score(text)
    total = (ws * 1.0) + (fs * 0.4) + (bs * 1.2) + (ps * 1.5)
    return round(total, 2)


# -------------------- Frequency-based Substitution Detector -------------------- #

def detect_substitution(ciphertext, top_n=3):
    """
    Try frequency analysis with randomized mappings
    to find top N likely decryptions.
    """
    ciphertext = re.sub(r'[^A-Za-z ]', '', ciphertext.upper())
    freq = Counter(c for c in ciphertext if c.isalpha())
    if not freq:
        return [{"mapping_variant": 0, "text": ciphertext, "score": 0}]

    most_common = [c for c, _ in freq.most_common()]
    english_sorted = sorted(ENGLISH_FREQ.keys(), key=lambda k: ENGLISH_FREQ[k], reverse=True)

    # Base map aligning frequent letters
    base_map = {c: english_sorted[i % len(english_sorted)] for i, c in enumerate(most_common)}

    results = []
    for attempt in range(20):  # increased random tries for better accuracy
        mapping = base_map.copy()
        for _ in range(random.randint(2, 6)):
            a, b = random.sample(english_sorted, 2)
            for k, v in mapping.items():
                if v == a:
                    mapping[k] = b
                elif v == b:
                    mapping[k] = a

        text = substitution_decrypt(ciphertext, mapping)
        score = english_score(text)
        results.append({
            "mapping_variant": attempt,
            "text": text,
            "score": round(score, 2)
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]
