# utils/atbash.py
try:
    from .english_scorer import cheap_score
except ImportError:
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    from english_scorer import cheap_score

# ================= ATBASH CORE ================= #

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


# ================= DETECTION ================= #

def detect_atbash(ciphertext):
    """Run Atbash decryption and evaluate English-likeness using fast scoring."""
    text = atbash_decrypt(ciphertext)
    score = cheap_score(text)  # ✅ use fast English scorer
    return [{
        "cipher": "Atbash Cipher",
        "text": text,
        "score": score
    }]
