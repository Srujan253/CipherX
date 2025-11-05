import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Landing from './pages/LandingPage'
import Decrypt from './pages/DecryptPage'
import Footer from './components/Footer'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-linear-to-br from-slate-900 via-slate-800 to-slate-900 overflow-x-hidden">
        <Navbar />
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/decrypt" element={<Decrypt />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  )
}

export default App
