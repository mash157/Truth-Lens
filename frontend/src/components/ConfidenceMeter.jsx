export default function ConfidenceMeter({ confidence, prediction }) {
  const percent = (confidence * 100).toFixed(1);
  const isGenuine = prediction === 'LIKELY_GENUINE';
  const color = isGenuine ? 'var(--accent-genuine)' : 'var(--accent-fake)';

  return (
    <div className="confidence-meter">
      <div className="confidence-head">
        <span className="confidence-label">Model Confidence</span>
        <span className="confidence-value" style={{ color }}>
          {percent}%
        </span>
      </div>

      <div
        className="confidence-track"
        role="progressbar"
        aria-label="Model confidence"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={Number(percent)}
      >
        <div
          className="confidence-fill"
          style={{
            width: `${percent}%`,
            background: `linear-gradient(90deg, ${color}, ${isGenuine ? '#2dd4bf' : '#fb7185'})`,
          }}
        />
      </div>

      <p className="confidence-note">
        Model confidence represents how strongly the classifier supports its
        predicted class. It does not guarantee factual correctness.
      </p>
    </div>
  );
}
