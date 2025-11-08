from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

# === Import cipher modules ===
from utils.detect_cipher import auto_detect
from utils.caesar import detect_caesar
from utils.substitution import detect_substitution
from utils.affine import detect_affine
from utils.atbash import detect_atbash
from utils.vigenere import detect_vigenere  # ✅ NEW import

app = Flask(__name__)
CORS(app)


@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        data = request.get_json()
        cipher_type = (data.get('cipher_type') or '').strip().lower()
        ciphertext = (data.get('ciphertext') or '').strip()

        print("\n=== 🔍 Decrypt Request Received ===")
        print("Cipher Type:", cipher_type)
        print("Ciphertext:", ciphertext)

        if not ciphertext:
            print("❌ Error: Ciphertext is empty")
            return jsonify({"error": "Ciphertext is required"}), 400

        # AUTO DETECT MODE
        if cipher_type in ["auto", "auto detect"]:
            print("⚙️ Running Auto Detection...")
            result = auto_detect(ciphertext)
            print("✅ Auto Detect Result:", result["best_cipher"])
            return jsonify({
                "cipher_used": result["best_cipher"],
                "best_decryption": result["best_text"],
                "top_results": result["top_results"]
            }), 200

        # CAESAR CIPHER
        elif cipher_type in ["caesar", "caesar cipher"]:
            results = detect_caesar(ciphertext, top_n=3)
            print("\n=== 🏛 Caesar Cipher Decryption ===")
            for i, r in enumerate(results[:3], 1):
                print(f"{i}. Shift={r['shift']} | Score={r['score']} | Text={r['text']}")
            print("====================================\n")

            return jsonify({
                "cipher_used": "Caesar Cipher",
                "best_decryption": results[0]["text"] if results else "",
                "top_results": results
            }), 200

        # VIGENÈRE CIPHER
        elif cipher_type in ["vigenere", "vigenere cipher"]:
            results = detect_vigenere(ciphertext, top_n=5)
            print("\n=== 🔐 Vigenère Cipher Auto-Detection ===")
            print(f"Ciphertext: {ciphertext}")
            print("Top 5 Possible Decryptions:\n")
            for i, r in enumerate(results[:5], 1):
                print(f"{i}. Key={r['key']:<6} | Score={r['score']:<6} | Text={r['text']}")
            print("=========================================\n")

            return jsonify({
                "cipher_used": "Vigenère Cipher",
                "top_results": results[:5],
                "best_decryption": results[0]["text"] if results else "",
                "best_key": results[0]["key"] if results else None
            }), 200

        # MONOALPHABETIC CIPHER
        elif cipher_type in ["monoalphabetic", "monoalphabetic cipher"]:
            results = detect_substitution(ciphertext, top_n=3)
            print("\n=== 🔠 Monoalphabetic Cipher Decryption ===")
            for i, r in enumerate(results[:3], 1):
                print(f"{i}. Variant={r.get('mapping_variant', '?')} | Score={r['score']} | Text={r['text']}")
            print("============================================\n")

            return jsonify({
                "cipher_used": "Monoalphabetic Cipher",
                "best_decryption": results[0]["text"] if results else "",
                "top_results": results
            }), 200

        # ATBASH CIPHER
        elif cipher_type in ["atbash", "atbash cipher"]:
            results = detect_atbash(ciphertext)
            print("\n=== 🔁 Atbash Cipher Decryption ===")
            for i, r in enumerate(results, 1):
                print(f"{i}. Text={r['text']}")
            print("====================================\n")

            return jsonify({
                "cipher_used": "Atbash Cipher",
                "best_decryption": results[0]["text"] if results else "",
                "top_results": results
            }), 200

        # AFFINE CIPHER
        elif cipher_type in ["affine", "affine cipher"]:
            results = detect_affine(ciphertext, top_n=5)
            print("\n=== 🔢 Affine Cipher Auto-Detection ===")
            print(f"Ciphertext: {ciphertext}")
            print("Top 5 Possible Decryptions:\n")
            for i, r in enumerate(results[:5], 1):
                print(f"{i}. a={r['a']:<3} | b={r['b']:<3} | Score={r['score']:<6} | Text={r['text']}")
            print("=========================================\n")

            return jsonify({
                "cipher_used": "Affine Cipher",
                "top_results": results[:5],
                "best_decryption": results[0]["text"] if results else "",
                "best_key": {"a": results[0]["a"], "b": results[0]["b"]} if results else None
            }), 200

        # INVALID TYPE
        else:
            print("❌ Invalid cipher type:", cipher_type)
            return jsonify({"error": f"Invalid cipher type '{cipher_type}'"}), 400

    except Exception as e:
        print("🔥 EXCEPTION OCCURRED:")
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "details": traceback.format_exc()
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
