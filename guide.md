# CipherX — Complete Project & Architecture Guide

## 1. Overview
**CipherX** is an automated classical cryptography analysis and decryption system. It bridges historical cryptanalysis with modern automated heuristics. Users can input any classical ciphertext without knowing the cipher algorithm or the key, and CipherX will automatically analyze the statistical patterns, identify the likely cipher, decrypt the message, and display the plaintext alongside confidence scores and key parameters.

---

## 2. Tech Stack

### Backend
- **Framework**: Python 3.11+ / Flask
- **CORS**: `flask-cors` for cross-origin communication with Vite frontend
- **NLP & Linguistics**:
  - `wordfreq`: Word frequency estimation via Zipf scale
  - `nltk` & `textblob`: Tokenization and English corpus analysis
  - `langdetect`: Language classification and likelihood scoring
- **Cryptographic Solvers**:
  - `caesar.py`: Brute-force shift iteration (1–25) with English scoring
  - `vigenere.py`: Kasiski examination, Index of Coincidence (IoC), and polyalphabetic key recovery
  - `atbash.py`: Symmetric reciprocal alphabet reversal
  - `affine.py`: Modular arithmetic solver $((ax + b) \pmod{26})$ testing all coprime $a \in \{1,3,5,7,9,11,15,17,19,21,23,25\}$ and shifts $b \in [0, 25]$
  - `substitution.py`: Frequency analysis and monoalphabetic substitution mapping

### Frontend
- **Framework**: React 19 + Vite
- **Styling**: Tailwind CSS v4 + custom retro cryptographic theme
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Visualizations**: Interactive SVG Alberti/Caesar Cipher Wheel with dynamic key shift rotation

---

## 3. Directory Structure

```
CipherX/
├── guide.md                       # This comprehensive architecture & developer guide
├── design.md                      # UI/UX design specifications & vintage parchment design system
├── README.md                      # General repository overview
├── backend/
│   ├── app.py                     # Primary Flask REST API entry point
│   ├── main.py                    # Alternative server bootstrap script
│   ├── requirements.txt           # Python dependency declarations
│   ├── test_api.http              # HTTP request samples for testing
│   └── utils/
│       ├── detect_cipher.py       # Central auto-detection coordinator & pipeline
│       ├── caesar.py              # Caesar cipher detection & decryption
│       ├── vigenere.py            # Vigenère polyalphabetic cipher solver
│       ├── atbash.py              # Atbash reciprocal cipher solver
│       ├── affine.py              # Affine cipher modular arithmetic solver
│       ├── substitution.py        # Monoalphabetic substitution solver
│       └── english_scorer.py      # Statistical English scoring algorithms
└── frontend/
    ├── package.json               # Node.js dependencies & scripts
    ├── vite.config.js             # Vite configuration with Tailwind CSS plugin
    ├── index.html                 # HTML entry point with retro Google Fonts
    └── src/
        ├── main.jsx               # React entry point
        ├── App.jsx                # Router and base layout wrapper
        ├── index.css              # Global styles & parchment theme definitions
        ├── components/
            ├── Navbar.jsx         # Vintage stamp header with seal & dangling mascot
            ├── CipherWheel.jsx    # Concentric dual-ring interactive cipher disk
            └── Footer.jsx         # Classical footer
        └── pages/
            ├── DecryptPage.jsx    # Main 3-panel cryptographic workstation
            └── LandingPage.jsx    # Presentation / landing page
```

---

## 4. How the Auto-Detection Engine Works

When a user submits ciphertext in `Auto Detect` mode:
1. **Sanitization**: Non-alphabetic noise is handled while preserving original spacing and punctuation for candidate outputs.
2. **Parallel Detection Pass**:
   - **Caesar Engine**: Shifts through all 25 possible rotations. Evaluates word frequency using Zipf scale.
   - **Atbash Engine**: Inverts characters ($A \leftrightarrow Z, B \leftrightarrow Y$) and computes English likeness.
   - **Affine Engine**: Tests all valid modular multiplicative inverses ($a$) and shifts ($b$).
   - **Vigenère Engine**: Determines probable key lengths via repeating n-grams (Kasiski) or Index of Coincidence (IoC), decomposes into Caesar sub-problems, and reconstructs the key.
   - **Substitution Engine**: Maps character distributions against standard English letter frequencies (ETAOIN SHRDLU).
