import { useState } from 'react';
import { Search, CheckCircle, XCircle, HelpCircle } from 'lucide-react';
import { api } from '../services/api';

const DEMO_ARTICLES = [
  {
    id: 'genuine',
    type: 'genuine',
    title: 'UN calls for humanitarian pause in Yemen as fighting escalates',
    text: "The United Nations called for a humanitarian pause in Yemen after fighting escalated in the capital Sana'a. The organization urged all parties to protect civilians, allow medical assistance to reach affected communities, and ensure access to food and water. Relief coordinators expressed concern about civilian casualties and called for immediate measures to protect vulnerable populations.",
  },
  {
    id: 'fake',
    type: 'fake',
    title: 'UNBELIEVABLE! CLINTON FOUNDATION RECEIVED MILLIONS IN CASH FROM ALIEN LOBBY',
    text: 'In a shocking turn of events, a secret leaked document has revealed that the Clinton Foundation received millions of dollars in cash payments from a mysterious alien lobby group claiming to represent extraterrestrial interests. According to the document, the payments were made during the height of the presidential campaign. This shocking discovery has left the public stunned, and mainstream media is refusing to cover the massive cover-up. Investigators are calling it the biggest scandal in modern history. SHARE this article everywhere before it gets taken down by the elite!',
  },
  {
    id: 'ambiguous',
    type: 'ambiguous',
    title: 'Scientists report unexpected changes in global weather patterns',
    text: 'A new report describes changes in weather patterns observed across several regions. Researchers say the findings require further study to understand the causes and possible long-term effects. Some experts believe the changes may be connected to broader environmental trends, while others say more evidence is needed before reaching a clear conclusion.',
  },
];

export default function NewsInput({ onResult, onLoading, onError }) {
  const [title, setTitle] = useState('');
  const [text, setText] = useState('');
  const [submitting, setSubmitting] = useState(false);

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

      {/* Demo articles */}
      <div className="demo-section" style={{ marginTop: 24, borderTop: '1px solid var(--border-color)', paddingTop: 16 }}>
          <p style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: 10 }}>
            Try a Demo Example
          </p>
          <div className="demo-buttons" style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {DEMO_ARTICLES.map(s => (
              <button
                key={s.id}
                className="btn btn-secondary"
                onClick={() => handleTryExample(s)}
                style={{ fontSize: '0.78rem', padding: '6px 14px' }}
              >
                {s.type === 'genuine' ? <CheckCircle size={14} style={{ color: 'var(--accent-genuine)' }} /> : s.type === 'fake' ? <XCircle size={14} style={{ color: 'var(--accent-fake)' }} /> : <HelpCircle size={14} style={{ color: 'var(--accent-ambiguous)' }} />}{' '}
                {s.type === 'genuine' ? 'Genuine Demo' : s.type === 'fake' ? 'Fake Demo' : 'Ambiguous Demo'}
              </button>
            ))}
          </div>
          <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontStyle: 'italic', marginTop: 8 }}>
            DEMO ARTICLES — FOR SYSTEM TESTING ONLY
          </p>
      </div>
    </div>
  );
}
