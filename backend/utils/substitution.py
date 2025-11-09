# utils/substitution.py
import random, re
from collections import Counter
from math import gcd

try:
    from .english_scorer import cheap_score, refine_with_transformer
except ImportError:
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    from english_scorer import cheap_score, refine_with_transformer

ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.49, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}


# -------------------- Helpers -------------------- #

def substitution_decrypt(ciphertext, mapping):
    """Decrypt ciphertext using a substitution mapping dict."""
    result = []
    for ch in ciphertext.upper():
        if ch.isalpha():
            result.append(mapping.get(ch, ch))
        else:
            result.append(ch)
    return ''.join(result)


def generate_base_mapping(ciphertext):
    """Initial mapping guess based on letter frequency alignment."""
    freq = Counter(c for c in ciphertext if c.isalpha())
    most_common = [c for c, _ in freq.most_common()]
    english_sorted = sorted(ENGLISH_FREQ.keys(), key=lambda k: ENGLISH_FREQ[k], reverse=True)
    return {c: english_sorted[i % 26] for i, c in enumerate(most_common)}


def random_swap(mapping):
    """Return a slightly altered version of a mapping by swapping two values."""
    new_map = mapping.copy()
    a, b = random.sample(list(new_map.keys()), 2)
    new_map[a], new_map[b] = new_map[b], new_map[a]
    return new_map


# -------------------- Hill-Climbing Search -------------------- #

def improve_mapping(ciphertext, initial_map, max_iterations=200):
    """Try random swaps to find higher-scoring decryptions."""
    best_map = initial_map
    best_score = cheap_score(substitution_decrypt(ciphertext, best_map))
    no_improve = 0

    for _ in range(max_iterations):
        new_map = random_swap(best_map)
        new_text = substitution_decrypt(ciphertext, new_map)
        new_score = cheap_score(new_text)

        if new_score > best_score:
            best_map, best_score = new_map, new_score
            no_improve = 0
        else:
            no_improve += 1

        if no_improve > 40:  # stop if stuck
            break

    return best_map, best_score


# -------------------- Detection -------------------- #

def detect_substitution(ciphertext, top_n=5):
    """
    Frequency + AI-based substitution cracker using random restarts
    and hill-climbing for better English output.
    """
    ciphertext = re.sub(r'[^A-Z ]', '', ciphertext.upper())
    base_map = generate_base_mapping(ciphertext)

    results = []
    for i in range(20):  # multiple random restarts (increased from 12)
        shuffled_map = random_swap(base_map)
        improved_map, score = improve_mapping(ciphertext, shuffled_map, max_iterations=200)
        text = substitution_decrypt(ciphertext, improved_map)
        results.append({
            "mapping_variant": i,
            "text": text,
            "score": round(score, 2)
        })

    # Sort by cheap_score
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Refine top candidates with transformer scoring for better ranking
    refined = refine_with_transformer(results, top_k=min(top_n, 5))
    
    return refined[:top_n]
