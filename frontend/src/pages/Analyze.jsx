import { useState } from 'react';
import NewsInput from '../components/NewsInput';
import ResultCard from '../components/ResultCard';
import LoadingState from '../components/LoadingState';

export default function Analyze() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  return (
    <div style={{ paddingBottom: 80 }}>
      {/* Page Header */}
      <section
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
          <ResultCard result={result} />
        </section>
      )}


    </div>
  );
}
