# utils/substitution.py
"""
Improved monoalphabetic substitution cracker.
Features:
- Word-pattern seeding (match cipher word patterns to dictionary words)
- Frequency-based mapping fallback
- Simulated annealing (temperature schedule) with targeted swaps
- Combined scoring: hybrid_score (global) + digram_score (local)
- Transformer refinement of top candidates
"""

import random, re, math, os, sys
from collections import Counter, defaultdict

# Try import english scorer utilities
try:
    from utils.english_scorer import hybrid_score, refine_with_transformer
except Exception:
    # fallback import path for local dev
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    from english_scorer import hybrid_score, refine_with_transformer

# load word list
try:
    import nltk
    from nltk.corpus import words
    try:
        nltk.data.find('corpora/words')
    except LookupError:
        nltk.download('words')
    ENGLISH_WORDS = set(w.upper() for w in words.words() if w.isalpha())
except Exception:
    ENGLISH_WORDS = set()

# common digrams for quick scoring
COMMON_DIGRAMS = set([
    "TH","HE","IN","ER","AN","RE","ON","AT","EN","ND",
    "TI","ES","OR","TE","OF","ED","IS","IT","AL","AR",
    "ST","TO","NT","HA","SE","OU","IO","LE","VE","ME"
])

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# ---------- helpers ----------

def cipher_word_pattern(word):
    """Return pattern token tuple for a word (e.g. 'KICK' -> (0,1,0,2))."""
    mp = {}
    pat = []
    next_id = 0
    for ch in word:
        if ch not in mp:
            mp[ch] = next_id
            next_id += 1
        pat.append(mp[ch])
    return tuple(pat)

def build_pattern_dict(min_len=2, max_len=12):
    """Build mapping pattern -> list of candidate words (from ENGLISH_WORDS)."""
    patdict = defaultdict(list)
    for w in ENGLISH_WORDS:
        L = len(w)
        if L < min_len or L > max_len:
            continue
        pat = cipher_word_pattern(w)
        patdict[(L, pat)].append(w)
    return patdict

PATTERN_DICT = build_pattern_dict()

def apply_mapping_to_text(text, mapping):
    """Apply mapping dict: ciphertext letter -> plaintext letter."""
    out = []
    for ch in text.upper():
        if ch.isalpha():
            out.append(mapping.get(ch, '?'))
        else:
            out.append(ch)
    return ''.join(out)

def generate_freq_mapping(ciphertext):
    """Simple frequency alignment mapping: most-common cipher -> most-common english."""
    freq = Counter(c for c in ciphertext if c.isalpha())
    most_common_cipher = [c for c, _ in freq.most_common()]
    english_order = sorted(list(ALPHABET), key=lambda c: -ENGLISH_FREQ.get(c, 0)) if 'ENGLISH_FREQ' in globals() else list(ALPHABET)
    mapping = {}
    for i, c in enumerate(most_common_cipher):
        mapping[c] = english_order[i % 26]
    # fill unmapped with remaining letters
    remaining_plain = [p for p in ALPHABET if p not in mapping.values()]
    remaining_cipher = [c for c in ALPHABET if c not in mapping]
    for c, p in zip(remaining_cipher, remaining_plain):
        mapping[c] = p
    return mapping

def digram_score(text):
    """Return fraction of digrams in text that are common (0..1)."""
    text = re.sub(r'[^A-Z]', '', text.upper())
    if len(text) < 2:
        return 0.0
    digs = [text[i:i+2] for i in range(len(text)-1)]
    if not digs:
        return 0.0
    hits = sum(1 for d in digs if d in COMMON_DIGRAMS)
    return hits / len(digs)

# ---------- mapping utilities ----------

def compose_mapping(base_map, replacements):
    """Return new mapping by applying replacements dict over base_map."""
    new_map = base_map.copy()
    new_map.update(replacements)
    return new_map

def swap_mapping(mapping, a, b):
    """Swap plaintext letters for two ciphertext letters a,b (ciphertext letters keys)."""
    nm = mapping.copy()
    nm[a], nm[b] = mapping[b], mapping[a]
    return nm

# ---------- seeding via pattern matching ----------

def seed_mappings_from_patterns(ciphertext, max_words=6, candidates_per_word=5):
    """
    Attempt to find seed mappings by matching frequent cipher words to dictionary words
    Returns list of candidate mappings.
    """
    words_list = [w for w in re.findall(r"[A-Z]{2,}", ciphertext.upper())]
    # sort by frequency and length
    words_sorted = sorted(set(words_list), key=lambda w: (-len(w), -words_list.count(w)))
    seed_maps = []

    for cw in words_sorted[:max_words]:
        L = len(cw)
        pat = cipher_word_pattern(cw)
        candidates = PATTERN_DICT.get((L, pat), [])[:candidates_per_word]
        for cand in candidates:
            # produce mapping from cw -> cand (cipher -> plain)
            m = {}
            ok = True
            for cch, pch in zip(cw, cand):
                # if conflict in mapping - skip
                if cch in m and m[cch] != pch:
                    ok = False
                    break
                m[cch] = pch
            if ok:
                seed_maps.append(m)
    # If none found, return empty
    return seed_maps

# ---------- simulated annealing search ----------