3. **English Scoring**: Each candidate decryption is passed to `english_score(text)`, which calculates the average Zipf frequency of recognized English words.
4. **Ranking & Selection**: Candidates are sorted in descending order of score. The top candidates are formatted into `top_results` and returned along with `best_cipher` and `best_decryption`.

---

## 5. API Reference

### `POST /decrypt`
Processes ciphertext and returns decryption candidates.

* **Endpoint**: `http://127.0.0.1:5000/decrypt`
* **Headers**: `Content-Type: application/json`

#### Request Body
```json
{
  "cipher_type": "Auto Detect",
  "ciphertext": "KHOOR ZRUOG WKLV LV FLSKHUA"
}
```
*Allowed `cipher_type` values*: `"Auto Detect"`, `"Caesar Cipher"`, `"Vigenere Cipher"`, `"Monoalphabetic Cipher"`, `"Atbash Cipher"`, `"Affine Cipher"`.

#### Response Body (Auto Detect / Multi-candidate)
```json
{
  "cipher_used": "Caesar (Shift=3)",
  "best_decryption": "HELLO WORLD THIS IS CIPHERX",
  "top_results": [
    {
      "cipher": "Caesar (Shift=3)",
      "text": "HELLO WORLD THIS IS CIPHERX",
      "score": 82.5
    },
    {
      "cipher": "Monoalphabetic (Variant A)",
      "text": "HELLO WORLD THIS IS CIPHERX",
      "score": 82.5
    }
  ]
}
```

---

## 6. How to Run the Project

### Terminal 1: Backend (Flask)
```powershell
# Navigate to backend directory
cd e:\Clg_Mini_Project\mine\CipherX\backend

# Run the Flask API server
python app.py
```
The backend will launch at `http://127.0.0.1:5000`.

### Terminal 2: Frontend (Vite)
```powershell
# Navigate to frontend directory
cd e:\Clg_Mini_Project\mine\CipherX\frontend

# Start the Vite development server
npm run dev
```
The frontend will launch at `http://localhost:5173`.

---

## 7. Cloud Deployment Guide (Hosting on Render)

CipherX can be hosted on **Render** (Free Tier):

### Architecture on Render
1. **Backend Web Service**: Hosts the Python Flask API.
2. **Frontend Static Site**: Hosts the React + Vite static bundle (global CDN, 0 latency).

### Model & RAM Management (Render Free Tier 512 MB Limit)
The backend uses **GPT-2 small** and **NLTK/WordFreq** for scoring. To keep it comfortably within Render’s 512 MB memory limit:
- **Single Worker**: Gunicorn is configured with `--workers 1 --threads 2`. This prevents duplicating PyTorch instances in RAM.
- **Pre-download NLTK**: The build command automatically executes `python -m nltk.downloader words` during build phase.
- **Root Directory**: Set Root Directory to `backend` for the API and `frontend` for the UI.

### Option A: 1-Click Render Blueprint
The repository includes a [render.yaml](file:///e:/Clg_Mini_Project/mine/CipherX/render.yaml) file.
1. Push your code to GitHub.
2. In the Render Dashboard, click **New +** → **Blueprint**.
3. Select your `CipherX` repository.
4. Render will automatically provision both the `cipherx-backend` Web Service and `cipherx-frontend` Static Site, configuring environment variables automatically.

### Option B: Manual Setup
#### Step 1: Deploy Backend (Web Service)
- **Environment**: `Python`
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt && python -m nltk.downloader words`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app --workers 1 --threads 2 --timeout 120`
- Copy your live backend URL (e.g., `https://cipherx-backend.onrender.com`).

#### Step 2: Deploy Frontend (Static Site)
- **Root Directory**: `frontend`
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `dist`
- **Environment Variable**:
  - `VITE_API_URL`: `https://cipherx-backend.onrender.com`

