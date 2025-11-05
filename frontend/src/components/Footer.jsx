import { motion } from 'framer-motion'
import { Github, Twitter, Linkedin, Mail, Shield } from 'lucide-react'

const Footer = () => {
  const socialLinks = [
    { icon: Github, href: '#', label: 'GitHub' },
    { icon: Twitter, href: '#', label: 'Twitter' },
    { icon: Linkedin, href: '#', label: 'LinkedIn' },
    { icon: Mail, href: '#', label: 'Email' }
  ]

  return (
    <footer className="bg-black/20 border-t border-white/10 backdrop-blur-lg">
      <div className="max-w-7xl mx-auto px-6 py-3">
        <div className="py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Brand Section */}
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <motion.div
                  whileHover={{ rotate: 360 }}
                  transition={{ duration: 0.5 }}
                  className="p-2 rounded-lg bg-white/10 border border-cyan-400/30"
                >
                  <Shield className="w-6 h-6 text-cyan-400" />
                </motion.div>
                <span className="text-xl font-bold text-white">
                  CipherX
                </span>
              </div>
              <p className="text-gray-400 text-sm leading-relaxed">
                Advanced AI-powered cipher detection and decryption platform. 
                Unlock the secrets of encrypted messages with cutting-edge technology.
              </p>
            </div>

            {/* Quick Links */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-white">Quick Links</h3>
              <div className="space-y-2">
                {['Home', 'Decrypt', 'About', 'Documentation', 'Support'].map((link) => (
                  <motion.a
                    key={link}
                    href="#"
                    whileHover={{ x: 5 }}
                    className="block text-gray-400 hover:text-cyan-400 transition-colors text-sm"
                  >
                    {link}
                  </motion.a>
                ))}
              </div>
            </div>

            {/* Social Links */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-white">Connect</h3>
              <div className="flex space-x-4">
                {socialLinks.map((social) => (
                  <motion.a
                    key={social.label}
                    href={social.href}
                    whileHover={{ scale: 1.1, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                    className="p-3 rounded-lg bg-white/5 border border-white/10 hover:border-cyan-400/40 hover:bg-cyan-400/10 transition-all duration-200 group"
                    aria-label={social.label}
                  >
                    <social.icon className="w-5 h-5 text-gray-400 group-hover:text-cyan-400 transition-colors" />
                  </motion.a>
                ))}
              </div>
              <p className="text-gray-500 text-sm">
                Follow us for updates and cybersecurity insights
              </p>
            </div>
          </div>

          {/* Bottom Section */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="border-t border-white/10 mt-8 pt-8"
          >
            <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
              <div className="flex items-center space-x-4 text-sm text-gray-500">
                <span>© 2025 CipherX — All Rights Reserved</span>
                <span className="hidden md:inline">•</span>
                <a href="#" className="hover:text-cyan-400 transition-colors">Privacy Policy</a>
                <span className="hidden md:inline">•</span>
                <a href="#" className="hover:text-cyan-400 transition-colors">Terms of Service</a>
              </div>
              
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <span>Made with</span>
                <motion.span
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                  className="text-red-400"
                >
                  ♥
                </motion.span>
                <span>for cybersecurity</span>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
