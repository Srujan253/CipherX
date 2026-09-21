import { useState, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Loader2, Copy, Check, AlertCircle, RefreshCw } from 'lucide-react'
import CipherWheel from '../components/CipherWheel'

const CIPHER_LIST = [
  { id: 'caesar', name: 'Caesar Cipher' },
  { id: 'vigenere', name: 'Vigenère Cipher' },
  { id: 'atbash', name: 'Atbash Cipher' },
  { id: 'affine', name: 'Affine Cipher' },
  { id: 'substitution', name: 'Substitution Cipher' },
]

const DecryptPage = () => {
  const [inputText, setInputText] = useState('KHOOR ZRUOG WKLV LV FLSKHUA')
  const [cipherType, setCipherType] = useState('auto')
  const [outputText, setOutputText] = useState('')
  const [candidateList, setCandidateList] = useState([])
  const [detectedCipherName, setDetectedCipherName] = useState('Caesar Cipher')
  const [detectedShift, setDetectedShift] = useState(3)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [copied, setCopied] = useState(false)

  const cipherOptions = [
    { value: 'auto', label: 'Auto Detect' },
    { value: 'caesar', label: 'Caesar Cipher' },
    { value: 'vigenere', label: 'Vigenère Cipher' },
    { value: 'monoalphabetic', label: 'Monoalphabetic / Substitution' },
    { value: 'atbash', label: 'Atbash Cipher' },
    { value: 'affine', label: 'Affine Cipher' },
  ]

  // Determine which ciphers are considered "matched" (✓) vs "unmatched" (✕)
  const activeCipherMatches = useMemo(() => {
    const matches = {}
    CIPHER_LIST.forEach((c) => {
      matches[c.id] = false
    })

    const name = (detectedCipherName || '').toLowerCase()

    if (name.includes('caesar')) {
      matches['caesar'] = true
      matches['substitution'] = true // Caesar is a monoalphabetic substitution subset
    } else if (name.includes('vigen')) {
      matches['vigenere'] = true
    } else if (name.includes('atbash')) {
      matches['atbash'] = true
      matches['substitution'] = true
    } else if (name.includes('affine')) {
      matches['affine'] = true
      matches['substitution'] = true
    } else if (name.includes('substitution') || name.includes('mono')) {
      matches['substitution'] = true
    }

    // Also check candidates
    if (candidateList.length > 0) {
      candidateList.forEach((item) => {
        const itemText = (item.cipher || '').toLowerCase()
        if (itemText.includes('caesar')) matches['caesar'] = true
        if (itemText.includes('vigen')) matches['vigenere'] = true
        if (itemText.includes('atbash')) matches['atbash'] = true
        if (itemText.includes('affine')) matches['affine'] = true
        if (itemText.includes('substitution') || itemText.includes('mono')) matches['substitution'] = true
      })
    }

    return matches
  }, [detectedCipherName, candidateList])

  const handleDecrypt = async () => {
    if (!inputText.trim()) {
      setError('Please enter some text to decrypt')
      return
    }

    setIsLoading(true)
    setError('')
    setSuccess(false)
    setOutputText('')
    setCandidateList([])

    try {
      const apiUrl = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000').replace(/\/$/, '')
      const response = await fetch(`${apiUrl}/decrypt`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          cipher_type:
            cipherType === 'auto'
              ? 'Auto Detect'
              : cipherType === 'caesar'
              ? 'Caesar Cipher'
              : cipherType === 'vigenere'
              ? 'Vigenere Cipher'
              : cipherType === 'monoalphabetic'
              ? 'Monoalphabetic Cipher'
              : cipherType === 'atbash'
              ? 'Atbash Cipher'
              : cipherType === 'affine'
              ? 'Affine Cipher'
              : 'Auto Detect',
          ciphertext: inputText,
        }),
      })

      const data = await response.json()

      if (data.error) throw new Error(data.error)

      let identified = data.cipher_used || 'Decrypted Output'
      let mainText = data.best_decryption || data.decrypted_text || ''

      // Extract shift or key for the cipher wheel
      if (data.top_results && data.top_results.length > 0) {
        setCandidateList(data.top_results)
        const best = data.top_results[0]
        identified = data.cipher_used || best.cipher || 'Caesar Cipher'
        mainText = best.text || mainText

        if (best.shift !== undefined) {
          setDetectedShift(best.shift)
        } else if (best.cipher && best.cipher.includes('Shift=')) {
          const match = best.cipher.match(/Shift=(\d+)/)
          if (match) setDetectedShift(parseInt(match[1], 10))
        }

        const formatted = data.top_results
          .map((r, i) => {
            const label =
              r.cipher ||
              (r.shift !== undefined
                ? `Caesar (Shift=${r.shift})`
                : r.key
                ? `Vigenère (Key=${r.key})`
                : r.a !== undefined && r.b !== undefined
                ? `Affine (a=${r.a}, b=${r.b})`
                : r.mapping_shift !== undefined
                ? `Monoalphabetic (Shift=${r.mapping_shift})`
                : 'Candidate')
            return `${i + 1}. [${label}] Score: ${r.score}\n${r.text}`
          })
          .join('\n\n')

        setOutputText(mainText)
      } else {
        setOutputText(mainText)
      }

      setDetectedCipherName(identified)
      setSuccess(true)
    } catch (err) {
      setError(err.message || 'Decryption failed. Is the backend running on port 5000?')
    } finally {
      setIsLoading(false)
    }
  }

  const handleClear = () => {
    setInputText('')
    setOutputText('')
    setCandidateList([])
    setError('')
    setSuccess(false)
    setDetectedCipherName('')
    setDetectedShift(0)
  }

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="min-h-[calc(100vh-65px)] bg-[#f4eedb] text-[#2b2621] py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-[1400px] mx-auto">
        {/* Main 3-Column Workstation Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          {/* ================= COLUMN 1: CIPHERTEXT INPUT ================= */}
          <div className="lg:col-span-4 bg-[#efe8d6] border border-[#d6cdba] rounded-lg p-5 shadow-xs flex flex-col justify-between">
            <div>
              {/* Header */}
              <div className="border-b border-dashed border-[#b8ad99] pb-2 mb-4">
                <h2 className="font-typewriter text-xs uppercase tracking-[0.2em] text-[#423a2f] font-bold">
                  Ciphertext Input
                </h2>
              </div>

              {/* Cipher Type Selector */}
              <div className="flex items-center justify-between mb-3 text-xs font-typewriter">
                <span className="text-[#685f52]">cipher_type:</span>
                <select
                  value={cipherType}
                  onChange={(e) => setCipherType(e.target.value)}
                  className="bg-[#fcfaf5] border border-[#cfc4b0] rounded px-2.5 py-1 text-[#7e221d] font-bold cursor-pointer focus:outline-none focus:ring-1 focus:ring-[#7e221d]"
                >
                  {cipherOptions.map((opt) => (
                    <option key={opt.value} value={opt.value}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Textarea Box */}
              <div className="relative mb-4">
                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value.toUpperCase())}
                  placeholder="ENTER ENCRYPTED TEXT HERE..."
                  rows={5}
                  className="w-full bg-[#fcfaf5] border border-[#cfc4b0] rounded-sm p-3.5 font-typewriter text-sm tracking-wider uppercase text-[#2b2621] placeholder-[#a69c8b] focus:outline-none focus:border-[#7e221d] focus:ring-1 focus:ring-[#7e221d] shadow-inner resize-none leading-relaxed"
                />
              </div>

              {/* Status Line */}
              <div className="mb-5 min-h-[22px]">
                {isLoading ? (
                  <p className="font-typewriter text-xs text-[#8c5a20] flex items-center space-x-1.5 animate-pulse">
                    <Loader2 className="w-3.5 h-3.5 animate-spin inline-block text-[#8c5a20]" />
                    <span>cipher identifying — decrypting...</span>
                  </p>
                ) : success ? (
                  <p className="font-typewriter text-xs text-[#5e7039] font-medium">
                    cipher identified — successfully decrypted.
                  </p>
                ) : error ? (
                  <p className="font-typewriter text-xs text-[#a82a2a] flex items-center space-x-1">
                    <AlertCircle className="w-3.5 h-3.5 inline-block shrink-0" />
                    <span>{error}</span>
                  </p>
                ) : (
                  <p className="font-typewriter text-xs text-[#8c8273]">
                    ready for cryptanalysis...
                  </p>
                )}
              </div>

              {/* Cipher Checklist (Matching the reference screenshot) */}
              <div className="space-y-1.5 pt-2 border-t border-dashed border-[#c5bba8] font-typewriter text-xs">
                {CIPHER_LIST.map((cipher) => {
                  const isMatched = activeCipherMatches[cipher.id]
                  return (
                    <div
                      key={cipher.id}
                      className="flex items-center space-x-2.5 py-0.5 transition-colors duration-200"
                    >
                      {isMatched ? (
                        <>
                          <span className="text-[#5e7039] font-bold text-sm leading-none">✓</span>
                          <span className="text-[#5e7039] font-semibold">{cipher.name}</span>
                        </>
                      ) : (
                        <>
                          <span className="text-[#9c9383] text-sm leading-none">✕</span>
                          <span className="text-[#9c9383]">{cipher.name}</span>
                        </>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>

            {/* Actions */}
            <div className="mt-6 pt-4 border-t border-[#d6cdba] flex items-center space-x-3">
              <button
                onClick={handleDecrypt}
                disabled={isLoading || !inputText.trim()}
                className="flex-1 bg-[#7e221d] hover:bg-[#6b1c17] disabled:bg-[#a69c8b] text-[#faf6ee] font-typewriter text-xs uppercase tracking-widest font-bold py-2.5 px-4 rounded shadow-xs transition-colors flex items-center justify-center space-x-2 cursor-pointer disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Decrypting...</span>
                  </>
                ) : (
                  <span>Run Decryption</span>
                )}
              </button>

              <button
                onClick={handleClear}
                className="bg-[#faf6ee] hover:bg-[#eae1ce] border border-[#cfc4b0] text-[#52493d] font-typewriter text-xs uppercase tracking-widest py-2.5 px-3 rounded transition-colors cursor-pointer"
                title="Clear input and results"
              >
                <RefreshCw className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* ================= COLUMN 2: CIPHER WHEEL VISUALIZATION ================= */}
          <div className="lg:col-span-5 bg-[#efe8d6] border border-[#d6cdba] rounded-lg p-5 shadow-xs flex flex-col items-center justify-center min-h-[460px]">
            <CipherWheel
              shift={detectedShift}
              cipherName={detectedCipherName}
              isIdentified={success}
              isSpinning={isLoading}
            />
          </div>

          {/* ================= COLUMN 3: DECRYPTED RESULTS ================= */}
          <div className="lg:col-span-3 bg-[#efe8d6] border border-[#d6cdba] rounded-lg p-5 shadow-xs flex flex-col justify-between min-h-[460px]">
            <div>
              {/* Header */}
              <div className="border-b border-dashed border-[#b8ad99] pb-2 mb-4 flex items-center justify-between">
                <h2 className="font-typewriter text-xs uppercase tracking-[0.2em] text-[#423a2f] font-bold">
                  Decrypted Output
                </h2>
                {outputText && (
                  <button
                    onClick={() => handleCopy(outputText)}
                    className="flex items-center space-x-1 font-typewriter text-[11px] text-[#7e221d] hover:underline cursor-pointer"
                  >
                    {copied ? (
                      <>
                        <Check className="w-3 h-3 text-[#5e7039]" />
                        <span className="text-[#5e7039]">Copied</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-3 h-3" />
                        <span>Copy</span>
                      </>
                    )}
                  </button>
                )}
              </div>

              {/* Best Decryption Box */}
              <div className="bg-[#fcfaf5] border border-[#cfc4b0] rounded-sm p-3.5 font-typewriter text-sm tracking-wider uppercase text-[#2b2621] min-h-[140px] shadow-inner flex flex-col justify-between">
                {outputText ? (
                  <p className="break-words leading-relaxed whitespace-pre-wrap select-all font-semibold">
                    {outputText}
                  </p>
                ) : (
                  <p className="text-[#a69c8b] italic text-xs font-normal">
                    Plaintext result will appear here upon decryption...
                  </p>
                )}

                {detectedCipherName && outputText && (
                  <div className="mt-3 pt-2 border-t border-dashed border-[#e0d6c3] text-[11px] text-[#7e221d] flex items-center justify-between">
                    <span>Algorithm:</span>
                    <span className="font-bold">{detectedCipherName}</span>
                  </div>
                )}
              </div>

              {/* Candidate Decryptions List */}
              {candidateList.length > 1 && (
                <div className="mt-5">
                  <h3 className="font-typewriter text-[11px] uppercase tracking-wider text-[#685f52] mb-2 font-bold">
                    Top Candidates:
                  </h3>
                  <div className="space-y-2 max-h-[180px] overflow-y-auto pr-1">
                    {candidateList.map((cand, idx) => (
                      <div
                        key={idx}
                        onClick={() => {
                          setOutputText(cand.text)
                          if (cand.shift !== undefined) setDetectedShift(cand.shift)
                          if (cand.cipher) setDetectedCipherName(cand.cipher)
                        }}
                        className={`p-2 rounded border cursor-pointer font-typewriter text-xs transition-all ${
                          outputText === cand.text
                            ? 'bg-[#f7f0df] border-[#7e221d] text-[#7e221d] font-bold'
                            : 'bg-[#faf6ed] border-[#d8cfbe] text-[#4a4237] hover:border-[#b8ad99]'
                        }`}
                      >
                        <div className="flex items-center justify-between text-[10px] text-[#6d6457]">
                          <span className="truncate">{cand.cipher || `Rank #${idx + 1}`}</span>
                          <span className="text-[#5e7039]">Score: {cand.score}</span>
                        </div>
                        <p className="truncate mt-1 text-xs text-[#2b2621]">
                          {cand.text}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Footer hint */}
            <div className="mt-4 pt-3 border-t border-dashed border-[#c5bba8] text-[10px] font-typewriter text-[#8c8273]">
              Tip: Click any candidate to inspect alignment on the cipher wheel.
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}

export default DecryptPage
