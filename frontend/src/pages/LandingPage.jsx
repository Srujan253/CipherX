import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowRight, Key, Shield, Terminal, BookOpen, Lock, Unlock, Cpu, FileText, ArrowUpRight, Compass } from 'lucide-react'
import { Link } from 'react-router-dom'

// Sample historical cipher intercepts for the live decipher preview
const HISTORICAL_SAMPLES = [
  {
    cipher: 'Caesar Cipher',
    origin: 'Roman Empire • 58 BC',
    ciphertext: 'KHOOR ZRUOG WKLV LV FLSKHUA',
    plaintext: 'HELLO WORLD THIS IS CIPHERX',
    key: 'Shift: +3 (k=3)',
    formula: 'C ≡ (P + 3) mod 26',
    description: 'Julius Caesar encrypted confidential military dispatches by shifting letters 3 positions forward in the Latin alphabet.',
  },
  {
    cipher: 'Atbash Cipher',
    origin: 'Biblical Hebrew • 500 BC',
    ciphertext: 'SVOOL DLIOW GSRH RH XRKSVIBC',
    plaintext: 'HELLO WORLD THIS IS CIPHERX',
    key: 'Reciprocal Alphabet (A ↔ Z)',
    formula: 'C ≡ (25 - P) mod 26',
    description: 'A traditional Hebrew monoalphabetic substitution where the alphabet is mapped directly to its mirror reverse.',
  },
  {
    cipher: 'Affine Cipher',
    origin: 'Classical Mathematics',
    ciphertext: 'WTAAD LDGAS IHYZ HY XYRSENX',
    plaintext: 'HELLO WORLD THIS IS CIPHERX',
    key: 'Multiplicative: a=5, Additive: b=7',
    formula: 'C ≡ (5P + 7) mod 26',
    description: 'A modular arithmetic substitution combining multiplication by a coprime modulus and an additive Caesar displacement.',
  },
  {
    cipher: 'Vigenère Cipher',
    origin: 'Renaissance France • 1586',
    ciphertext: 'KSQUR DTIPI APWZ PZ ULVLMPB',
    plaintext: 'HELLO WORLD THIS IS CIPHERX',
    key: 'Keyword: "CIPHER"',
    formula: 'Ci ≡ (Pi + Ki) mod 26',
    description: 'The celebrated "Le Chiffre Indéchiffrable" — polyalphabetic substitution once considered immune to frequency cryptanalysis for 300 years.',
  }
]

