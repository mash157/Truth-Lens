import { Moon, Sun } from 'lucide-react';

export default function ThemeToggle({ theme, toggleTheme }) {
  const isDark = theme === 'dark';
  return (
    <button
      type="button"
      className={`theme-toggle ${isDark ? 'is-dark' : ''}`}
      onClick={toggleTheme}
      role="switch"
      aria-checked={isDark}
      aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
      title={`Switch to ${isDark ? 'light' : 'dark'} mode`}
    >
      <span className="theme-option theme-option-light"><Sun size={16} aria-hidden="true" /> Light</span>
      <span className="theme-option theme-option-dark"><Moon size={16} aria-hidden="true" /> Dark</span>
      <span className="theme-orb" aria-hidden="true" />
    </button>
  );
}
