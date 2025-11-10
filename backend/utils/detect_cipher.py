import sys, os, re, time, traceback
from wordfreq import zipf_frequency

# ---------------- Package import auto-fix ---------------- #
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from .caesar import detect_caesar
    from .substitution import detect_substitution
    from .atbash import detect_atbash
    from .vigenere import detect_vigenere
    from .affine import detect_affine
except ImportError:
    from utils.caesar import detect_caesar
    from utils.substitution import detect_substitution
    from utils.atbash import detect_atbash
    from utils.vigenere import detect_vigenere
    from utils.affine import detect_affine


# -------------------------- English scoring -------------------------- #
def english_score(text):
    """Lightweight English-likeness scorer using word frequency (Zipf scale)."""
    words = re.findall(r"[A-Za-z]+", text)
    if not words:
        return 0.0
    total = 0.0
    for w in words:
        freq = zipf_frequency(w.lower(), 'en')
        if len(w) > 2 and freq > 3.0:
            total += freq
    avg = total / len(words)
    return round(avg * 10, 2)  # 0–100 scale


# -------------------------- Safe execution wrapper -------------------------- #
def safe_detect(detector_func, name, ciphertext, **kwargs):
    """Run cipher detection safely with timing and error isolation."""
    start = time.time()
    results = []
    try:
        res = detector_func(ciphertext, **kwargs)
        if res:
            results = res
    except Exception as e:
        print(f"[WARN] {name} detection failed: {e}")
        traceback.print_exc(limit=1)
    finally:
        elapsed = time.time() - start
        if elapsed > 10:
            print(f"[WARN] {name} detection exceeded 10s ({elapsed:.1f}s).")
    return results


# -------------------------- Auto Detection -------------------------- #
def auto_detect(ciphertext, top_n=3):
    """
    Try Caesar, Monoalphabetic, Atbash, Vigenere, and Affine decryption.
    Rank and return the most English-like result.
    """
    combined_results = []

    detectors = [
        ("Caesar", detect_caesar, {"top_n": 3}),
        # ("Monoalphabetic", detect_substitution, {"top_n": 3}),
        ("Atbash", detect_atbash, {}),
        ("Vigenere", detect_vigenere, {"top_n": 3}),
        ("Affine", detect_affine, {"top_n": 3}),
    ]

    print("\n=== 🔍 AUTO DETECTION START ===")

    for name, func, kwargs in detectors:
        print(f"▶ Running {name} detection...")
        results = safe_detect(func, name, ciphertext, **kwargs)

        # If Caesar, short-circuit after first fast result set
        if name == "Caesar" and results:
            # keep only top few for speed
            results = results[:5]

        for r in results:
            combined_results.append({
                "cipher": (
                    f"{name} (Shift={r.get('shift', '?')})" if name == "Caesar"
                    else f"{name} (Key={r.get('key', '?')})" if name == "Vigenere"
                    else f"{name} (a={r.get('a', '?')}, b={r.get('b', '?')})" if name == "Affine"
                    else f"{name} (Variant {r.get('mapping_variant', '?')})" if name == "Monoalphabetic"
                    else f"{name}"
                ),
                "text": r["text"],
                "score": english_score(r["text"])
            })

    if not combined_results:
        print("⚠️ No valid decryption detected.")
        return {"best_cipher": "Unknown", "best_text": ciphertext, "top_results": []}

    # Sort by English-likeness
    combined_results.sort(key=lambda x: x["score"], reverse=True)
    top_results = combined_results[:top_n]
    best = top_results[0]

    # Summary
    print("\n=== ✅ AUTO DETECTION SUMMARY ===")
    print(f"Ciphertext: {ciphertext[:80]}{'...' if len(ciphertext) > 80 else ''}")
    for i, r in enumerate(top_results, 1):
        print(f"{i}. {r['cipher']} | Score={r['score']:<6} | Text={r['text'][:60]}")
    print("=================================\n")

    return {
        "best_cipher": best["cipher"],
        "best_text": best["text"],
        "top_results": top_results
    }
