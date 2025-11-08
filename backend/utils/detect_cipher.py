from wordfreq import zipf_frequency
from .caesar import detect_caesar
from .substitution import detect_substitution
from .atbash import detect_atbash
from .vigenere import detect_vigenere
from .affine import detect_affine
import re


# -------------------------- English scoring -------------------------- #
def english_score(text):
    """
    Measures how 'English-like' a text is using word frequencies.
    Higher score = more likely to be real English.
    """
    words = re.findall(r"[A-Za-z]+", text)
    if not words:
        return 0
    total = 0
    for w in words:
        freq = zipf_frequency(w.lower(), 'en')
        if len(w) > 2 and freq > 3.0:
            total += freq
    avg = total / len(words)
    return round(avg * 10, 2)  # scale up to 0–100 range


# -------------------------- Auto Detection -------------------------- #
def auto_detect(ciphertext, top_n=3):
    """
    Try Caesar, Monoalphabetic, Atbash, Vigenere, and Affine decryption.
    Rank and return the most English-like result.
    """
    combined_results = []

    # 1️⃣ Caesar Cipher
    try:
        for r in detect_caesar(ciphertext, top_n=3):
            combined_results.append({
                "cipher": f"Caesar (Shift={r.get('shift', '?')})",
                "text": r["text"],
                "score": english_score(r["text"])
            })
    except Exception as e:
        print(f"[WARN] Caesar detection failed: {e}")

    # 2️⃣ Monoalphabetic Cipher
    try:
        for r in detect_substitution(ciphertext, top_n=3):
            combined_results.append({
                "cipher": f"Monoalphabetic (Variant {r.get('mapping_variant', '?')})",
                "text": r["text"],
                "score": english_score(r["text"])
            })
    except Exception as e:
        print(f"[WARN] Monoalphabetic detection failed: {e}")

    # 3️⃣ Atbash Cipher
    try:
        for r in detect_atbash(ciphertext):
            combined_results.append({
                "cipher": "Atbash Cipher",
                "text": r["text"],
                "score": english_score(r["text"])
            })
    except Exception as e:
        print(f"[WARN] Atbash detection failed: {e}")

    # 4️⃣ Vigenere Cipher
    try:
        for r in detect_vigenere(ciphertext, top_n=3):
            combined_results.append({
                "cipher": f"Vigenere (Key={r.get('key', '?')})",
                "text": r["text"],
                "score": english_score(r["text"])
            })
    except Exception as e:
        print(f"[WARN] Vigenere detection failed: {e}")

    # 5️⃣ Affine Cipher
    try:
        for r in detect_affine(ciphertext, top_n=3):
            combined_results.append({
                "cipher": f"Affine (a={r.get('a', '?')}, b={r.get('b', '?')})",
                "text": r["text"],
                "score": english_score(r["text"])
            })
    except Exception as e:
        print(f"[WARN] Affine detection failed: {e}")

    # Sort by English-likeness score (descending)
    combined_results.sort(key=lambda x: x["score"], reverse=True)

    # Top N
    top_results = combined_results[:top_n]

    # Best guess
    best = top_results[0] if top_results else {
        "cipher": "Unknown",
        "text": ciphertext,
        "score": 0
    }

    print("\n=== 🔍 AUTO DETECTION SUMMARY ===")
    print(f"Ciphertext: {ciphertext}")
    for i, r in enumerate(top_results, 1):
        print(f"{i}. {r['cipher']} | Score={r['score']:<6} | Text={r['text'][:50]}")
    print("==================================\n")

    return {
        "best_cipher": best["cipher"],
        "best_text": best["text"],
        "top_results": top_results
    }
