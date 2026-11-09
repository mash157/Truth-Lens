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
      <h2 className="form-title">Analyze a News Article</h2>

      {/* Headline */}
      <label className="field-label" htmlFor="analyze-headline">
        Headline <span className="field-optional">(optional)</span>
      </label>
      <input
        id="analyze-headline"
        className="input-field"
        type="text"
        placeholder="Enter the headline or title..."
        value={title}
        onChange={e => setTitle(e.target.value)}
      />

      {/* Article body */}
      <label className="field-label" htmlFor="analyze-content">
        Article Content <span className="field-required">*</span>
      </label>
      <textarea
        id="analyze-content"
        className="input-field"
        placeholder="Paste or type the article text here (minimum 10 characters)..."
        value={text}
        onChange={e => setText(e.target.value)}
        rows={8}
      />

      {/* Counters */}
      <div className="field-meta">
        <span>{wordCount} words</span>
        <span>{charCount} characters</span>
      </div>

      {/* Actions */}
      <div className="analyze-actions">
        <button type="button" className="btn btn-primary" onClick={handleAnalyze} disabled={!canSubmit}>
          {submitting ? 'Analyzing...' : <><Search size={16} /> Analyze</>}
        </button>
        <button type="button" className="btn btn-web" onClick={handleVerifyWithWeb} disabled={!canSubmit}>
          <Globe size={16} /> Verify with Web
        </button>
        <button type="button" className="btn btn-secondary" onClick={handleClear}>Clear</button>
      </div>

      {/* Demo Article Library */}
      <div className="demo-section">
        <div className="demo-notice">
          <p className="demo-notice-title">Demo Testing Set</p>
          <p className="demo-notice-text">
            These examples are for testing the TruthLens model and UI. Expected labels are testing expectations and are not proof of factual truth.
          </p>
        </div>

        <h3 className="demo-heading">Try a Demo Article</h3>
        <p className="demo-sub">
          Select a category, then click an article to populate the fields above.
        </p>

        {/* Category Tabs */}
        <div className="demo-tabs">
          {TABS.map(tab => {
            const Icon = tab.icon;
            const isActive = demoTab === tab.key;
            return (
              <button
                type="button"
                key={tab.key}
                className={`demo-tab${isActive ? ' is-active' : ''}`}
                style={{ '--tab-color': tab.color }}
                onClick={() => setDemoTab(tab.key)}
              >
                <Icon size={14} />
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Demo Article Cards */}
        <div className="demo-grid">
          {filteredDemos.map(article => (
            <button
              type="button"
              key={article.id}
              className="glass-card demo-card"
              onClick={() => handleTryExample(article)}
              aria-label={`Use demo article: ${article.headline}`}
            >
              <span className="demo-card-top">
                <span className="demo-category">{article.category}</span>
                {article.sourceType === 'demo-test' && (
                  <span className="demo-badge">DEMO TEST</span>
                )}
              </span>
              <span className="demo-title">{article.headline}</span>
              <span className="demo-use-btn">
                Use This Example
                <ChevronRight size={12} />
              </span>
            </button>
          ))}
        </div>

        <p className="demo-count">
          DEMO TEST SET — {filteredDemos.length} articles shown
        </p>
      </div>
    </div>
  );
}
