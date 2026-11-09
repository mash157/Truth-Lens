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
            <span className="bar-rank">{i + 1}</span>
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
    <div className="feature-importance">
      <h3 className="feature-heading">
        Why did the model classify this article this way?
      </h3>
      <p className="feature-sub">
        Features are ranked by their contribution weight (TF-IDF value × model
        coefficient).
      </p>

      {supporting.length > 0 && (
        <div className="feature-group">
          <h4 className="feature-group-title genuine">Supporting Features</h4>
          {renderBars(supporting, 'fill-genuine')}
        </div>
      )}

      {opposing.length > 0 && (
        <div className="feature-group">
          <h4 className="feature-group-title fake">Opposing Features</h4>
          {renderBars(opposing, 'fill-fake')}
        </div>
      )}

      {supporting.length === 0 && opposing.length === 0 && (
        <p className="feature-empty">
          No feature contributions available for this text.
        </p>
      )}
    </div>
  );
}