def simulated_annealing(ciphertext, initial_map, max_iters=2000, init_temp=1.0, cooling=0.995):
    """
    Simulated annealing that swaps mapping entries.
    Score = weighted hybrid_score + digram_score
    """
    # prepare text uppercase
    ctext = re.sub(r'[^A-Z ]', '', ciphertext.upper())
    best_map = initial_map.copy()
    best_plain = apply_mapping_to_text(ctext, best_map)
    best_score_h = hybrid_score(best_plain)
    best_dg = digram_score(best_plain)
    best_score = 0.9 * best_score_h + 0.1 * best_dg

    current_map = best_map.copy()
    current_plain = best_plain
    current_score_h = best_score_h
    current_dg = best_dg
    current_score = best_score

    T = init_temp
    letters = [c for c in ALPHABET]

    for i in range(max_iters):
        # propose either random swap or targeted swap using low-frequency plaintext letters
        if random.random() < 0.6:
            a, b = random.sample(list(current_map.keys()), 2)
            candidate_map = swap_mapping(current_map, a, b)
        else:
            # targeted: swap mappings that map to unlikely plain letters (like rare vowels/consonants)
            candidate_map = current_map.copy()
            a, b = random.sample(list(current_map.keys()), 2)
            candidate_map = swap_mapping(current_map, a, b)

        candidate_plain = apply_mapping_to_text(ctext, candidate_map)
        cs_h = hybrid_score(candidate_plain)
        cs_dg = digram_score(candidate_plain)
        cs = 0.9 * cs_h + 0.1 * cs_dg

        # accept if better or by probability
        if cs > current_score or random.random() < math.exp((cs - current_score) / max(1e-9, T)):
            current_map = candidate_map
            current_plain = candidate_plain
            current_score_h = cs_h
            current_dg = cs_dg
            current_score = cs

            if cs > best_score:
                best_score = cs
                best_map = candidate_map.copy()
                best_plain = candidate_plain
                best_score_h = cs_h
                best_dg = cs_dg

        T *= cooling
        if T < 1e-4:
            break

    return best_map, best_plain, best_score

# ---------- top-level detection ----------

def detect_substitution(ciphertext, restarts=30, max_iters=2000, top_n=5, refine=True):
    """
    High-level API: returns top_n candidates (each dict with text, score).
    """
    # clean ciphertext
    ctext = re.sub(r'[^A-Z ]', '', ciphertext.upper())
    if len(re.sub(r'[^A-Z]', '', ctext)) < 6:
        # too short for reliable substitution analysis
        return []

    candidates = []

    # 1) try pattern-seeded mappings
    seeds = seed_mappings_from_patterns(ctext, max_words=6, candidates_per_word=6)
    freq_map = generate_freq_mapping(ctext)

    # combine seeds with freq_map to produce initial maps
    initial_maps = []
    for s in seeds:
        # start from freq_map then overlay seed s
        im = freq_map.copy()
        for k, v in s.items():
            im[k] = v
        initial_maps.append(im)

    # always include pure frequency map and a few random shuffles
    initial_maps.append(freq_map)
    for _ in range(5):
        # random shuffle of freq_map target letters
        vals = list(freq_map.values())
        random.shuffle(vals)
        shuffled = {k: v for k, v in zip(freq_map.keys(), vals)}
        # fill missing keys
        for ch in ALPHABET:
            if ch not in shuffled:
                shuffled[ch] = random.choice([p for p in ALPHABET if p not in shuffled.values()])
        initial_maps.append(shuffled)

    # deduplicate initial_maps by string form
    seen = set()
    uniq_inits = []
    for m in initial_maps:
        key = ''.join([m.get(ch, '?') for ch in ALPHABET])
        if key not in seen:
            seen.add(key)
            uniq_inits.append(m)

    # run multiple restarts using simulated annealing
    for i in range(restarts):
        if i < len(uniq_inits):
            init_map = uniq_inits[i]
        else:
            # start from random permutation of freq_map
            vals = list(freq_map.values())
            random.shuffle(vals)
            init_map = {k: v for k, v in zip(freq_map.keys(), vals)}
            for ch in ALPHABET:
                if ch not in init_map:
                    init_map[ch] = random.choice([p for p in ALPHABET if p not in init_map.values()])

        best_map, best_plain, best_score = simulated_annealing(ctext, init_map, max_iters=max_iters)
        # basic filtering
        if best_score > 0.05:
            candidates.append({"text": best_plain, "score": round(best_score, 4)})

    if not candidates:
        return []

    # sort & deduplicate texts
    candidates.sort(key=lambda x: x["score"], reverse=True)
    unique = []
    seen_texts = set()
    for c in candidates:
        t = re.sub(r'[^A-Z ]', '', c["text"])
        if t not in seen_texts:
            seen_texts.add(t)
            unique.append(c)

    top = unique[:max(10, top_n)]

    # transformer refine top ones
    if refine:
        refined = refine_with_transformer(top, top_k=min(8, len(top)))
        # produce final sorted list
        refined.sort(key=lambda x: x.get("final_score", x.get("score", 0)), reverse=True)
        final = [{"text": r["text"], "score": round(r.get("final_score", r["score"]), 4)} for r in refined[:top_n]]
    else:
        final = top[:top_n]

    return final

# ---------- small main demo ----------
if __name__ == "__main__":
    # substitution of "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG" as test
    cipher = "svool dliow"
    print("=== Substitution auto-detect ===")
    results = detect_substitution(cipher, restarts=20, max_iters=1200)
    for i, r in enumerate(results, 1):
        print(f"{i}. Score={r['score']} | {r['text'][:80]}")
