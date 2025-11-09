# utils/vigenere.py
import itertools
import string
import re
from nltk.corpus import words
import nltk
from wordfreq import zipf_frequency

# English scoring utilities (cheap first + refine)
try:
    from .english_scorer import cheap_score, refine_with_transformer
except ImportError:
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    from english_scorer import cheap_score, refine_with_transformer

# --------- setup ----------
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

ENGLISH_WORDS = set(words.words())

# --------- core decrypt ----------
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


# --------- generate limited, realistic keys ----------
def generate_keys(max_len=4, common_only=True, max_extra_words=300):
    """
    Return a compact list of candidate keys:
      - Always include a curated set of common keys.
      - Optionally add the top `max_extra_words` most frequent short English words (from wordfreq).
      - And a small set of generated seeds from top letters for variety.
    This avoids thousands of candidates while still covering likely keys.
    """
    common_keys = [
        "KEY", "LOCK", "CODE", "DATA", "TIME", "TEST", "WORD", "LOVE",
        "PASS", "NOTE", "BOOK", "PLAN", "TEAM", "STAR", "SUN", "DAY",
        "SAFE", "LIFE", "GOOD", "WORK", "SEC", "SAFE", "CRYPTO"
    ]

    if common_only:
        # small curated set
        return list(dict.fromkeys([k.upper() for k in common_keys]))

    # gather short words from nltk but filter by zipf frequency (wordfreq)
    short_candidates = [w.upper() for w in ENGLISH_WORDS if w.isalpha() and 2 <= len(w) <= max_len]
    # score them by wordfreq and pick top N
    scored = []
    for w in short_candidates:
        try:
            f = zipf_frequency(w.lower(), 'en')
        except Exception:
            f = -10.0
        scored.append((f, w))
    scored.sort(reverse=True)  # highest frequency first
    top_words = [w for _, w in scored[:max_extra_words]]

    # small generated seeds using the most frequent letters
    top_letters = "ETAOINSHRDLU"
    generated = []
    for L in range(2, max_len + 1):
        # keep small: product of first 4 letters only
        for p in itertools.product(top_letters[:4], repeat=L):
            generated.append(''.join(p))

    all_keys = list(dict.fromkeys(common_keys + top_words + generated))
    return all_keys


# --------- detection: cheap-first then refine with transformer ----------
def detect_vigenere(ciphertext: str, max_key_len=4, top_n=5, max_candidates=1000, refine_top_k=5):
    """
    Auto-decrypt Vigenère:
      - Generate a limited set of candidate keys
      - Score each decryption cheaply (cheap_score)
      - Keep top `max_candidates` by cheap_score
      - Refine the top `refine_top_k` with transformer via refine_with_transformer
      - Return top_n results
    """
    # normalize ciphertext: keep letters and spaces (preserve spaces for word scoring)
    ciphertext_clean = ''.join(ch for ch in ciphertext if ch.isalpha() or ch.isspace()).upper()
    if not ciphertext_clean:
        return []

    # candidate keys (not huge)
    candidate_keys = generate_keys(max_len=max_key_len, common_only=False, max_extra_words=500)

    # Score every candidate cheaply
    candidates = []
    for key in candidate_keys:
        # skip keys longer than allowed
        if len(key) > max_key_len:
            continue
        decrypted = vigenere_decrypt(ciphertext_clean, key)
        score = cheap_score(decrypted)
        candidates.append({"key": key, "text": decrypted, "score": score})

    # Reduce to a manageable shortlist by cheap score
    candidates.sort(key=lambda x: x["score"], reverse=True)
    shortlist = candidates[:max_candidates]

    # Refine shortlist with transformer (only top refine_top_k will actually call the model)
    refined = refine_with_transformer(shortlist, top_k=refine_top_k)

    # Prepare final results (keep top_n)
    results = []
    for r in refined[:top_n]:
        results.append({
            "key": r.get("key"),
            "text": r.get("text"),
            "score": r.get("final_score", r.get("score"))
        })
    return results
