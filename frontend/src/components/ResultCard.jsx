import ConfidenceMeter from './ConfidenceMeter';
import FeatureImportance from './FeatureImportance';
import Disclaimer from './Disclaimer';

export default function ResultCard({ result }) {
  if (!result) return null;
  const isGenuine = result.prediction === 'LIKELY_GENUINE';
  const borderClass = isGenuine ? 'border-genuine' : 'border-fake';
  const labelColor = isGenuine ? 'var(--accent-genuine)' : 'var(--accent-fake)';
  const labelBg = isGenuine ? 'var(--accent-genuine-glow)' : 'var(--accent-fake-glow)';

  return (
    <div className={`glass-card ${borderClass} fade-in`} style={{
      maxWidth: 720,
      margin: '32px auto',
    }}>
      {/* Prediction label */}
      <div style={{ textAlign: 'center', marginBottom: 20 }}>
        <span style={{
          display: 'inline-block',
          padding: '8px 28px',
          borderRadius: '24px',
          background: labelBg,
          color: labelColor,
          fontSize: '1.2rem',
          fontWeight: 800,
          letterSpacing: '0.06em',
          textTransform: 'uppercase',
        }}>
          {result.prediction.replace('_', ' ')}
        </span>
      </div>

      {/* Confidence */}
      <ConfidenceMeter confidence={result.confidence} prediction={result.prediction} />

      {/* Model & metadata */}
      <div style={{
        display: 'flex',
        gap: 24,
        marginTop: 20,
        flexWrap: 'wrap',
      }}>
        <div>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Model</span>
          <p style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{result.model_name}</p>
        </div>
        <div>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Words</span>
          <p style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{result.word_count?.toLocaleString()}</p>
        </div>
        <div>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>Characters</span>
          <p style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{result.character_count?.toLocaleString()}</p>
        </div>
      </div>

      {/* Feature Importance Explanation */}
      <FeatureImportance
        supporting={result.supporting_features}
        opposing={result.opposing_features}
      />

      {/* Disclaimer */}
      <Disclaimer compact />
    </div>
  );
}
