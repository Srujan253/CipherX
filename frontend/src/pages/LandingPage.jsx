import { motion } from 'framer-motion'
import { ArrowRight, Key, Lock, Code, Shield, Zap, Eye } from 'lucide-react'
import { Link } from 'react-router-dom'

const LandingPage = () => {
  const features = [
    {
      icon: Shield,
      title: "AI-Powered Cipher Detection",
      description: "Advanced machine learning algorithms automatically identify cipher types for faster decryption."
    },
    {
      icon: Key,
      title: "Multiple Decryption Algorithms",
      description: "Support for Caesar, Vigenère, Atbash, Base64, and many more classical and modern ciphers."
    },
    {
      icon: Zap,
      title: "Real-Time Analysis Dashboard",
      description: "Get instant feedback and analysis on cipher patterns with our intuitive dashboard interface."
    }
  ]

  return (
    <div className="min-h-screen">

      {/* Hero Section */}
      <section className="min-h-screen flex items-center justify-center pt-20">
        <div className="max-w-7xl mx-auto px-6 py-3">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="space-y-8"
            >
              {/* Main Title */}
              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.4 }}
                className="text-4xl md:text-6xl lg:text-7xl font-bold leading-tight text-white"
              >
                <span className="block">Uncover Hidden Messages</span>
                <span className="block text-cyan-400">with CipherX</span>
              </motion.h1>

              {/* Subtitle */}
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.6 }}
                className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto leading-relaxed"
              >
                Decrypt classic and modern ciphers instantly using AI intelligence.
              </motion.p>

              {/* CTA Button */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.8 }}
                className="pt-8"
              >
                <Link
                  to="/decrypt"
                  className="group inline-flex items-center space-x-3 bg-cyan-500 hover:bg-cyan-400 text-black font-semibold text-lg px-8 py-4 rounded-xl shadow-lg hover:shadow-cyan-500/50 transition-all duration-300 transform hover:scale-105"
                >
                  <span>Try Decryptor</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Link>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-6 py-3">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Powerful Features
            </h2>
            <p className="text-lg text-gray-400 max-w-2xl mx-auto">
              Advanced cryptographic tools designed for professionals and enthusiasts
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                whileHover={{ y: -5 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="group p-8 rounded-xl bg-white/5 border border-white/10 backdrop-blur-lg hover:border-cyan-400/30 hover:bg-white/10 transition-all duration-300"
              >
                <div className="mb-6">
                  <div className="w-12 h-12 rounded-lg bg-white/10 border border-cyan-400/30 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <feature.icon className="w-6 h-6 text-cyan-400" />
                  </div>
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-400 leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}

export default LandingPage
