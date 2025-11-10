"""
vigenere_breaker.py (final improved)
-----------------------------------
Enhanced Vigenère auto-decryption system using english_scorer.py for ranking.

Features:
- Key rotation correction
- Local refinement of key letters (±1)
- Smarter chi-squared key estimation
- GPT-2 semantic fluency re-ranking via english_scorer

Usage:
  python vigenere_breaker.py --demo
  python vigenere_breaker.py --break "ciphertext here"
"""

import re
import math
import argparse
from collections import defaultdict

# --- Import with fallback handling ---
try:
    from english_scorer import hybrid_score, refine_with_transformer
except Exception:
    import sys, os
    current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    try:
        from english_scorer import hybrid_score, refine_with_transformer
    except Exception:
        try:
            from .english_scorer import hybrid_score, refine_with_transformer
        except Exception as e:
            raise ImportError(
                "Could not import 'english_scorer'. Ensure english_scorer.py is in the same directory "
                "as vigenere_breaker.py. Original error: {}".format(e)
            ) from e

# --- Helpers ---

def clean_letters(text: str) -> str:
    """Return only uppercase alphabetic characters."""
    return ''.join(ch.upper() for ch in text if ch.isalpha())

# --- Index of Coincidence ---

def index_of_coincidence(text: str) -> float:
    """Compute Index of Coincidence to estimate key length."""
    text = clean_letters(text)
    n = len(text)
    if n < 2:
        return 0.0
    freq = {ch: text.count(ch) for ch in set(text)}
    return sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))

# --- Kasiski & IC methods ---

def kasiski_spacings(cipher: str, min_len=3, max_len=5):
    text = clean_letters(cipher)
    spacings = []
    for L in range(min_len, max_len + 1):
        positions = defaultdict(list)
        for i in range(len(text) - L + 1):
            seq = text[i:i + L]
            positions[seq].append(i)
        for seq, poslist in positions.items():
            if len(poslist) > 1:
                for i in range(1, len(poslist)):
                    spacings.append(poslist[i] - poslist[i - 1])
    return spacings

def likely_key_lengths(cipher: str, max_len=12):
    spacings = kasiski_spacings(cipher)
    if spacings:
        gcd_counts = defaultdict(int)
        for s in spacings:
            for g in range(2, max_len + 1):
                if s % g == 0:
                    gcd_counts[g] += 1
        candidates = sorted(gcd_counts.items(), key=lambda x: x[1], reverse=True)
        if candidates:
            return [k for k, _ in candidates[:5]]
    return ic_key_length_candidates(cipher, max_len)

def ic_key_length_candidates(cipher: str, max_len=12):
    text = clean_letters(cipher)
    scores = []
    for m in range(1, max_len + 1):
        cols = [''.join(text[i::m]) for i in range(m)]
        avg_ic = sum(index_of_coincidence(c) for c in cols) / m
        scores.append((m, avg_ic))
    scores.sort(key=lambda x: x[1], reverse=True)
    return [m for m, _ in scores[:5]]

# --- Chi-squared analysis ---

EN_FREQ = {
    'A': 0.08167,'B':0.01492,'C':0.02782,'D':0.04253,'E':0.12702,'F':0.02228,'G':0.02015,
    'H':0.06094,'I':0.06966,'J':0.00153,'K':0.00772,'L':0.04025,'M':0.02406,'N':0.06749,
    'O':0.07507,'P':0.01929,'Q':0.00095,'R':0.05987,'S':0.06327,'T':0.09056,'U':0.02758,
    'V':0.00978,'W':0.02360,'X':0.00150,'Y':0.01974,'Z':0.00074
}

def chi_squared_for_shift(column: str, shift: int) -> float:
    """Return chi-squared score for a given Caesar shift."""
    if not column:
        return float('inf')
    shifted = [chr((ord(c) - ord('A') - shift) % 26 + ord('A')) for c in column]
    counts = {ch: 0 for ch in EN_FREQ}
    for ch in shifted:
        counts[ch] += 1
    N = len(shifted)
    chi2 = 0.0
    for ch, expected_p in EN_FREQ.items():
        expected = expected_p * N
        chi2 += (counts[ch] - expected) ** 2 / (expected + 1e-9)
    return chi2

