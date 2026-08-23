export default function Footer() {
  return (
    <footer
      style={{
        borderTop: '1px solid var(--border-color)',
        padding: '24px 24px',
        textAlign: 'center',
        marginTop: 64,
      }}
    >
      <div style={{ maxWidth: 1200, margin: '0 auto' }}>
        <p
          style={{
            fontSize: '0.88rem',
            color: 'var(--text-secondary)',
            lineHeight: 1.7,
            margin: 0,
          }}
        >
          Made With ❤️ by{' '}
          <span
            style={{
              fontWeight: 700,
              color: 'var(--primary)',
            }}
          >
            @mash157
          </span>
        </p>
        <p
          style={{
            fontSize: '0.78rem',
            color: 'var(--text-muted)',
            marginTop: 6,
            margin: '6px 0 0',
          }}
        >
          © All Rights Reserved 2026
        </p>
      </div>
    </footer>
  );
}
