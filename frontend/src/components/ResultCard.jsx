import ConfidenceMeter from './ConfidenceMeter';
import FeatureImportance from './FeatureImportance';
import Disclaimer from './Disclaimer';
import WebEvidence from './WebEvidence';

export default function ResultCard({ result, title, articleText }) {
  if (!result) return null;
  const isGenuine = result.prediction === 'LIKELY_GENUINE';
  const borderClass = isGenuine ? 'border-genuine' : 'border-fake';
  const labelColor = isGenuine ? 'var(--accent-genuine)' : 'var(--accent-fake)';
  const labelBg = isGenuine ? 'var(--accent-genuine-glow)' : 'var(--accent-fake-glow)';

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
