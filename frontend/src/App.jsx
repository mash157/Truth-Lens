import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Navbar from './components/Navbar';
import Footer from './components/Footer';
import useTheme from './hooks/useTheme';

import Home from './pages/Home';
import Analyze from './pages/Analyze';
import Dashboard from './pages/Dashboard';
import Research from './pages/Research';
import HowItWorks from './pages/HowItWorks';
import Model from './pages/Model';

function NotFound() {
  return (
    <div
      className="container"
      style={{
        minHeight: '70vh',
        display: 'grid',
        placeItems: 'center',
        textAlign: 'center',
      }}
    >
      <div>
        <h1 style={{ color: 'var(--text-primary)' }}>404</h1>
        <p style={{ color: 'var(--text-secondary)' }}>
          The page you're looking for doesn't exist.
        </p>
      </div>
    </div>
  );
}

function App() {
  const { theme, toggleTheme } = useTheme();

  return (
    <BrowserRouter>
      <div
        style={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          background: 'var(--bg-primary)',
        }}
      >
        <Navbar theme={theme} toggleTheme={toggleTheme} />

        <main style={{ flex: 1 }} className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/analyze" element={<Analyze />} />
            <Route path="/research" element={<Research />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/how-it-works" element={<HowItWorks />} />
            <Route path="/model" element={<Model />} />

            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>

        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;