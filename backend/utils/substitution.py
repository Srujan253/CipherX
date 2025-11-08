# utils/substitution.py
from textblob import TextBlob
from collections import Counter
import string, random, math
import nltk
from nltk.corpus import words

# Make sure the word list is available
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


def substitution_decrypt(ciphertext, mapping):
    """Decrypt ciphertext using a substitution mapping dict."""
    result = ""
    for char in ciphertext.upper():
        if char.isalpha():
            result += mapping.get(char, char)
        else:
            result += char
    return result


def word_score(text):
    """Check how many real English words exist in text."""
    blob = TextBlob(text)
    valid_words = [w for w in blob.words if len(w) > 2 and w.lower() in ENGLISH_WORDS]
    return len(valid_words)


def freq_score(text):
    """Compare letter frequency distribution to English frequency."""
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


def english_score(text):
    """Hybrid score: word recognition + letter frequency similarity"""
    return word_score(text) * 10 + freq_score(text)


def detect_substitution(ciphertext, top_n=3):
    """
    Try frequency analysis with randomized mappings
    to find top N likely decryptions.
    """
    ciphertext = ciphertext.upper()
    freq = Counter(c for c in ciphertext if c.isalpha())
    if not freq:
        return [{"mapping_variant": 0, "text": ciphertext, "score": 0}]

    most_common = [c for c, _ in freq.most_common()]
    english_sorted = sorted(ENGLISH_FREQ.keys(), key=lambda k: ENGLISH_FREQ[k], reverse=True)

    # Base map (align top frequency letters)
    base_map = {}
    for i, c in enumerate(most_common):
        base_map[c] = english_sorted[i % len(english_sorted)]

    results = []
    for attempt in range(8):  # try 8 variations
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
