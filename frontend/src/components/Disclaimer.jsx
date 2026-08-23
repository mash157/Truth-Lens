import { AlertTriangle } from 'lucide-react';
import { RESEARCH_DISCLAIMER } from '../utils/constants';

export default function Disclaimer({ compact = false }) {
  return (
    <div style={{
      padding: compact ? '12px 16px' : '20px 24px',
      borderRadius: '12px',
      background: 'var(--bg-tertiary)',
      border: '1px solid var(--border-color)',
      borderLeft: '4px solid var(--accent-ambiguous)',
      marginTop: compact ? '12px' : '24px',
      display: 'flex',
      alignItems: compact ? 'center' : 'flex-start',
      gap: 10,
    }}>
      <AlertTriangle
        size={compact ? 14 : 18}
        style={{ color: 'var(--accent-ambiguous)', flexShrink: 0, marginTop: compact ? 0 : 2 }}
      />
      <p style={{
        fontSize: compact ? '0.78rem' : '0.85rem',
        lineHeight: 1.6,
        color: 'var(--text-secondary)',
        fontStyle: 'italic',
        margin: 0,
      }}>
        {RESEARCH_DISCLAIMER}
      </p>
    </div>
  );
}
