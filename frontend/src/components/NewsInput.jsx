import { useState } from 'react';
import { Search, CheckCircle, XCircle, HelpCircle, ChevronRight, Globe } from 'lucide-react';
import { api } from '../services/api';
import { DEMO_ARTICLES } from '../data/demoArticles';

const TABS = [
  { key: 'genuine', label: 'Genuine', icon: CheckCircle, color: 'var(--accent-genuine)' },
  { key: 'fake', label: 'Fake', icon: XCircle, color: 'var(--accent-fake)' },
  { key: 'ambiguous', label: 'Ambiguous', icon: HelpCircle, color: 'var(--accent-ambiguous)' },
];

export default function NewsInput({ onResult, onLoading, onError, onInputChange, onWebResults }) {
  const [title, setTitle] = useState('');
  const [text, setText] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [demoTab, setDemoTab] = useState('genuine');

  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const charCount = text.length;
  const canSubmit = text.trim().length >= 10 && !submitting;

  const handleAnalyze = async () => {
    if (!canSubmit) return;
    setSubmitting(true);
    onLoading(true);
    onError(null);
    if (onInputChange) onInputChange({ title, text });
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

  const handleVerifyWithWeb = async () => {
    if (!canSubmit) return;
    setSubmitting(true);
    onLoading(true);
    onError(null);
    if (onInputChange) onInputChange({ title, text });
    try {
      const query = title.trim() || text.trim().slice(0, 120);
      const data = await api.searchNews(query, 5);
      if (onWebResults) onWebResults(data.results || []);
    } catch (err) {
      onError(err.detail || err.message || 'Web verification failed.');
    } finally {
      setSubmitting(false);
      onLoading(false);
    }
  };

  const handleTryExample = (article) => {
    setTitle(article.headline);
    setText(article.text);
    onResult(null);
    onError(null);
  };

  const handleClear = () => {
    setTitle('');
    setText('');
    onResult(null);
    onError(null);
  };

  const filteredDemos = DEMO_ARTICLES.filter(a => {
    if (demoTab === 'genuine') return a.expectedLabel === 'LIKELY_GENUINE';
    if (demoTab === 'fake') return a.expectedLabel === 'LIKELY_FAKE';
    return a.expectedBehavior === 'LOWER_CONFIDENCE';
  });

  return (
    <div className="glass-card analyze-input-card fade-in" style={{ maxWidth: 720, margin: '0 auto' }}>
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
        placeholder="Enter the headline or title..."
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
        placeholder="Paste or type the article text here (minimum 10 characters)..."
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
        <button
          className="btn btn-secondary"
          onClick={handleVerifyWithWeb}
          disabled={!canSubmit}
          style={{
            borderColor: 'var(--accent-web)',
            color: 'var(--accent-web)',
            background: 'var(--accent-web-glow)',
          }}
        >
          <Globe size={16} /> Verify with Web
        </button>
        <button className="btn btn-secondary" onClick={handleClear}>Clear</button>
      </div>

      {/* ── Demo Article Library ── */}
      <div style={{ marginTop: 28, borderTop: '1px solid var(--border-color)', paddingTop: 20 }}>
        {/* Demo Warning Banner */}
        <div style={{
          background: 'rgba(245, 158, 11, 0.08)',
          border: '1px solid rgba(245, 158, 11, 0.25)',
          borderRadius: 8,
          padding: '10px 14px',
          marginBottom: 16,
        }}>
          <p style={{
            fontSize: '0.82rem',
            fontWeight: 700,
            color: 'var(--accent-ambiguous)',
            margin: '0 0 4px',
          }}>Demo Testing Set</p>
          <p style={{
            fontSize: '0.75rem',
            color: 'var(--text-muted)',
            margin: 0,
            lineHeight: 1.45,
          }}>
            These examples are for testing the TruthLens model and UI. Expected labels are testing expectations and are not proof of factual truth.
          </p>
        </div>

        <h3 style={{
          fontSize: '1.05rem',
          fontWeight: 700,
          color: 'var(--text-primary)',
          marginBottom: 4,
        }}>Try a Demo Article</h3>
        <p style={{
          fontSize: '0.8rem',
          color: 'var(--text-muted)',
          marginBottom: 16,
        }}>
          Select a category, then click an article to populate the fields above.
        </p>

        {/* Category Tabs */}
        <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
          {TABS.map(tab => {
            const Icon = tab.icon;
            const isActive = demoTab === tab.key;
            return (
              <button
                key={tab.key}
                onClick={() => setDemoTab(tab.key)}
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 6,
                  padding: '7px 16px',
                  fontSize: '0.82rem',
                  fontWeight: 600,
                  borderRadius: 8,
                  border: `1px solid ${isActive ? tab.color : 'var(--border-color)'}`,
                  background: isActive ? `${tab.color}18` : 'transparent',
                  color: isActive ? tab.color : 'var(--text-secondary)',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                }}
              >
                <Icon size={14} />
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Demo Article Cards — Responsive Grid */}
        <div className="demo-grid">
          {filteredDemos.map(article => (
            <div
              key={article.id}
              className="glass-card demo-card"
              onClick={() => handleTryExample(article)}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6, flexWrap: 'wrap' }}>
                <span style={{
                  fontSize: '0.7rem',
                  fontWeight: 600,
                  color: 'var(--text-muted)',
                  textTransform: 'uppercase',
                  letterSpacing: '0.04em',
                }}>{article.category}</span>
                {article.sourceType === 'demo-test' && (
                  <span style={{
                    fontSize: '0.62rem',
                    fontWeight: 500,
                    color: 'var(--primary)',
                    background: 'var(--primary-glow)',
                    padding: '2px 6px',
                    borderRadius: 4,
                  }}>DEMO TEST</span>
                )}
              </div>
              <p style={{
                fontSize: '0.85rem',
                fontWeight: 600,
                color: 'var(--text-primary)',
                lineHeight: 1.35,
                margin: '0 0 10px',
                display: '-webkit-box',
                WebkitLineClamp: 2,
                WebkitBoxOrient: 'vertical',
                overflow: 'hidden',
              }}>{article.headline}</p>
              <button
                className="btn btn-secondary demo-use-btn"
              >
                Use This Example
                <ChevronRight size={12} />
              </button>
            </div>
          ))}
        </div>

        <p style={{
          fontSize: '0.72rem',
          color: 'var(--text-muted)',
          fontStyle: 'italic',
          marginTop: 12,
          textAlign: 'center',
        }}>
          DEMO TEST SET — {filteredDemos.length} articles shown
        </p>
      </div>
    </div>
  );
}
