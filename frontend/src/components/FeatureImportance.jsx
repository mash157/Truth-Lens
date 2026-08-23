export default function FeatureImportance({ supporting = [], opposing = [] }) {
  const maxWeight = Math.max(
    ...supporting.map(f => f.weight),
    ...opposing.map(f => f.weight),
    0.001
  );

  const renderBars = (features, fillClass) => (
    <div className="bar-chart-container">
      {features.map((f, i) => {
        const pct = Math.min((f.weight / maxWeight) * 100, 100);
        return (
          <div className="bar-row" key={i}>
            <span className="bar-label" title={f.word}>{f.word}</span>
            <div className="bar-track">
              <div className={`bar-fill ${fillClass}`} style={{ width: `${pct}%` }} />
            </div>
            <span className="bar-value">{f.weight.toFixed(3)}</span>
          </div>
        );
      })}
    </div>
  );

  return (
    <div style={{ marginTop: 24 }}>
      <h3 style={{
        fontSize: '1.05rem',
        fontWeight: 700,
        color: 'var(--text-primary)',
        marginBottom: 4,
      }}>Why did the model classify this article this way?</h3>
      <p style={{
        fontSize: '0.82rem',
        color: 'var(--text-muted)',
        marginBottom: 20,
      }}>Features are ranked by their contribution weight (TF-IDF value × model coefficient).</p>

      {supporting.length > 0 && (
        <div style={{ marginBottom: 28 }}>
          <h4 style={{
            fontSize: '0.9rem', fontWeight: 600,
            color: 'var(--text-secondary)', marginBottom: 8,
            textTransform: 'uppercase', letterSpacing: '0.04em',
          }}>Supporting Features</h4>
          {renderBars(supporting, 'fill-genuine')}
        </div>
      )}

      {opposing.length > 0 && (
        <div>
          <h4 style={{
            fontSize: '0.9rem', fontWeight: 600,
            color: 'var(--text-secondary)', marginBottom: 8,
            textTransform: 'uppercase', letterSpacing: '0.04em',
          }}>Opposing Features</h4>
          {renderBars(opposing, 'fill-fake')}
        </div>
      )}

      {supporting.length === 0 && opposing.length === 0 && (
        <p style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>
          No feature contributions available for this text.
        </p>
      )}
    </div>
  );
}