def best_shifts_for_length(cipher: str, m: int):
    """Return best shift for each column assuming key length m."""
    text = clean_letters(cipher)
    cols = [''.join(text[i::m]) for i in range(m)]
    shifts = []
    for col in cols:
        best = min(range(26), key=lambda s: chi_squared_for_shift(col, s))
        shifts.append(best)
    return shifts

def shifts_to_key(shifts):
    """Convert numeric shifts to key letters."""
    return ''.join(chr(s + ord('A')) for s in shifts)

# --- Vigenère decrypt ---

def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt ciphertext using given Vigenère key."""
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

# --- Main Decryptor ---

def detect_vigenere(ciphertext: str, max_key_len=10, top_n=5):
    """
    Auto-detect and decrypt Vigenère cipher.
    Includes local refinement for short ciphertexts.
    """
    text = clean_letters(ciphertext)
    if len(text) < 20:
        print("⚠️ Short ciphertext — low confidence.")

    lengths = likely_key_lengths(ciphertext, max_len=max_key_len)
    results = []

    for m in lengths:
        shifts = best_shifts_for_length(ciphertext, m)
        for offset in range(m):  # rotation correction
            rotated = shifts[offset:] + shifts[:offset]
            key = shifts_to_key(rotated)
            dec = vigenere_decrypt(ciphertext, key)
            score = hybrid_score(dec)
            results.append({"key": key, "text": dec, "score": score})

    # --- Local refinement: tweak each key letter ±1 and re-score ---
    refined_results = []
    for r in results:
        key = r["key"]
        best_key, best_score = key, r["score"]
        for i in range(len(key)):
            for delta in (-1, 1):
                klist = list(key)
                klist[i] = chr((ord(klist[i]) - ord('A') + delta) % 26 + ord('A'))
                new_key = ''.join(klist)
                dec = vigenere_decrypt(ciphertext, new_key)
                s = hybrid_score(dec)
                if s > best_score:
                    best_score, best_key = s, new_key
        refined_results.append({
            "key": best_key,
            "text": vigenere_decrypt(ciphertext, best_key),
            "score": best_score
        })

    refined_results.sort(key=lambda x: x["score"], reverse=True)
    final = refine_with_transformer(refined_results[:top_n]) if refined_results else []
    return final[:top_n]

# Backward compatibility alias
break_vigenere = detect_vigenere

# --- Demo ---

def demo():
    plaintext = "cryptography is the art of writing and solving codes used to secure communication"
    key = "LEMON"

    def encrypt(text, key):
        res = []
        ki = 0
        for ch in text:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                shift = ord(key[ki % len(key)].upper()) - ord('A')
                res.append(chr((ord(ch) - base + shift) % 26 + base))
                ki += 1
            else:
                res.append(ch)
        return ''.join(res)

    cipher = encrypt(plaintext, key)
    print("Plaintext:", plaintext)
    print("Key:", key)
    print("Ciphertext:", cipher)

    results = detect_vigenere(cipher, max_key_len=8, top_n=5)
    print("\nTop results:")
    for i, r in enumerate(results, 1):
        print(f"{i}. key={r['key']} | score={r['score']:.4f} | text={r['text'][:80]}")

# --- CLI ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--demo', action='store_true')
    parser.add_argument('--break', dest='ciphertext', type=str)
    args = parser.parse_args()

    if args.demo:
        demo()
    elif args.ciphertext:
        res = detect_vigenere(args.ciphertext)
        for i, r in enumerate(res, 1):
            print(f"{i}. key={r['key']} | score={r['score']:.4f} | text={r['text'][:100]}")
    else:
        print("Use --demo or --break 'ciphertext'")
