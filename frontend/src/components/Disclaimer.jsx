import { AlertTriangle } from 'lucide-react';

const DISCLAIMER_TITLE = 'Important Notice';
const DISCLAIMER_TEXT =
  'TruthLens provides machine-learning-based classification using patterns learned from labelled training data. ' +
  'It does not independently verify factual claims. Predictions may be incorrect, so important information ' +
  'should always be verified using reliable independent sources.';

/**
 * Disclaimer card — homepage full version.
 * compact prop kept for backward compatibility (used on other pages).
 */
export default function Disclaimer({ compact = false }) {
  if (compact) {
    return (
      <div className="disclaimer is-compact">
        <AlertTriangle className="disclaimer-icon" size={16} aria-hidden="true" />
        <p className="disclaimer-text">{DISCLAIMER_TEXT}</p>
      </div>
    );
  }

  return (
    <div className="disclaimer-card" role="note" aria-label="Important disclaimer">
      {/* Icon container */}
      <div className="disclaimer-card-icon" aria-hidden="true">
        <AlertTriangle size={22} strokeWidth={2.2} />
      </div>

      {/* Text body */}
      <div className="disclaimer-card-body">
        <p className="disclaimer-card-title">{DISCLAIMER_TITLE}</p>
        <p className="disclaimer-card-text">{DISCLAIMER_TEXT}</p>
      </div>
    </div>
  );
}
