# CipherX (ins)

A small web app for detecting and decrypting classical substitution and polyalphabetic ciphers. This repository contains a Python backend (cipher detection + decryption) and a React + Vite frontend.

## Key features

- Automatic detection of common classical ciphers.
- Decryption support for: Caesar, Vigenère, Atbash, Affine, Monoalphabetic/substitution.
- Backend exposes a JSON API (`/decrypt`) used by the frontend.
- Results may contain `top_results` (best candidate decryptions) or a single `decrypted_text` / `cipher_used`.

## Tech stack

- Backend: Python (Flask or simple HTTP server). See `ins/backend/` for source and `requirements.txt` for dependencies.
- Frontend: React (Vite). See `ins/frontend/`.

## Supported ciphers

Based on files in `ins/backend/utils/`:
- Caesar (`caesar.py`)
- Vigenère (`vigenere.py`)
- Atbash (`atbash.py`)
- Affine (`affine.py`)
- Monoalphabetic / Substitution (`substitution.py`)
- Detection helper (`detect_cipher.py`)

## Project layout

- `ins/backend/` — Python backend, includes `app.py`, `main.py`, `requirements.txt`, and `test_api.http`.
- `ins/frontend/` — React + Vite frontend.
- `ins/backend/utils/` — cipher implementations and detection helpers.

## Local setup

Open two terminals (one for backend, one for frontend).

Backend (Windows PowerShell):

```powershell
# create a Python venv (optional but recommended)
python -m venv .venv; .\.venv\Scripts\Activate.ps1
# install dependencies
pip install -r ins\backend\requirements.txt
# run the backend (adjust if your entrypoint differs)
python ins\backend\main.py
```

Frontend (Windows PowerShell):

```powershell
cd ins\frontend
npm install
# start dev server (Vite)
npm run dev
```

The frontend expects the backend at: `http://127.0.0.1:5000/decrypt` (this is used in the app source).

## API

POST /decrypt

Request JSON:

```json
{
  "cipher_type": "Auto Detect", // or specific: "Caesar Cipher", "Vigenere Cipher", etc.
  "ciphertext": "ENCRYPTED TEXT HERE"
}
```

Response examples:

- Automatic detection with multiple candidate results:

```json
{
  "top_results": [
    {"text":"decrypted text 1","shift":3,"score":0.95},
    {"text":"decrypted text 2","shift":5,"score":0.72},
    {"text":"decrypted text 3","shift":8,"score":0.60}
  ]
}
```

- Single best decryption:

```json
{
  "cipher_used": "Vigenere Cipher",
  "decrypted_text": "the decrypted output"
}
```

PowerShell example (Invoke-RestMethod):

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/decrypt -ContentType 'application/json' -Body '{"cipher_type":"Auto Detect","ciphertext":"LIPPS ASVPH"}'
```

Note: the frontend already handles responses containing `top_results` and will display the candidates.

## Development notes

- The frontend uses `ins/frontend/src/pages/DecryptPage.jsx` which posts to the backend and expects either a `top_results` array (multiple candidates) or a single `decrypted_text` + `cipher_used` response.
- If `top_results` is returned, the frontend displays the top candidates. The backend may include additional fields per candidate such as `shift`, `a`, `b`, `key`, or `mapping_shift` depending on cipher type.

## Testing

- `ins/backend/test_api.http` contains sample requests for quick manual testing (use an editor extension like REST Client) or use the PowerShell `Invoke-RestMethod` example above.

## Contributing

1. Open an issue describing the change.
2. Create a branch, implement tests where appropriate, run the app locally, and open a PR.

## License

This repository does not specify a license file. Add a `LICENSE` if you want to set a project license.
