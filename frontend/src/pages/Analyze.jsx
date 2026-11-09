import { useState } from 'react';
import NewsInput from '../components/NewsInput';
import ResultCard from '../components/ResultCard';
import LoadingState from '../components/LoadingState';

function getDomain(link) {
  try {
    return new URL(link).hostname.replace(/^www\./, '');
  } catch {
    return '';
  }
}

export default function Analyze() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [inputData, setInputData] = useState({ title: '', text: '' });
  const [webResults, setWebResults] = useState(null);

  return (
    <div className="analyze-page">
      {/* Page Header */}
      <section className="analyze-header">
        <h1 className="analyze-title">Analyze News Article</h1>
        <p className="analyze-subtitle">
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
          <div className="glass-card analyze-error-card fade-in" role="alert">
            <h3>Analysis Error</h3>
            <p>
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
          <div className="glass-card web-evidence-card fade-in">
            <div className="web-results-head">
              <h3 className="web-results-title">Web Evidence</h3>
              <p className="web-results-sub">
                {webResults.length} related source
                {webResults.length !== 1 ? 's' : ''} found
              </p>
            </div>

            {webResults.map((source, index) => {
              const domain = getDomain(source.link);
              return (
                <div className="glass-card web-result-card" key={`${source.link}-${index}`}>
                  {domain && <span className="web-source-domain">{domain}</span>}
                  <h4 className="web-source-title">{source.title}</h4>
                  <p className="web-source-snippet">{source.snippet}</p>
                </div>
              );
            })}

            <p className="web-results-note">
              Web evidence is retrieved from external search results and does not
              independently verify factual claims. Always consult primary sources.
            </p>
          </div>
        </section>
      )}
    </div>
  );
}