const LandingPage = () => {
  const [activeSampleIdx, setActiveSampleIdx] = useState(0)
  const [isRevealed, setIsRevealed] = useState(true)
  const [scratchpadText, setScratchpadText] = useState('CIPHER')

  const currentSample = HISTORICAL_SAMPLES[activeSampleIdx]

  // Calculate live Caesar + Atbash for the mini interactive scratchpad
  const scratchpadEncrypted = scratchpadText
    .toUpperCase()
    .split('')
    .map((char) => {
      const code = char.charCodeAt(0)
      if (code >= 65 && code <= 90) {
        return String.fromCharCode(((code - 65 + 3) % 26) + 65)
      }
      return char
    })
    .join('')

  const scratchpadAtbash = scratchpadText
    .toUpperCase()
    .split('')
    .map((char) => {
      const code = char.charCodeAt(0)
      if (code >= 65 && code <= 90) {
        return String.fromCharCode(25 - (code - 65) + 65)
      }
      return char
    })
    .join('')

  return (
    <div className="min-h-screen bg-[#f4eedb] text-[#2b2621] font-typewriter select-none pb-16">
      
      {/* ================= CLASSIFIED DOSSIER TOP BANNER ================= */}
      <div className="w-full bg-[#ebd0bd]/30 border-b border-[#d4cbb8] text-[10px] text-[#6b6151] py-1.5 px-4 sm:px-8 flex flex-wrap items-center justify-between gap-2 uppercase tracking-widest">
        <div className="flex items-center space-x-3">
          <span className="inline-block w-2 h-2 rounded-full bg-[#7e221d] animate-pulse"></span>
          <span className="font-bold text-[#7e221d]">DECLASSIFIED ARCHIVE DOSSIER</span>
          <span className="text-[#a69c8b]">|</span>
          <span>RECORD: #CX-1926</span>
        </div>
        <div className="flex items-center space-x-4 text-[10px]">
          <span>STATUS: OPERATIONAL</span>
          <span className="text-[#a69c8b]">|</span>
          <span>CORE ENGINE: FREQUENCY & ALBERTI SOLVER</span>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-10">
        
        {/* ================= HERO SECTION: ARCHIVAL DOSSIER ================= */}
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch mb-16">
          
          {/* Left Column: Mission & Identity */}
          <div className="lg:col-span-7 flex flex-col justify-between space-y-6">
            <div className="space-y-4">
              
              {/* Archival Stamp Tag */}
              <div className="inline-flex items-center space-x-2 border border-[#7e221d]/40 bg-[#fbf8f0] px-3 py-1 rounded text-xs text-[#7e221d] shadow-xs">
                <Compass className="w-3.5 h-3.5 text-[#7e221d]" />
                <span className="font-bold tracking-widest uppercase">Automated Cryptanalysis Division</span>
              </div>

              {/* Main Historic Title */}
              <h1 className="font-serif-vintage text-4xl sm:text-5xl lg:text-6xl font-black text-[#26201b] leading-[1.12] tracking-tight">
                Decipher History’s Ciphers. <br />
                <span className="text-[#7e221d] italic font-serif">Without the Key.</span>
              </h1>

              {/* Subtitle */}
              <p className="font-typewriter text-sm sm:text-base text-[#5c5243] leading-relaxed max-w-xl">
                CipherX combines classical cryptanalytic heuristics with statistical linguistics. 
                Submit any intercepted classical ciphertext — our automated pipeline identifies the cipher algorithm, reconstructs the key parameters, and displays the plaintext instantly.
              </p>
            </div>

            {/* Features ledger / Technical bullets */}
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 py-2 border-y border-dashed border-[#c7bca8] text-xs">
              <div>
                <div className="text-[10px] uppercase text-[#7e221d] font-bold tracking-wider">Ciphers Supported</div>
                <div className="font-bold text-sm text-[#2b2621]">5 Algorithms</div>
                <div className="text-[10px] text-[#786e60]">Caesar, Vigenère, Atbash...</div>
              </div>
              <div>
                <div className="text-[10px] uppercase text-[#7e221d] font-bold tracking-wider">Detection Mode</div>
                <div className="font-bold text-sm text-[#2b2621]">Heuristic Auto</div>
                <div className="text-[10px] text-[#786e60]">0 Prior Hints Required</div>
              </div>
              <div>
                <div className="text-[10px] uppercase text-[#7e221d] font-bold tracking-wider">Disk Simulation</div>
                <div className="font-bold text-sm text-[#2b2621]">Alberti Wheel</div>
                <div className="text-[10px] text-[#786e60]">Dual-Ring Concentric SVG</div>
              </div>
            </div>

            {/* Call to Actions */}
            <div className="flex flex-wrap items-center gap-4 pt-2">
              <Link
                to="/decrypt"
                className="inline-flex items-center space-x-3 bg-[#7e221d] hover:bg-[#681c17] text-[#faf6ee] font-typewriter font-bold text-xs uppercase tracking-[0.2em] px-7 py-3.5 rounded shadow-sm hover:shadow transition-all group cursor-pointer"
              >
                <span>Launch Workstation</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>

              <a
                href="#codex"
                className="inline-flex items-center space-x-2 bg-[#fbf7ee] hover:bg-[#efe6d2] border border-[#cfc4b0] text-[#423a2f] font-typewriter text-xs uppercase tracking-wider px-5 py-3.5 rounded transition-colors"
              >
                <BookOpen className="w-3.5 h-3.5 text-[#7e221d]" />
                <span>Field Manual Codex</span>
              </a>
            </div>
          </div>

          {/* Right Column: Interactive Live Intercept Decoder Box */}
          <div className="lg:col-span-5 bg-[#efe8d6] border border-[#d6cdba] rounded-lg p-5 shadow-xs flex flex-col justify-between">
            <div>
              {/* Card Header with red seal */}
              <div className="border-b border-dashed border-[#b8ad99] pb-3 mb-4 flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-[#7e221d]"></div>
                  <span className="font-typewriter text-xs uppercase tracking-widest font-bold text-[#3d352a]">
                    Live Intercept Sandbox
                  </span>
                </div>
                <span className="text-[10px] bg-[#e4dac4] text-[#615748] px-2 py-0.5 rounded font-typewriter">
                  SIMULATION
                </span>
              </div>

              {/* Sample Selector Tabs */}
              <div className="grid grid-cols-2 gap-1.5 mb-4 text-[11px]">
                {HISTORICAL_SAMPLES.map((sample, idx) => (
                  <button
                    key={sample.cipher}
                    onClick={() => {
                      setActiveSampleIdx(idx)
                      setIsRevealed(true)
                    }}
                    className={`px-2.5 py-1.5 rounded border text-left truncate transition-colors font-typewriter cursor-pointer ${
                      activeSampleIdx === idx
                        ? 'bg-[#7e221d] text-[#faf6ee] border-[#7e221d] font-bold'
                        : 'bg-[#faf6ed] text-[#52493d] border-[#d8cfbe] hover:border-[#b8ad99]'
                    }`}
                  >
                    {sample.cipher}
                  </button>
                ))}
              </div>

              {/* Intercept Data Sheet */}
              <div className="space-y-3 bg-[#fdfbf7] border border-[#cfc4b0] rounded-sm p-4 shadow-inner">
                <div className="flex items-center justify-between text-[11px] text-[#6d6457] border-b border-[#eee5d3] pb-1.5">
                  <span>HISTORICAL ORIGIN:</span>
                  <span className="font-bold text-[#7e221d]">{currentSample.origin}</span>
                </div>

                {/* Ciphertext representation */}
                <div>
                  <div className="text-[10px] uppercase tracking-wider text-[#8c8273] mb-1">
                    [ Intercepted Encrypted Wire ]
                  </div>
                  <div className="font-typewriter text-xs font-bold tracking-widest text-[#7e221d] bg-[#f9f3e5] p-2.5 rounded border border-[#e8ddc7] break-words">
                    {currentSample.ciphertext}
                  </div>
                </div>

                {/* Plaintext representation */}
                <div>
                  <div className="flex items-center justify-between text-[10px] uppercase tracking-wider text-[#8c8273] mb-1">
                    <span>[ Reconstructed Plaintext ]</span>
                    <button
                      onClick={() => setIsRevealed(!isRevealed)}
                      className="text-[#7e221d] hover:underline cursor-pointer"
                    >
                      {isRevealed ? 'Hide Plaintext' : 'Reveal Plaintext'}
                    </button>
                  </div>
                  <div className="font-typewriter text-xs font-bold tracking-widest text-[#2b2621] bg-[#faf6ee] p-2.5 rounded border border-[#cfc4b0] break-words min-h-[36px] flex items-center">
                    {isRevealed ? currentSample.plaintext : '•••••••••••••••••••••••••••'}
                  </div>
                </div>

                {/* Key metadata */}
                <div className="pt-2 border-t border-dashed border-[#e6dcce] flex flex-wrap items-center justify-between text-[11px]">
                  <span className="text-[#685f52]">Mathematical Key:</span>
                  <span className="font-bold text-[#5e7039]">{currentSample.key}</span>
                </div>
              </div>

              {/* Explanatory snippet */}
              <p className="mt-3 text-[11px] text-[#6d6457] leading-relaxed italic">
                "{currentSample.description}"
              </p>
            </div>

            {/* Direct action button */}
            <div className="mt-4 pt-3 border-t border-[#d6cdba]">
              <Link
                to="/decrypt"
                className="w-full bg-[#f4eedb] hover:bg-[#e8dec7] border border-[#b8ad99] text-[#2b2621] text-xs font-bold uppercase tracking-widest py-2 px-3 rounded flex items-center justify-center space-x-2 transition-colors cursor-pointer"
              >
                <span>Decrypt this in Workstation</span>
                <ArrowUpRight className="w-3.5 h-3.5 text-[#7e221d]" />
              </Link>
            </div>
          </div>

        </section>

        {/* ================= SECTION 2: THE HISTORICAL CIPHER CODEX ================= */}
        <section id="codex" className="mb-16 pt-6">
          <div className="border-b border-dashed border-[#b8ad99] pb-3 mb-8 flex flex-col sm:flex-row sm:items-end justify-between gap-2">
            <div>
              <div className="text-xs uppercase tracking-[0.2em] text-[#7e221d] font-bold">
                Archival Reference
              </div>
              <h2 className="font-serif-vintage text-2xl sm:text-3xl font-bold text-[#26201b] mt-1">
                The Historical Cipher Codex
              </h2>
            </div>
            <p className="font-typewriter text-xs text-[#6e6456] max-w-md">
              Five foundational cryptographic schemes decoded natively by the CipherX heuristic core.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            
            {/* Card 1: Caesar */}
            <div className="bg-[#efe8d6] border border-[#d6cdba] rounded-lg p-5 shadow-xs flex flex-col justify-between hover:border-[#b8ad99] transition-colors">
              <div>
                <div className="flex items-center justify-between mb-3 text-xs">
                  <span className="text-[10px] font-bold text-[#7e221d] bg-[#fbf8f0] px-2 py-0.5 rounded border border-[#cfc4b0]">
                    58 BC • ROME
                  </span>
                  <span className="text-[#6d6457] text-[10px]">MONOALPHABETIC</span>
                </div>
                <h3 className="font-serif-vintage font-bold text-lg text-[#2b2621] mb-1">
                  Caesar Shift Cipher
                </h3>
                <p className="text-xs text-[#615748] leading-relaxed mb-4">
                  Shifts every letter along the 26-character alphabet by a fixed integer $k$. CipherX checks all 25 possible rotations in microseconds and computes English Zipf likelihood.
                </p>
              </div>
              <div className="bg-[#fcfaf5] p-2.5 rounded border border-[#d8cfbe] text-[11px] font-mono text-[#7e221d]">
                Formula: C ≡ (P + k) mod 26
              </div>
            </div>

            {/* Card 2: Vigenère */}
            <div className="bg-[#efe8d6] border border-[#d6cdba] rounded-lg p-5 shadow-xs flex flex-col justify-between hover:border-[#b8ad99] transition-colors">
              <div>
                <div className="flex items-center justify-between mb-3 text-xs">
                  <span className="text-[10px] font-bold text-[#7e221d] bg-[#fbf8f0] px-2 py-0.5 rounded border border-[#cfc4b0]">
                    1586 • FRANCE
                  </span>
                  <span className="text-[#6d6457] text-[10px]">POLYALPHABETIC</span>
                </div>
                <h3 className="font-serif-vintage font-bold text-lg text-[#2b2621] mb-1">
                  Vigenère Cipher
                </h3>
                <p className="text-xs text-[#615748] leading-relaxed mb-4">
                  Applies a repetitive repeating keyword over the Tabula Recta. CipherX employs Kasiski examination and Index of Coincidence (IoC) to break key lengths up to 20 letters.
                </p>
              </div>
              <div className="bg-[#fcfaf5] p-2.5 rounded border border-[#d8cfbe] text-[11px] font-mono text-[#7e221d]">
                Formula: Ci ≡ (Pi + Ki) mod 26
              </div>
            </div>

            {/* Card 3: Atbash */}
            <div className="bg-[#efe8d6] border border-[#d6cdba] rounded-lg p-5 shadow-xs flex flex-col justify-between hover:border-[#b8ad99] transition-colors">
              <div>
                <div className="flex items-center justify-between mb-3 text-xs">
                  <span className="text-[10px] font-bold text-[#7e221d] bg-[#fbf8f0] px-2 py-0.5 rounded border border-[#cfc4b0]">
                    c. 500 BC • JUDEA
                  </span>
                  <span className="text-[#6d6457] text-[10px]">RECIPROCAL MIRROR</span>
                </div>
                <h3 className="font-serif-vintage font-bold text-lg text-[#2b2621] mb-1">
                  Atbash Cipher
                </h3>
                <p className="text-xs text-[#615748] leading-relaxed mb-4">
                  Originally used in biblical scribal texts. Maps the first letter to the last ($A \leftrightarrow Z, B \leftrightarrow Y$). Self-invertible; encrypting twice returns the original plaintext.
                </p>
              </div>
              <div className="bg-[#fcfaf5] p-2.5 rounded border border-[#d8cfbe] text-[11px] font-mono text-[#7e221d]">
                Mapping: A↔Z, B↔Y, C↔X ...
              </div>
            </div>

            {/* Card 4: Affine */}
            <div className="bg-[#efe8d6] border border-[#d6cdba] rounded-lg p-5 shadow-xs flex flex-col justify-between hover:border-[#b8ad99] transition-colors">
              <div>
                <div className="flex items-center justify-between mb-3 text-xs">
                  <span className="text-[10px] font-bold text-[#7e221d] bg-[#fbf8f0] px-2 py-0.5 rounded border border-[#cfc4b0]">
                    ARITHMETIC
                  </span>
                  <span className="text-[#6d6457] text-[10px]">MODULAR LINEAR</span>
                </div>
                <h3 className="font-serif-vintage font-bold text-lg text-[#2b2621] mb-1">
                  Affine Cipher
                </h3>
                <p className="text-xs text-[#615748] leading-relaxed mb-4">
                  Multiplies letters by key $a$ (coprime to 26) and adds key $b$. Decryption requires computing modular multiplicative inverse $a^{-1} \pmod{26}$.
                </p>
              </div>
              <div className="bg-[#fcfaf5] p-2.5 rounded border border-[#d8cfbe] text-[11px] font-mono text-[#7e221d]">
                Formula: P ≡ a⁻¹(C - b) mod 26
              </div>
            </div>

            {/* Card 5: Monoalphabetic Substitution */}
            <div className="bg-[#efe8d6] border border-[#d6cdba] rounded-lg p-5 shadow-xs flex flex-col justify-between hover:border-[#b8ad99] transition-colors">
              <div>
                <div className="flex items-center justify-between mb-3 text-xs">
                  <span className="text-[10px] font-bold text-[#7e221d] bg-[#fbf8f0] px-2 py-0.5 rounded border border-[#cfc4b0]">
                    HISTORICAL
                  </span>
                  <span className="text-[#6d6457] text-[10px]">ARBITRARY KEYMAP</span>
                </div>
                <h3 className="font-serif-vintage font-bold text-lg text-[#2b2621] mb-1">
                  General Substitution
                </h3>
                <p className="text-xs text-[#615748] leading-relaxed mb-4">
                  Replaces each letter with an arbitrary fixed alternative. Cracked via letter frequency distributions (ETAOIN SHRDLU) and common English digram occurrences.
                </p>
              </div>
              <div className="bg-[#fcfaf5] p-2.5 rounded border border-[#d8cfbe] text-[11px] font-mono text-[#7e221d]">
                Keyspace: 26! ≈ 4.03 × 10²⁶ keys
              </div>
            </div>

            {/* Card 6: Alberti Cipher Wheel */}
            <div className="bg-[#efe8d6] border border-[#d6cdba] rounded-lg p-5 shadow-xs flex flex-col justify-between hover:border-[#b8ad99] transition-colors">
              <div>
                <div className="flex items-center justify-between mb-3 text-xs">
                  <span className="text-[10px] font-bold text-[#7e221d] bg-[#fbf8f0] px-2 py-0.5 rounded border border-[#cfc4b0]">
                    1467 • FLORENCE
                  </span>
                  <span className="text-[#6d6457] text-[10px]">MECHANICAL DEVICE</span>
                </div>
                <h3 className="font-serif-vintage font-bold text-lg text-[#2b2621] mb-1">
                  Alberti Cipher Disk
                </h3>
                <p className="text-xs text-[#615748] leading-relaxed mb-4">
                  Leon Battista Alberti invented the dual-concentric disk mechanism. CipherX simulates this exact physical disk in SVG, rotating the inner ring to reveal letter correspondences.
                </p>
              </div>
              <div className="bg-[#fcfaf5] p-2.5 rounded border border-[#d8cfbe] text-[11px] font-mono text-[#7e221d]">
                Dual-Concentric Brass Simulation
              </div>
            </div>

          </div>
        </section>

        {/* ================= SECTION 3: INTERACTIVE MINI SCRATCHPAD ================= */}
        <section className="bg-[#efe8d6] border border-[#d6cdba] rounded-lg p-6 sm:p-8 shadow-xs mb-16">
          <div className="max-w-3xl mx-auto text-center space-y-3 mb-6">
            <span className="text-[10px] uppercase tracking-widest text-[#7e221d] font-bold">
              [ TACTILE EXPERIMENTATION ]
            </span>
            <h2 className="font-serif-vintage text-2xl sm:text-3xl font-bold text-[#26201b]">
              Interactive Cryptographic Scratchpad
            </h2>
            <p className="text-xs text-[#615748]">
              Type any word below to see it transformed into Caesar (+3) and Atbash ciphertexts in real time.
            </p>
          </div>

          <div className="max-w-xl mx-auto space-y-4">
            <div>
              <label className="block text-xs uppercase tracking-wider text-[#6d6457] mb-1.5 font-bold">
                Plaintext Input:
              </label>
              <input
                type="text"
                value={scratchpadText}
                onChange={(e) => setScratchpadText(e.target.value.replace(/[^A-Za-z]/g, ''))}
                placeholder="TYPE A WORD..."
                maxLength={20}
                className="w-full bg-[#fdfbf7] border border-[#cfc4b0] rounded p-3 font-typewriter text-center uppercase tracking-widest text-lg font-bold text-[#2b2621] focus:outline-none focus:border-[#7e221d] shadow-inner"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
              <div className="bg-[#faf6ee] p-3 rounded border border-[#cfc4b0] text-center">
                <div className="text-[10px] uppercase text-[#7e221d] font-bold">Caesar Cipher (Shift +3)</div>
                <div className="font-typewriter text-base font-bold text-[#7e221d] mt-1 tracking-widest break-words">
                  {scratchpadEncrypted || '—'}
                </div>
              </div>

              <div className="bg-[#faf6ee] p-3 rounded border border-[#cfc4b0] text-center">
                <div className="text-[10px] uppercase text-[#5e7039] font-bold">Atbash (Mirror Reverse)</div>
                <div className="font-typewriter text-base font-bold text-[#5e7039] mt-1 tracking-widest break-words">
                  {scratchpadAtbash || '—'}
                </div>
              </div>
            </div>

            <div className="text-center pt-4">
              <Link
                to="/decrypt"
                className="inline-flex items-center space-x-2 bg-[#7e221d] hover:bg-[#681c17] text-[#faf6ee] font-typewriter text-xs uppercase tracking-widest px-6 py-3 rounded shadow-xs transition-colors"
              >
                <span>Decrypt Any Text in Full Workstation</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        </section>

        {/* ================= SECTION 4: THE DECRYPTION PIPELINE ================= */}
        <section className="mb-10">
          <div className="border-b border-dashed border-[#b8ad99] pb-3 mb-6">
            <span className="text-xs uppercase tracking-[0.2em] text-[#7e221d] font-bold">
              Engineering Architecture
            </span>
            <h2 className="font-serif-vintage text-2xl sm:text-3xl font-bold text-[#26201b] mt-1">
              The Cryptanalytic Pipeline
            </h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            
            <div className="bg-[#efe8d6] border border-[#d6cdba] rounded p-4 text-xs">
              <div className="font-serif-vintage font-bold text-[#7e221d] text-lg mb-1">01. Ingestion</div>
              <div className="font-bold text-[#2b2621] mb-1">Noise Filtering</div>
              <p className="text-[#685e50] text-[11px] leading-relaxed">
                Sanitizes input text, separates alphabetic character streams while caching original punctuation for pristine output formatting.
              </p>
            </div>

            <div className="bg-[#efe8d6] border border-[#d6cdba] rounded p-4 text-xs">
              <div className="font-serif-vintage font-bold text-[#7e221d] text-lg mb-1">02. IoC Profiling</div>
              <div className="font-bold text-[#2b2621] mb-1">Polyalphabetic Test</div>
              <p className="text-[#685e50] text-[11px] leading-relaxed">
                Calculates the Index of Coincidence. Flat distributions indicate Vigenère keys, while sharp spikes indicate monoalphabetic shifts.
              </p>
            </div>

            <div className="bg-[#efe8d6] border border-[#d6cdba] rounded p-4 text-xs">
              <div className="font-serif-vintage font-bold text-[#7e221d] text-lg mb-1">03. Key Space Search</div>
              <div className="font-bold text-[#2b2621] mb-1">Multi-Heuristic Core</div>
              <p className="text-[#685e50] text-[11px] leading-relaxed">
                Parallel solvers evaluate Caesar shifts, Atbash inversion, Affine modular pairs, and Vigenère Kasiski periodic tables.
              </p>
            </div>

            <div className="bg-[#efe8d6] border border-[#d6cdba] rounded p-4 text-xs">
              <div className="font-serif-vintage font-bold text-[#7e221d] text-lg mb-1">04. Zipf Ranking</div>
              <div className="font-bold text-[#2b2621] mb-1">English Fluency</div>
              <p className="text-[#685e50] text-[11px] leading-relaxed">
                Ranks decryption candidates using word frequency logarithms on the Zipf scale, outputting the highest-confidence plaintexts.
              </p>
            </div>

          </div>
        </section>

      </div>
    </div>
  )
}

export default LandingPage
