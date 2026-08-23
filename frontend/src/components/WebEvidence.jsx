import { useState } from 'react';
import { Search, ExternalLink, Loader2, AlertCircle } from 'lucide-react';
import { api } from '../services/api';

function getDomain(url) {
  try {
    return new URL(url).hostname.replace('www.', '');
  } catch {
    return '';
  }
}

function SourceCard({ result }) {
  const domain = getDomain(result.link);

  return (
    <div
      className="glass-card"
      style={{
        padding: '16px 20px',
        marginBottom: 12,
        borderLeft: '3px solid var(--primary)',
      }}
    >
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-start',
          gap: 12,
        }}
      >
        <div style={{ flex: 1, minWidth: 0 }}>
          {/* Domain */}
          {domain && (
            <span
              style={{
                fontSize: '0.75rem',
                fontWeight: 600,
                color: 'var(--primary)',
                textTransform: 'uppercase',
                letterSpacing: '0.04em',
                display: 'block',
                marginBottom: 4,
              }}
            >
              {domain}
            </span>
          )}

          {/* Title */}
          <h4
            style={{
              fontSize: '0.95rem',
              fontWeight: 700,
              color: 'var(--text-primary)',
              marginBottom: 6,
              lineHeight: 1.3,
            }}
          >
            {result.title}
          </h4>

          {/* Snippet */}
          <p
            style={{
              fontSize: '0.84rem',
              color: 'var(--text-secondary)',
              lineHeight: 1.6,
              margin: 0,
            }}
          >
            {result.snippet}
          </p>
        </div>

        {/* Open Source button */}
        <a
          href={result.link}
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-secondary"
          style={{
            flexShrink: 0,
            padding: '8px 14px',
            fontSize: '0.8rem',
            gap: 6,
          }}
        >
          <ExternalLink size={14} />
          Open Source
        </a>
      </div>
    </div>
  );
}

export default function WebEvidence({ headline, articleText }) {
  const [searching, setSearching] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleVerify = async () => {
    if (searching) return;

    setSearching(true);
    setError(null);
    setHasSearched(true);

    // Build a concise query: prefer headline, fall back to first ~120 chars of text
    const query = headline?.trim() || articleText?.trim().slice(0, 120) || '';

    try {
      const data = await api.searchNews(query, 5);
      setResults(data.results || []);
    } catch (err) {
      setError(
        err.detail?.message ||
          err.message ||
          'Web verification is temporarily unavailable.'
      );
      setResults(null);
    } finally {
      setSearching(false);
    }
  };

  return (
    <div style={{ marginTop: 20 }}>
      {/* Separator */}
      <div
        style={{
          height: 1,
          background: 'var(--border-color)',
          marginBottom: 20,
        }}
      />

      {/* Verify with Web button */}
      <button
        className="btn btn-secondary"
        onClick={handleVerify}
        disabled={searching}
        style={{
          width: '100%',
          padding: '12px 20px',
          fontSize: '0.95rem',
          fontWeight: 600,
          gap: 8,
          border: '1px solid var(--primary)',
          color: 'var(--primary)',
          background: 'var(--primary-glow)',
        }}
      >
        {searching ? (
          <>
            <Loader2 size={18} style={{ animation: 'spin 1s linear infinite' }} />
            Searching the web for related evidence...
          </>
        ) : (
          <>
            <Search size={18} />
            Verify with Web
          </>
        )}
      </button>

      {/* Loading spinner style */}
      {searching && (
        <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      )}

      {/* Loading state */}
      {searching && (
        <div
          style={{
            textAlign: 'center',
            padding: '24px 16px',
            color: 'var(--text-muted)',
            fontSize: '0.88rem',
          }}
        >
          Searching the web for related evidence...
        </div>
      )}

      {/* Error state */}
      {error && !searching && (
        <div
          style={{
            marginTop: 16,
            padding: '16px 20px',
            borderRadius: 12,
            background: 'var(--bg-tertiary)',
            border: '1px solid var(--border-color)',
            borderLeft: '4px solid var(--accent-ambiguous)',
            display: 'flex',
            alignItems: 'center',
            gap: 10,
          }}
        >
          <AlertCircle
            size={18}
            style={{ color: 'var(--accent-ambiguous)', flexShrink: 0 }}
          />
          <p
            style={{
              fontSize: '0.88rem',
              color: 'var(--text-secondary)',
              margin: 0,
              lineHeight: 1.5,
            }}
          >
            {error}
          </p>
        </div>
      )}

      {/* Results */}
      {hasSearched && !searching && !error && results && (
        <div style={{ marginTop: 20 }}>
          {/* Section header */}
          <div style={{ marginBottom: 16 }}>
            <h3
              style={{
                fontSize: '1.05rem',
                fontWeight: 700,
                color: 'var(--text-primary)',
                marginBottom: 4,
              }}
            >
              Web Evidence
            </h3>
            <p
              style={{
                fontSize: '0.82rem',
                color: 'var(--text-muted)',
                margin: 0,
              }}
            >
              {results.length > 0
                ? `${results.length} related source${results.length !== 1 ? 's' : ''} found`
                : 'No relevant web sources were found.'}
            </p>
          </div>

          {/* Source cards */}
          {results.length > 0 ? (
            results.map((r, i) => <SourceCard key={i} result={r} />)
          ) : (
            <div
              style={{
                padding: '24px 20px',
                borderRadius: 12,
                background: 'var(--bg-tertiary)',
                border: '1px solid var(--border-color)',
                textAlign: 'center',
              }}
            >
              <p
                style={{
                  fontSize: '0.9rem',
                  color: 'var(--text-muted)',
                  fontStyle: 'italic',
                  margin: 0,
                }}
              >
                No relevant web sources were found.
              </p>
            </div>
          )}

          {/* Disclaimer */}
          <div
            style={{
              marginTop: 16,
              padding: '12px 16px',
              borderRadius: 12,
              background: 'var(--bg-tertiary)',
              border: '1px solid var(--border-color)',
              borderLeft: '4px solid var(--accent-ambiguous)',
              fontSize: '0.78rem',
              color: 'var(--text-muted)',
              fontStyle: 'italic',
              lineHeight: 1.6,
            }}
          >
            Web evidence is retrieved from external search results and does not
            independently verify factual claims. Always consult primary sources.
          </div>
        </div>
      )}
    </div>
  );
}
