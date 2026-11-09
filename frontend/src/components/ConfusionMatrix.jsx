import { api } from '../services/api';

export default function ConfusionMatrix() {
  return (
    <div style={{ textAlign: 'center' }}>
      <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: 16 }}>
        Confusion Matrix
      </h3>
      <img
        src={api.getConfusionMatrixUrl()}
        alt="Confusion Matrix"
        style={{
          maxWidth: '100%',
          width: 420,
          borderRadius: 12,
          border: '1px solid var(--border-color)',
          boxShadow: 'var(--shadow-md)',
        }}
        onError={e => { e.target.style.display = 'none'; }}
      />
    </div>
  );
}
