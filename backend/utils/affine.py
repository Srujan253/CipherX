"""
affine.py
----------
Advanced Affine cipher auto-decryption module with AI-based English scoring.

Features:
- Brute-forces all (a, b) key pairs (where gcd(a, 26) == 1)
- Scores candidates using english_scorer.hybrid_score()
- Refines top results using transformer-based scoring
- Returns top N most probable plaintexts
"""

import math

# Try relative import first (when used as package), then absolute
try:
    from .english_scorer import hybrid_score, refine_with_transformer
except ImportError:
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    from english_scorer import hybrid_score, refine_with_transformer

# ----------------- Math Utilities -----------------

def gcd(a, b):
    """Greatest common divisor."""
    while b:
        a, b = b, a % b
    return a


def mod_inv(a, m):
    """Modular inverse of a mod m."""
    a %= m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


# ----------------- Affine Cipher Core -----------------

def affine_decrypt(ciphertext, a, b, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    """
    D(x) = a_inv * (x - b) mod m
    Works for both upper and lower case.
    """
    result = []
    m = len(alphabet)
    a_inv = mod_inv(a, m)
    if a_inv is None:
        return ""

    for ch in ciphertext:
        if ch.upper() in alphabet:
            x = alphabet.index(ch.upper())
            dec = alphabet[(a_inv * (x - b)) % m]
            # preserve case
            result.append(dec.lower() if ch.islower() else dec)
        else:
            result.append(ch)

    return "".join(result)


# ----------------- Affine Auto Detection -----------------

def detect_affine(ciphertext, top_n=5, refine=True):
    """
    Brute-force all valid (a,b) key pairs and score using hybrid English detection.
    Optionally refine top results using transformer re-ranking.
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    m = len(alphabet)
    valid_a = [a for a in range(1, m) if gcd(a, m) == 1]
    results = []

    for a in valid_a:
        for b in range(m):
            decrypted = affine_decrypt(ciphertext, a, b, alphabet)
            if not decrypted.strip():
                continue
            score = hybrid_score(decrypted)
            if score <= 0.05:  # filter noise
                continue
            results.append({
                "a": a,
                "b": b,
                "text": decrypted,
                "score": round(score, 4)
            })

    if not results:
        return []

    # Sort by base hybrid score
    results.sort(key=lambda x: x["score"], reverse=True)
    shortlist = results[:80]  # keep top 80

    # Optional transformer refinement (only for top 10)
    if refine:
        shortlist = refine_with_transformer(shortlist, top_k=10)

    # Final sorting by final_score (after refinement)
    final_sorted = sorted(shortlist, key=lambda x: x.get("final_score", x["score"]), reverse=True)
    top = final_sorted[:top_n]

    # Clean, minimal result
    cleaned = [
        {
            "a": r["a"],
            "b": r["b"],
            "score": round(r.get("final_score", r["score"]), 4),
            "text": r["text"]
        }
        for r in top
    ]
    return cleaned


# ----------------- Demo -----------------

if __name__ == "__main__":
    sample = "RCLLA OAPLX"  # Ciphertext for "HELLO WORLD" (a=5, b=8)
    print("=== 🔍 Affine Cipher Auto-Detection ===")
    results = detect_affine(sample, top_n=5, refine=True)
    for i, r in enumerate(results, 1):
        print(f"{i}. a={r['a']:2d} | b={r['b']:2d} | Score={r['score']:7.3f} | Text={r['text']}")
