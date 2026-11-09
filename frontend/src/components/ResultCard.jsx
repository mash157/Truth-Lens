import ConfidenceMeter from './ConfidenceMeter';
import FeatureImportance from './FeatureImportance';
import Disclaimer from './Disclaimer';
import WebEvidence from './WebEvidence';

export default function ResultCard({ result, title, articleText }) {
  if (!result) return null;
  const isGenuine = result.prediction === 'LIKELY_GENUINE';
  const isUncertain = result.prediction === 'UNCERTAIN';
  const isFake = result.prediction === 'LIKELY_FAKE';
  
  const borderClass = isUncertain ? 'border-ambiguous' : (isGenuine ? 'border-genuine' : 'border-fake');
  const labelColor = isUncertain ? 'var(--accent-ambiguous)' : (isGenuine ? 'var(--accent-genuine)' : 'var(--accent-fake)');
  const labelBg = isUncertain ? 'var(--accent-ambiguous-glow, rgba(245,158,11,0.12))' : (isGenuine ? 'var(--accent-genuine-glow)' : 'var(--accent-fake-glow)');

  return (
    <div className={`glass-card result-card ${borderClass} fade-in`}>
      {/* Prediction label */}
      <div className="result-prediction-wrap">
        <span
          className="result-prediction"
          style={{ background: labelBg, color: labelColor }}
        >
          {result.prediction.replace('_', ' ')}
        </span>
      </div>

      {/* Confidence */}
      <ConfidenceMeter
        confidence={result.confidence}
        prediction={result.prediction}
      />

      {/* Uncertainty Notice */}
      {result.uncertainty && (
        <div style={{
          marginTop: 16,
          padding: '14px 18px',
          borderRadius: 10,
          background: 'rgba(245, 158, 11, 0.08)',
          border: '1px solid rgba(245, 158, 11, 0.25)',
          borderLeft: '4px solid var(--accent-ambiguous)',
        }}>
          <p style={{
            fontSize: '0.85rem',
            fontWeight: 600,
            color: 'var(--accent-ambiguous)',
            margin: '0 0 6px',
          }}>
            ⚠ Model Uncertain
          </p>
          <p style={{
            fontSize: '0.8rem',
            color: 'var(--text-secondary)',
            margin: 0,
            lineHeight: 1.55,
          }}>
            The model does not have sufficient confidence for a definitive classification.
            This does NOT mean the article is fake. Consider verifying with web sources
            or consulting additional fact-checking resources.
          </p>
        </div>
      )}

      {/* Model & metadata */}
      <div className="result-meta-grid">
        <div className="result-meta-block">
          <span className="result-meta-label">Model</span>
          <p className="result-meta-value">{result.model_name}</p>
        </div>
        <div className="result-meta-block">
          <span className="result-meta-label">Words</span>
          <p className="result-meta-value">
            {result.word_count?.toLocaleString()}
          </p>
        </div>
        <div className="result-meta-block">
          <span className="result-meta-label">Characters</span>
          <p className="result-meta-value">
            {result.character_count?.toLocaleString()}
          </p>
        </div>
      </div>

      {/* Feature Importance Explanation */}
      <FeatureImportance
        supporting={result.supporting_features}
        opposing={result.opposing_features}
      />

      {/* Disclaimer */}
      <Disclaimer compact />

      {/* Verify with Web */}
      <WebEvidence headline={title} articleText={articleText} />
    </div>
  );
}
