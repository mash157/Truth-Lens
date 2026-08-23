import { Sun, Moon } from 'lucide-react';

export default function ThemeToggle({ theme, toggleTheme }) {
  const isDark = theme === 'dark';

  return (
    <button
      onClick={toggleTheme}
      role="switch"
      aria-checked={isDark}
      aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
      title={`Switch to ${isDark ? 'light' : 'dark'} mode`}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 0,
        padding: '3px 4px',
        borderRadius: 999,
        border: '1px solid var(--border-color)',
        background: 'var(--bg-tertiary)',
        cursor: 'pointer',
        position: 'relative',
        height: 32,
        minWidth: 100,
        transition: 'background-color 0.2s ease, border-color 0.2s ease',
        outline: 'none',
      }}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggleTheme();
        }
      }}
      onFocus={(e) => {
        e.currentTarget.style.boxShadow = '0 0 0 3px var(--primary-glow)';
      }}
      onBlur={(e) => {
        e.currentTarget.style.boxShadow = 'none';
      }}
    >
      {/* Light label + icon */}
      <span
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 4,
          padding: '2px 8px',
          borderRadius: 999,
          fontSize: '0.7rem',
          fontWeight: isDark ? 500 : 700,
          color: isDark ? 'var(--text-muted)' : 'var(--primary)',
          transition: 'color 0.2s ease',
          zIndex: 1,
          whiteSpace: 'nowrap',
        }}
      >
        <Sun size={13} strokeWidth={isDark ? 1.5 : 2.5} />
        <span>Light</span>
      </span>

      {/* Dark label + icon */}
      <span
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 4,
          padding: '2px 8px',
          borderRadius: 999,
          fontSize: '0.7rem',
          fontWeight: isDark ? 700 : 500,
          color: isDark ? 'var(--primary)' : 'var(--text-muted)',
          transition: 'color 0.2s ease',
          zIndex: 1,
          whiteSpace: 'nowrap',
        }}
      >
        <span>Dark</span>
        <Moon size={13} strokeWidth={isDark ? 2.5 : 1.5} />
      </span>

      {/* Sliding knob */}
      <span
        style={{
          position: 'absolute',
          top: 3,
          left: isDark ? 'calc(50% - 2px)' : 3,
          width: 'calc(50% - 2px)',
          height: 24,
          borderRadius: 999,
          background: 'var(--primary)',
          opacity: 0.18,
          transition: 'left 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
          pointerEvents: 'none',
        }}
      />
    </button>
  );
}
