import { formatPercentage } from '../utils/formatters';

export default function ConfidenceMeter({ confidence, prediction }) {
  const percent = (confidence * 100).toFixed(1);
  const isGenuine = prediction === 'LIKELY_GENUINE';
  const isUncertain = prediction === 'UNCERTAIN';
  
  const color = isUncertain ? 'var(--accent-ambiguous)' : (isGenuine ? 'var(--accent-genuine)' : 'var(--accent-fake)');
  const gradientEnd = isUncertain ? '#f59e0b' : (isGenuine ? '#2dd4bf' : '#fb7185');

  return (
    <div style={{ marginTop: 16 }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'baseline',
        marginBottom: 8,
      }}>
        <span style={{
          fontSize: '0.85rem',
          fontWeight: 600,
          color: 'var(--text-secondary)',
          textTransform: 'uppercase',
          letterSpacing: '0.04em',
        }}>Model Confidence</span>
        <span style={{
          fontSize: '1.6rem',
          fontWeight: 800,
          color: color,
        }}>{percent}%</span>
      </div>

      {/* Track */}
      <div style={{
        height: 10,
        background: 'var(--bg-tertiary)',
        borderRadius: 5,
        overflow: 'hidden',
      }}>
        <div style={{
          height: '100%',
          width: `${percent}%`,
          background: `linear-gradient(90deg, ${color}, ${gradientEnd})`,
          borderRadius: 5,
          transition: 'width 0.8s cubic-bezier(0.4, 0, 0.2, 1)',
        }} />
      </div>

      <p style={{
        fontSize: '0.75rem',
        color: 'var(--text-muted)',
        marginTop: 8,
        fontStyle: 'italic',
      }}>
        {isUncertain
          ? 'The model lacks sufficient confidence for a definitive classification. UNCERTAIN does NOT mean the article is fake — it means more verification is recommended.'
          : 'Model confidence represents how strongly the classifier supports its predicted class. It does not guarantee factual correctness.'
        }
      </p>
    </div>
  );
}
