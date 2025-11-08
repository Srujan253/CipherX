from wordfreq import zipf_frequency
from nltk.corpus import words
import nltk

# Ensure English dictionary is available
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

ENGLISH_WORDS = set(words.words())


def atbash_decrypt(ciphertext):
    """Decrypt (or encrypt) using Atbash cipher. Same operation both ways."""
    result = []
    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr(base + (25 - (ord(ch) - base))))
        else:
            result.append(ch)
    return ''.join(result)


def english_score(text):
    """Simple English-likeness scoring using dictionary words + word frequency."""
    words_list = text.split()
    valid_count = sum(1 for w in words_list if w.lower() in ENGLISH_WORDS)
    if not words_list:
        return 0
    avg_freq = sum(zipf_frequency(w.lower(), 'en') for w in words_list) / len(words_list)
    score = valid_count * 10 + avg_freq * 10
    return round(score, 2)


def detect_atbash(ciphertext):
    """Detect and score Atbash cipher output."""
    text = atbash_decrypt(ciphertext)
    score = english_score(text)
    return [{
        "cipher": "Atbash Cipher",
        "text": text,
        "score": score
    }]
