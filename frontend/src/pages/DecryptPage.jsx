import { useState } from 'react'
import { motion } from 'framer-motion'
import { Loader2, Copy, CheckCircle, AlertCircle, Lock, Unlock } from 'lucide-react'

const DecryptPage = () => {
  const [inputText, setInputText] = useState('')
  const [cipherType, setCipherType] = useState('auto')
  const [outputText, setOutputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  // ✅ Added Atbash & Affine Cipher here
  const cipherOptions = [
    { value: 'auto', label: 'Auto Detect' },
    { value: 'caesar', label: 'Caesar Cipher' },
    { value: 'vigenere', label: 'Vigenère Cipher' },
    { value: 'monoalphabetic', label: 'Monoalphabetic Cipher' },
    { value: 'atbash', label: 'Atbash Cipher' },
    { value: 'affine', label: 'Affine Cipher' },
  ]

  const handleDecrypt = async () => {
    if (!inputText.trim()) {
      setError("Please enter some text to decrypt");
      return;
    }

    setIsLoading(true);
    setError("");
    setSuccess(false);
    setOutputText("");

    try {
      const response = await fetch("http://127.0.0.1:5000/decrypt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cipher_type:
            cipherType === "auto"
              ? "Auto Detect"
              : cipherType === "caesar"
              ? "Caesar Cipher"
              : cipherType === "vigenere"
              ? "Vigenere Cipher"
              : cipherType === "monoalphabetic"
              ? "Monoalphabetic Cipher"
              : cipherType === "atbash"
              ? "Atbash Cipher"
              : cipherType === "affine"
              ? "Affine Cipher"
              : "Auto Detect",
          ciphertext: inputText,
        }),
      });

      const data = await response.json();

      if (data.error) throw new Error(data.error);

      // ✅ Handles all ciphers (including Affine, Atbash)
      if (data.top_results) {
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
                : "Possible Decryption");

            return `${i + 1}. ${label} | Score=${r.score}\n${r.text}`;
          })
          .join("\n\n");

        setOutputText(`Top Results:\n\n${formatted}`);
        setSuccess(true);
      } else {
        setOutputText(`${data.cipher_used}\n\n${data.decrypted_text || data.best_decryption}`);
        setSuccess(true);
      }
    } catch (err) {
      setError(err.message || "Decryption failed");
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setInputText('')
    setOutputText('')
    setError('')
    setSuccess(false)
    setCipherType('auto')
  }

  return (
    <div className="min-h-screen pt-20">
      <div className="max-w-7xl mx-auto px-6 py-3">
        <div className="max-w-3xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-12"
          >
            <div className="flex items-center justify-center mb-6">
              <motion.div
                animate={{ rotate: success ? 360 : 0 }}
                transition={{ duration: 0.5 }}
                className="p-4 rounded-full bg-white/10 border border-cyan-400/30"
              >
                {isLoading ? (
                  <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
                ) : success ? (
                  <Unlock className="w-8 h-8 text-green-400" />
                ) : (
                  <Lock className="w-8 h-8 text-cyan-400" />
                )}
              </motion.div>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Decrypt Your Cipher
            </h1>
            <p className="text-xl text-gray-400">
              Paste your encrypted text below and let CipherX do the rest.
            </p>
          </motion.div>

          {/* Main Decrypt Panel */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="p-8 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-lg"
          >
            <div className="space-y-6">
              {/* Cipher Type Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Cipher Type
                </label>
                <select
                  value={cipherType}
                  onChange={(e) => setCipherType(e.target.value)}
                  className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all duration-200"
                >
                  {cipherOptions.map((option) => (
                    <option key={option.value} value={option.value} className="bg-gray-800 text-white">
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Input Textarea */}
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Encrypted Text
                </label>
                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Enter your encrypted text here..."
                  rows={6}
                  className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-gray-400 focus:ring-2 focus:ring-cyan-500 focus:border-transparent transition-all duration-200 resize-none"
                />
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-4">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handleDecrypt}
                  disabled={isLoading || !inputText.trim()}
                  className="flex-1 bg-cyan-500 hover:bg-cyan-400 disabled:bg-gray-600 disabled:cursor-not-allowed text-black font-semibold rounded-xl px-6 py-3 shadow-lg hover:shadow-cyan-500/50 transition-all duration-200 flex items-center justify-center space-x-2"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      <span>Decrypting...</span>
                    </>
                  ) : (
                    <>
                      <Unlock className="w-5 h-5" />
                      <span>Decrypt</span>
                    </>
                  )}
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handleClear}
                  className="px-6 py-3 bg-white/10 hover:bg-white/20 border border-white/20 text-gray-300 font-medium rounded-xl transition-all duration-200"
                >
                  Clear All
                </motion.button>
              </div>

              {/* Results Section */}
              {(outputText || error) && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                  className="space-y-4"
                >
                  <label className="block text-sm font-medium text-gray-300">
                    Result
                  </label>

                  {error ? (
                    <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-xl flex items-start space-x-3">
                      <AlertCircle className="w-5 h-5 text-red-400 mt-0.5 shrink-0" />
                      <div>
                        <p className="font-medium text-red-400">Decryption Failed</p>
                        <p className="text-red-300 text-sm mt-1">{error}</p>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      <div className="p-4 bg-green-500/10 border border-green-500/30 rounded-xl flex items-start space-x-3">
                        <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 shrink-0" />
                        <div className="flex-1">
                          <p className="font-medium text-green-400">Decryption Successful</p>
                          <p className="text-green-300 text-sm mt-1">Cipher pattern detected and decrypted</p>
                        </div>
                      </div>

                      <div className="relative">
                        <textarea
                          value={outputText}
                          readOnly
                          rows={4}
                          className="w-full bg-white/5 border border-green-400/30 rounded-xl px-4 py-3 text-white resize-none"
                        />
                        <button
                          onClick={() => navigator.clipboard.writeText(outputText)}
                          className="absolute top-3 right-3 p-2 bg-white/10 hover:bg-white/20 border border-white/20 rounded-lg transition-colors"
                        >
                          <Copy className="w-4 h-4 text-gray-400" />
                        </button>
                      </div>
                    </div>
                  )}
                </motion.div>
              )}
            </div>
          </motion.div>

          {/* Help Text */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="text-center mt-8"
          >
            <p className="text-gray-500 text-sm">
              Tip: Try entering some text or select a specific cipher type for better results
            </p>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default DecryptPage
