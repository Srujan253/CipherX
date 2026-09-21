import { Github, Mail } from 'lucide-react'
import { Link } from 'react-router-dom'

const Footer = () => {
  return (
    <footer className="w-full bg-[#ede5d0] border-t border-[#d6cdba] text-[#52493d] font-typewriter py-6 mt-10">
      <div className="max-w-7xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs">
        <div className="flex items-center space-x-2">
          <span className="font-serif-vintage font-bold text-[#7e221d] text-sm">CipherX</span>
          <span>— Classical Cryptographic Auto-Decryption Engine</span>
        </div>

        <div className="flex items-center space-x-6">
          <Link to="/" className="hover:text-[#7e221d] transition-colors">
            Home
          </Link>
          <Link to="/decrypt" className="hover:text-[#7e221d] transition-colors">
            Decryptor
          </Link>
          <a
            href="https://github.com/Srujan253/CipherX"
            target="_blank"
            rel="noreferrer"
            className="flex items-center space-x-1 hover:text-[#7e221d] transition-colors"
          >
            <Github className="w-3.5 h-3.5" />
            <span>Repository</span>
          </a>
        </div>
      </div>
    </footer>
  )
}

export default Footer
