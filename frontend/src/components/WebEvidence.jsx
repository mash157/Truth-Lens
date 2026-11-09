import { useState } from 'react';
import { Search, ExternalLink, Loader2, AlertCircle } from 'lucide-react';
import { api } from '../services/api';

function getDomain(url) {
  try {
    return new URL(url).hostname.replace(/^www\./, '');
  } catch {
    return '';
  }
}

function SourceCard({ result }) {
  const domain = getDomain(result.link);

  return (
    <div className="glass-card web-source-card">
      <div className="web-source-main">
        <div className="web-source-body">
          {domain && <span className="web-source-domain">{domain}</span>}

          <h4 className="web-source-title">{result.title}</h4>
          <p className="web-source-snippet">{result.snippet}</p>
        </div>

        <a
          href={result.link}
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-secondary web-source-link"
        >
          <ExternalLink size={14} aria-hidden="true" />
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
    <div className="web-evidence">
      <div className="web-divider" aria-hidden="true" />

      <button
        type="button"
        className="btn btn-primary web-verify-btn"
        onClick={handleVerify}
        disabled={searching}
      >
        {searching ? (
          <>
            <Loader2 className="spin-icon" size={18} aria-hidden="true" />
            <span>Searching the web for related evidence...</span>
          </>
        ) : (
          <>
            <Search size={18} aria-hidden="true" />
            <span>Verify with Web</span>
          </>
        )}
      </button>

      {searching && (
        <p className="web-status" role="status">
          Searching the web for related evidence...
        </p>
      )}

      {error && !searching && (
        <div className="web-error" role="alert">
          <AlertCircle className="web-error-icon" size={18} aria-hidden="true" />
          <div className="web-error-body">
            <strong>Web verification error</strong>
            <p>{error}</p>
          </div>
        </div>
      )}

      {hasSearched && !searching && !error && results && (
        <div className="web-results">
          <div className="web-results-head">
            <h3 className="web-results-title">Web Evidence</h3>
            <p className="web-results-sub">
              {results.length > 0
                ? `${results.length} related source${results.length !== 1 ? 's' : ''} found`
                : 'No relevant web sources were found.'}
            </p>
          </div>

          {results.length > 0 ? (
            results.map((result, index) => (
              <SourceCard key={`${result.link}-${index}`} result={result} />
            ))
          ) : (
            <div className="web-empty">
              <p>No relevant web sources were found.</p>
            </div>
          )}

          <p className="web-results-note">
            Web evidence is retrieved from external search results and does not
            independently verify factual claims. Always consult primary sources.
          </p>
        </div>
      )}
    </div>
  );
}
