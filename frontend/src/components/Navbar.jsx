import { motion } from 'framer-motion'
import { Link, useLocation } from 'react-router-dom'

const Navbar = () => {
  const location = useLocation()

  return (
    <header className="relative w-full border-b border-[#d6cdba] bg-[#f4eedb] select-none z-30">
      {/* Dangling Retro Mini Mascot hanging from top rim */}
      <div className="absolute left-1/2 -translate-x-1/2 -top-1 pointer-events-none z-40">
        <motion.div
          animate={{ y: [0, 3, 0], rotate: [-1, 1.5, -1] }}
          transition={{ repeat: Infinity, duration: 4, ease: 'easeInOut' }}
          className="flex flex-col items-center"
        >
          {/* Subtle string/hook line */}
          <div className="w-[1.5px] h-3 bg-[#8c8273]"></div>
          {/* Stylized dangling Luffy-style pirate character SVG */}
          <svg width="28" height="34" viewBox="0 0 28 34" fill="none">
            {/* Straw Hat */}
            <ellipse cx="14" cy="9" rx="12" ry="3.5" fill="#facc15" stroke="#ca8a04" strokeWidth="1" />
            <path d="M7 8 C7 4, 21 4, 21 8" fill="#eab308" />
            <rect x="7" y="7" width="14" height="2" fill="#dc2626" />
            {/* Head */}
            <circle cx="14" cy="13" rx="5" ry="5" fill="#fed7aa" />
            {/* Eyes and grin */}
            <circle cx="12" cy="12" r="0.8" fill="#1c1917" />
            <circle cx="16" cy="12" r="0.8" fill="#1c1917" />
            <path d="M12 15 Q14 17 16 15" stroke="#1c1917" strokeWidth="0.8" fill="none" />
            {/* Red Vest / Body */}
            <rect x="10.5" y="17" width="7" height="8" rx="2" fill="#dc2626" />
            {/* Arms holding the rope */}
            <path d="M11 18 L13 2" stroke="#fed7aa" strokeWidth="2" strokeLinecap="round" />
            <path d="M17 18 L15 2" stroke="#fed7aa" strokeWidth="2" strokeLinecap="round" />
            {/* Blue shorts */}
            <rect x="11" y="24" width="6" height="4" fill="#2563eb" />
            {/* Little legs dangling */}
            <path d="M12 28 L11 32" stroke="#fed7aa" strokeWidth="1.8" strokeLinecap="round" />
            <path d="M16 28 L17 32" stroke="#fed7aa" strokeWidth="1.8" strokeLinecap="round" />
          </svg>
        </motion.div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
        {/* Left Side: Vintage Stamp Logo + CipherX + Subtitle */}
        <Link to="/" className="flex items-center space-x-3.5 group">
          {/* Double-circle (X) Stamp */}
          <div className="relative w-10 h-10 rounded-full border-2 border-[#7e221d] flex items-center justify-center p-[2px] transition-transform duration-300 group-hover:scale-105">
            <div className="w-full h-full rounded-full border border-dashed border-[#7e221d] flex items-center justify-center bg-[#f7f2e5]">
              <span className="font-serif-vintage font-black text-[#7e221d] text-lg leading-none">
                X
              </span>
            </div>
          </div>

          <div>
            <h1 className="font-serif-vintage font-bold text-2xl tracking-wide text-[#7e221d] leading-none">
              CipherX
            </h1>
            <p className="font-typewriter text-[10px] tracking-[0.2em] uppercase text-[#6d6457] mt-0.5">
              Classical Cipher Auto-Decryption
            </p>
          </div>
        </Link>

        {/* Right Side: Typewriter navigation */}
        <nav className="flex items-center space-x-6">
          <Link
            to="/decrypt"
            className={`font-typewriter text-xs uppercase tracking-widest px-3 py-1.5 rounded transition-all ${
              location.pathname === '/decrypt'
                ? 'bg-[#7e221d] text-[#faf6ee] font-bold shadow-xs'
                : 'text-[#52493d] hover:text-[#7e221d] hover:bg-[#eae1cd]'
            }`}
          >
            [ Decryptor ]
          </Link>
          <Link
            to="/"
            className={`font-typewriter text-xs uppercase tracking-widest px-3 py-1.5 rounded transition-all ${
              location.pathname === '/'
                ? 'bg-[#7e221d] text-[#faf6ee] font-bold shadow-xs'
                : 'text-[#52493d] hover:text-[#7e221d] hover:bg-[#eae1cd]'
            }`}
          >
            [ Home ]
          </Link>
          <a
            href="https://github.com/Srujan253/CipherX"
            target="_blank"
            rel="noreferrer"
            className="font-typewriter text-xs uppercase tracking-widest text-[#52493d] hover:text-[#7e221d] px-2 py-1.5 transition-colors hidden sm:inline-block"
          >
            GitHub
          </a>
        </nav>
      </div>
    </header>
  )
}

export default Navbar
