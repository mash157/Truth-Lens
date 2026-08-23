import { useState } from 'react';
import NewsInput from '../components/NewsInput';
import ResultCard from '../components/ResultCard';
import LoadingState from '../components/LoadingState';

export default function Analyze() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [inputData, setInputData] = useState({ title: '', text: '' });
  const [webResults, setWebResults] = useState(null);

  return (
    <div style={{ paddingBottom: 80 }}>
      {/* Page Header */}
      <section
        className="analyze-header"
        style={{
          textAlign: 'center',
          padding: '50px 24px 30px',
          maxWidth: 700,
          margin: '0 auto',
        }}
      >
        <h1
          style={{
            fontSize: 'clamp(1.8rem, 4vw, 2.6rem)',
            fontWeight: 800,
            lineHeight: 1.15,
            letterSpacing: '-0.03em',
            marginBottom: 12,
            background: 'linear-gradient(135deg, var(--primary) 0%, #06b6d4 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          Analyze News Article
        </h1>
        <p
          style={{
            fontSize: '1rem',
            color: 'var(--text-secondary)',
            maxWidth: 540,
            margin: '0 auto',
            lineHeight: 1.65,
          }}
        >
          Paste a news headline and article text. TruthLens will classify it and
          explain which textual features influenced the prediction.
        </p>
      </section>

      {/* Input Form */}
      <section className="container">
        <NewsInput
          onResult={setResult}
          onLoading={setLoading}
          onError={setError}
          onInputChange={setInputData}
          onWebResults={setWebResults}
        />
      </section>

      {/* Loading State */}
      {loading && (
        <section className="container">
          <LoadingState message="Analyzing article..." />
        </section>
      )}

      {/* Error State */}
      {error && !loading && (
        <section className="container">
          <div
            className="glass-card fade-in"
            style={{
              maxWidth: 720,
              margin: '32px auto',
              padding: '24px',
              borderLeft: '4px solid var(--accent-fake)',
            }}
          >
            <h3
              style={{
                fontSize: '1.05rem',
                fontWeight: 700,
                color: 'var(--accent-fake)',
                marginBottom: 8,
              }}
            >
              Analysis Error
            </h3>
            <p
              style={{
                fontSize: '0.9rem',
                color: 'var(--text-secondary)',
                lineHeight: 1.6,
                margin: 0,
              }}
            >
              {typeof error === 'string'
                ? error
                : 'An unexpected error occurred. Please ensure the backend is running and try again.'}
            </p>
          </div>
        </section>
      )}

      {/* Result */}
      {result && !loading && (
        <section className="container">
          <ResultCard
            result={result}
            title={inputData.title}
            articleText={inputData.text}
          />
        </section>
      )}

      {/* Web Verification Results */}
      {webResults && webResults.length > 0 && !loading && (
        <section className="container">
          <div
            className="glass-card fade-in"
            style={{ maxWidth: 720, margin: '32px auto' }}
          >
            <h3 style={{
              fontSize: '1.05rem',
              fontWeight: 700,
              color: 'var(--text-primary)',
              marginBottom: 4,
            }}>Web Evidence</h3>
            <p style={{
              fontSize: '0.82rem',
              color: 'var(--text-muted)',
              margin: '0 0 16px',
            }}>
              {webResults.length} related source{webResults.length !== 1 ? 's' : ''} found
            </p>
            {webResults.map((r, i) => (
              <div
                key={i}
                className="glass-card"
                style={{
                  padding: '14px 18px',
                  marginBottom: 10,
                  borderLeft: '3px solid var(--primary)',
                }}
              >
                <span style={{
                  fontSize: '0.72rem',
                  fontWeight: 600,
                  color: 'var(--primary)',
                  textTransform: 'uppercase',
                  letterSpacing: '0.04em',
                  display: 'block',
                  marginBottom: 4,
                }}>{r.link ? new URL(r.link).hostname.replace('www.', '') : ''}</span>
                <h4 style={{
                  fontSize: '0.92rem',
                  fontWeight: 700,
                  color: 'var(--text-primary)',
                  marginBottom: 6,
                  lineHeight: 1.3,
                }}>{r.title}</h4>
                <p style={{
                  fontSize: '0.82rem',
                  color: 'var(--text-secondary)',
                  lineHeight: 1.55,
                  margin: 0,
                }}>{r.snippet}</p>
              </div>
            ))}
            <p style={{
              fontSize: '0.75rem',
              color: 'var(--text-muted)',
              fontStyle: 'italic',
              marginTop: 8,
            }}>
              Web evidence is retrieved from external search results and does not independently verify factual claims.
            </p>
          </div>
        </section>
      )}


    </div>
  );
}
