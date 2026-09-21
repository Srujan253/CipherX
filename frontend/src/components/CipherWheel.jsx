import React from 'react'
import { motion } from 'framer-motion'

const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')

const CipherWheel = ({
  shift = 3,
  cipherName = 'Caesar Cipher',
  isIdentified = true,
  isSpinning = false,
}) => {
  const size = 380
  const center = size / 2
  const outerRadius = 142
  const innerRadius = 96
  const centerRadius = 32

  const anglePerStep = 360 / 26
  // Shift rotation: when decrypted, shift the inner alphabet
  const targetInnerRotation = -((shift || 0) % 26) * anglePerStep

  return (
    <div className="flex flex-col items-center justify-center p-2 select-none">
      <div className="relative flex items-center justify-center">
        <svg
          width={size}
          height={size}
          viewBox={`0 0 ${size} ${size}`}
          className="overflow-visible"
        >
          {/* Static background guidelines */}
          <circle
            cx={center}
            cy={center}
            r={outerRadius + 18}
            fill="none"
            stroke="#dfd7c6"
            strokeWidth="1.5"
          />
          <circle
            cx={center}
            cy={center}
            r={outerRadius + 8}
            fill="none"
            stroke="#c8bfae"
            strokeWidth="1"
            strokeDasharray="2 4"
          />

          {/* Group centered at (center, center) so all rotations are strictly concentric around (0, 0) */}
          <g transform={`translate(${center}, ${center})`}>
            
            {/* ================= OUTER RING (Clockwise / Left to Right) ================= */}
            <motion.g
              animate={
                isSpinning
                  ? { rotate: 360 }
                  : { rotate: 0 }
              }
              transition={
                isSpinning
                  ? { repeat: Infinity, ease: 'linear', duration: 3.5 }
                  : { duration: 0.6, ease: 'easeOut' }
              }
            >
              {/* Outer Ring Background Track */}
              <circle
                cx="0"
                cy="0"
                r={outerRadius}
                fill="#f8f3e5"
                stroke="#c8bfae"
                strokeWidth="1.5"
              />
              <circle
                cx="0"
                cy="0"
                r={innerRadius + 22}
                fill="#efe7d4"
                stroke="#c5bca9"
                strokeWidth="1.2"
              />

              {/* Outer Tick Marks & Letters */}
              {ALPHABET.map((letter, i) => {
                const angleDeg = i * anglePerStep - 90
                const angleRad = angleDeg * (Math.PI / 180)
                const x1 = (outerRadius - 14) * Math.cos(angleRad)
                const y1 = (outerRadius - 14) * Math.sin(angleRad)
                const x2 = (outerRadius - 8) * Math.cos(angleRad)
                const y2 = (outerRadius - 8) * Math.sin(angleRad)
                const tx = (outerRadius + 1) * Math.cos(angleRad)
                const ty = (outerRadius + 1) * Math.sin(angleRad)

                return (
                  <g key={`outer-${letter}`}>
                    <line
                      x1={x1}
                      y1={y1}
                      x2={x2}
                      y2={y2}
                      stroke="#b5a995"
                      strokeWidth="1"
                    />
                    <text
                      x={tx}
                      y={ty}
                      textAnchor="middle"
                      dominantBaseline="central"
                      fill="#2b2621"
                      fontSize="12"
                      fontFamily="'Courier Prime', 'Space Mono', monospace"
                      fontWeight="600"
                    >
                      {letter}
                    </text>
                  </g>
                )
              })}
            </motion.g>

            {/* ================= INNER RING (Counter-Clockwise / Right to Left) ================= */}
            <motion.g
              animate={
                isSpinning
                  ? { rotate: -360 }
                  : { rotate: targetInnerRotation }
              }
              transition={
                isSpinning
                  ? { repeat: Infinity, ease: 'linear', duration: 2.8 }
                  : { type: 'spring', stiffness: 55, damping: 13 }
              }
            >
              {/* Inner Ring Body */}
              <circle
                cx="0"
                cy="0"
                r={innerRadius + 18}
                fill="#f5eedc"
                stroke="#c0b5a1"
                strokeWidth="1.5"
              />
              <circle
                cx="0"
                cy="0"
                r={centerRadius + 16}
                fill="#ece3ce"
                stroke="#d3c8b4"
                strokeWidth="1"
              />

              {/* Inner Letters (Deep Crimson) */}
              {ALPHABET.map((letter, i) => {
                const angleDeg = i * anglePerStep - 90
                const angleRad = angleDeg * (Math.PI / 180)
                const tx = (innerRadius - 2) * Math.cos(angleRad)
                const ty = (innerRadius - 2) * Math.sin(angleRad)

                return (
                  <g key={`inner-${letter}`}>
                    <text
                      x={tx}
                      y={ty}
                      textAnchor="middle"
                      dominantBaseline="central"
                      fill="#7e221d"
                      fontSize="11.5"
                      fontFamily="'Courier Prime', 'Space Mono', monospace"
                      fontWeight="700"
                    >
                      {letter}
                    </text>
                  </g>
                )
              })}
            </motion.g>

            {/* ================= MIDDLE / CENTER SEAL ================= */}
            <motion.g
              animate={
                isSpinning
                  ? { scale: [1, 1.1, 1], rotate: 360 }
                  : { scale: 1, rotate: 0 }
              }
              transition={
                isSpinning
                  ? {
                      scale: { repeat: Infinity, duration: 1.2, ease: 'easeInOut' },
                      rotate: { repeat: Infinity, duration: 4, ease: 'linear' },
                    }
                  : { type: 'spring', stiffness: 120, damping: 12 }
              }
            >
              {/* Outer seal border */}
              <circle
                cx="0"
                cy="0"
                r={centerRadius}
                fill="#fbf7ed"
                stroke="#7e221d"
                strokeWidth="2"
              />
              <circle
                cx="0"
                cy="0"
                r={centerRadius - 4}
                fill="none"
                stroke="#7e221d"
                strokeWidth="0.8"
                strokeDasharray="2.5 2.5"
              />

              {/* Icon inside seal */}
              {isSpinning ? (
                // Scanning radar / decrypting crosshair while spinning
                <g>
                  <circle cx="0" cy="0" r="10" fill="none" stroke="#7e221d" strokeWidth="1.2" />
                  <line x1="-14" y1="0" x2="14" y2="0" stroke="#7e221d" strokeWidth="1" strokeDasharray="2 2" />
                  <line x1="0" y1="-14" x2="0" y2="14" stroke="#7e221d" strokeWidth="1" strokeDasharray="2 2" />
                </g>
              ) : isIdentified ? (
                <text
                  x="0"
                  y="1"
                  textAnchor="middle"
                  dominantBaseline="central"
                  fill="#7e221d"
                  fontSize="21"
                  fontFamily="'Courier Prime', monospace"
                  fontWeight="bold"
                >
                  ✓
                </text>
              ) : (
                <text
                  x="0"
                  y="1"
                  textAnchor="middle"
                  dominantBaseline="central"
                  fill="#6d6457"
                  fontSize="13"
                  fontFamily="'Courier Prime', monospace"
                >
                  {shift > 0 ? `+${shift}` : '—'}
                </text>
              )}
            </motion.g>

          </g>
        </svg>
      </div>

      {/* Label underneath: detected: [Cipher Name] */}
      <div className="mt-4 text-center">
        <p className="font-typewriter text-xs sm:text-sm tracking-wider text-[#4a4237]">
          detected:{' '}
          <span className="font-bold text-[#7e221d] ml-1">
            {isSpinning
              ? 'Analyzing ciphertext patterns...'
              : cipherName || 'Caesar Cipher'}
          </span>
          {!isSpinning && shift > 0 && (
            <span className="text-xs text-[#6e6456] ml-2">
              (Shift: {shift})
            </span>
          )}
        </p>
      </div>
    </div>
  )
}

export default CipherWheel
