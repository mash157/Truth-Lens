import { Link, useLocation } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { useEffect, useState } from 'react';
import ThemeToggle from './ThemeToggle';

const NAV_LINKS = [
  { to: '/', label: 'Home' }, { to: '/analyze', label: 'Analyze' },
  { to: '/dashboard', label: 'Dashboard' }, { to: '/research', label: 'Research' },
  { to: '/how-it-works', label: 'How It Works' }, { to: '/model', label: 'Model' },
];

export default function Navbar({ theme, toggleTheme }) {
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);
  useEffect(() => setMenuOpen(false), [location.pathname]);

  return (
    <nav className="site-nav glass" aria-label="Main navigation">
      <div className="nav-inner">
        <Link to="/" className="brand" aria-label="TruthLens Home">
          Truth<span>Lens</span>
        </Link>
        <div className="nav-desktop">
          {NAV_LINKS.map((link) => (
            <Link key={link.to} to={link.to} className={location.pathname === link.to ? 'active' : ''}>
              {link.label}
            </Link>
          ))}
          <ThemeToggle theme={theme} toggleTheme={toggleTheme} />
        </div>
        <div className="nav-mobile">
          <ThemeToggle theme={theme} toggleTheme={toggleTheme} />
          <button className="menu-button" onClick={() => setMenuOpen((open) => !open)} aria-label={menuOpen ? 'Close menu' : 'Open menu'} aria-expanded={menuOpen}>
            {menuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>
      {menuOpen && <div className="mobile-menu">
        {NAV_LINKS.map((link) => <Link key={link.to} to={link.to} className={location.pathname === link.to ? 'active' : ''}>{link.label}</Link>)}
      </div>}
    </nav>
  );
}
