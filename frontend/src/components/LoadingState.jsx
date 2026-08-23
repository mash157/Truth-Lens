export default function LoadingState({ message = 'Analyzing article...' }) {
  return (
    <div className="glass-card loading-glow fade-in" style={{
      textAlign: 'center',
      padding: '48px 32px',
      maxWidth: '500px',
      margin: '40px auto',
    }}>
      {/* Animated spinner */}
      <div style={{
        width: 48, height: 48,
        border: '3px solid var(--border-color)',
        borderTop: '3px solid var(--primary)',
        borderRadius: '50%',
        margin: '0 auto 20px',
        animation: 'spin 0.8s linear infinite',
      }} />

      <p style={{
        fontSize: '1.1rem',
        fontWeight: 600,
        color: 'var(--text-primary)',
        marginBottom: 8,
      }}>{message}</p>

      <p style={{
        fontSize: '0.85rem',
        color: 'var(--text-muted)',
      }}>Running NLP preprocessing and classification…</p>

      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
