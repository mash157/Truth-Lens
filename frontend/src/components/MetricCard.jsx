export default function MetricCard({ label, value, icon, color }) {
  return (
    <div className="glass-card" style={{ textAlign: 'center', padding: '20px 16px' }}>
      <span style={{ fontSize: '1.6rem', display: 'block', marginBottom: 6 }}>{icon}</span>
      <span style={{
        fontSize: '1.8rem',
        fontWeight: 800,
        color: color || 'var(--primary)',
        display: 'block',
      }}>{value}</span>
      <span style={{
        fontSize: '0.8rem',
        color: 'var(--text-muted)',
        fontWeight: 500,
        textTransform: 'uppercase',
        letterSpacing: '0.04em',
      }}>{label}</span>
    </div>
  );
}
