import { useState, useEffect } from 'react';
import { Search, CheckCircle, XCircle, HelpCircle } from 'lucide-react';
import { api } from '../services/api';

export default function NewsInput({ onResult, onLoading, onError }) {
  const [title, setTitle] = useState('');
  const [text, setText] = useState('');
  const [samples, setSamples] = useState([]);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    api.getSampleArticles().then(setSamples).catch(() => {});
  }, []);

  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const charCount = text.length;
  const canSubmit = text.trim().length >= 10 && !submitting;

  const handleAnalyze = async () => {
    if (!canSubmit) return;
    setSubmitting(true);
    onLoading(true);
    onError(null);
    try {
      const result = await api.analyzeNews(title, text);
      onResult(result);
    } catch (err) {
      onError(err.detail || err.message || 'Analysis failed. Is the backend running?');
      onResult(null);
    } finally {
      setSubmitting(false);
      onLoading(false);
    }
  };

  const handleTryExample = (sample) => {
    setTitle(sample.title);
    setText(sample.text);
    onResult(null);
    onError(null);
  };

  const handleClear = () => {
    setTitle('');
    setText('');
    onResult(null);
    onError(null);
  };

  return (
    <div className="glass-card fade-in" style={{ maxWidth: 720, margin: '0 auto' }}>
      <h2 style={{
        fontSize: '1.3rem',
        fontWeight: 700,
        marginBottom: 20,
        color: 'var(--text-primary)',
      }}>Analyze a News Article</h2>

      {/* Headline */}
      <label style={{ display: 'block', marginBottom: 6, fontSize: '0.88rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
        Headline <span style={{ fontWeight: 400, color: 'var(--text-muted)' }}>(optional)</span>
      </label>
      <input
        className="input-field"
        type="text"
        placeholder="Enter the headline or title…"
        value={title}
        onChange={e => setTitle(e.target.value)}
        style={{ marginBottom: 16 }}
      />

      {/* Article body */}
      <label style={{ display: 'block', marginBottom: 6, fontSize: '0.88rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
        Article Content <span style={{ color: 'var(--accent-fake)', fontWeight: 400 }}>*</span>
      </label>
      <textarea
        className="input-field"
        placeholder="Paste or type the article text here (minimum 10 characters)…"
        value={text}
        onChange={e => setText(e.target.value)}
        rows={8}
        style={{ resize: 'vertical', marginBottom: 8 }}
      />

      {/* Counters */}
      <div style={{ display: 'flex', gap: 16, fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: 16 }}>
        <span>{wordCount} words</span>
        <span>{charCount} characters</span>
      </div>

      {/* Actions */}
      <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
        <button className="btn btn-primary" onClick={handleAnalyze} disabled={!canSubmit}>
          {submitting ? 'Analyzing...' : <><Search size={16} /> Analyze</>}
        </button>
        <button className="btn btn-secondary" onClick={handleClear}>Clear</button>
      </div>

      {/* Sample articles */}
      {samples.length > 0 && (
        <div style={{ marginTop: 24, borderTop: '1px solid var(--border-color)', paddingTop: 16 }}>
          <p style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: 10 }}>
            Try a Demo Example
          </p>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {samples.map(s => (
              <button
                key={s.id}
                className="btn btn-secondary"
                onClick={() => handleTryExample(s)}
                style={{ fontSize: '0.78rem', padding: '6px 14px' }}
              >
                {s.label.includes('GENUINE') ? <CheckCircle size={14} style={{ color: 'var(--accent-genuine)' }} /> : s.label.includes('FAKE') ? <XCircle size={14} style={{ color: 'var(--accent-fake)' }} /> : <HelpCircle size={14} style={{ color: 'var(--accent-ambiguous)' }} />}{' '}
                {s.label.includes('GENUINE') ? 'Genuine Demo' : s.label.includes('FAKE') ? 'Fake Demo' : 'Ambiguous Demo'}
              </button>
            ))}
          </div>
          <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontStyle: 'italic', marginTop: 8 }}>
            DEMO ARTICLES — FOR SYSTEM TESTING ONLY
          </p>
        </div>
      )}
    </div>
  );
}
