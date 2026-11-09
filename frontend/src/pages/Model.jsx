import { useState, useEffect } from 'react';
import {
  Database,
  Binary,
  BrainCircuit,
  GitCompare,
  Award,
  BarChart3,
  AlertTriangle,
  RefreshCw,
  BookOpen,
} from 'lucide-react';
import { api } from '../services/api';
import ModelComparison from '../components/ModelComparison';
import LoadingState from '../components/LoadingState';
import { formatPercentage } from '../utils/formatters';

const MODELS_INFO = [
  {
    name: 'Logistic Regression',
    icon: BrainCircuit,
    description:
      'A linear model that estimates the probability of an article being fake using a logistic function. It is fast, interpretable, and provides probability outputs directly through predict_proba.',
    strengths: [
      'Fast training and prediction',
      'Provides probability estimates',
      'Linear coefficients are interpretable',
    ],
    color: '#6366f1',
  },
  {
    name: 'Multinomial Naive Bayes',
    icon: BookOpen,
    description:
      'A probabilistic classifier based on Bayes\' theorem with the "naive" assumption of feature independence. Well-suited for text classification with TF-IDF features.',
    strengths: [
      'Very fast training',
      'Works well with small datasets',
      'Simple and effective for text',
    ],
    color: '#14b8a6',
  },
  {
    name: 'Linear SVM (Calibrated)',
    icon: GitCompare,
    description:
      'A Linear Support Vector Machine wrapped in CalibratedClassifierCV to provide probability estimates. Finds the optimal hyperplane that maximally separates fake and genuine article features.',
    strengths: [
      'Excellent for high-dimensional text data',
      'Strong generalization',
      'Best performance in this project',
    ],
    color: '#f43f5e',
  },
];

export default function Model() {
  const [modelInfo, setModelInfo] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [modelData, metricsData] = await Promise.allSettled([
          api.getModelInfo(),
          api.getMetrics(),
        ]);
        if (modelData.status === 'fulfilled') setModelInfo(modelData.value);
        if (metricsData.status === 'fulfilled') setMetrics(metricsData.value);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div style={{ paddingBottom: 80 }}>
      {/* Page Header */}
      <section
        style={{
          textAlign: 'center',
          padding: '50px 24px 30px',
          maxWidth: 750,
          margin: '0 auto',
        }}
      >
        <h1
          style={{
            fontSize: 'clamp(1.8rem, 4vw, 2.6rem)',
            fontWeight: 800,
            letterSpacing: '-0.03em',
            marginBottom: 12,
            background: 'linear-gradient(135deg, var(--primary) 0%, #06b6d4 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          Model Information
        </h1>
        <p
          style={{
            fontSize: '1rem',
            color: 'var(--text-secondary)',
            lineHeight: 1.65,
          }}
        >
          Understanding the WELFake dataset, TF-IDF vectorization, trained
          classifiers, and how the best model was selected.
        </p>
      </section>

      <div className="container">
        {/* WELFake Dataset */}
        <div
          className="glass-card fade-in"
          style={{ marginBottom: 28, padding: '28px 24px', borderLeft: '4px solid var(--primary)' }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 14 }}>
            <Database size={20} style={{ color: 'var(--primary)' }} />
            <h2 style={{ fontSize: '1.2rem', fontWeight: 750, color: 'var(--text-primary)' }}>
              WELFake Dataset
            </h2>
          </div>
          <p
            style={{
              fontSize: '0.92rem',
              color: 'var(--text-secondary)',
              lineHeight: 1.7,
              marginBottom: 16,
            }}
          >
            TruthLens is trained on the WELFake (Wikipedia + Event-driven + Liar Fake news)
            dataset from Kaggle. It contains 72,134 news articles labelled as either fake (1)
            or genuine (0). After cleaning — removing duplicates, handling missing values, and
            filtering empty records — 63,678 clean articles remain for training and evaluation.
          </p>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
              gap: 12,
            }}
          >
            <StatBadge label="Total Articles" value="72,134" />
            <StatBadge label="After Cleaning" value="63,678" />
            <StatBadge label="Genuine" value="54.6%" />
            <StatBadge label="Fake" value="45.4%" />
          </div>
        </div>

        {/* TF-IDF */}
        <div
          className="glass-card fade-in"
          style={{ marginBottom: 28, padding: '28px 24px', borderLeft: '4px solid #06b6d4' }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 14 }}>
            <Binary size={20} style={{ color: '#06b6d4' }} />
            <h2 style={{ fontSize: '1.2rem', fontWeight: 750, color: 'var(--text-primary)' }}>
              TF-IDF Vectorization
            </h2>
          </div>
          <p
            style={{
              fontSize: '0.92rem',
              color: 'var(--text-secondary)',
              lineHeight: 1.7,
              marginBottom: 14,
            }}
          >
            Term Frequency-Inverse Document Frequency (TF-IDF) is used to convert raw text
            into numerical feature vectors that machine learning models can process. TF-IDF
            weights words based on how frequently they appear in a document relative to the
            entire corpus.
          </p>
          <p
            style={{
              fontSize: '0.92rem',
              color: 'var(--text-secondary)',
              lineHeight: 1.7,
              marginBottom: 14,
            }}
          >
            Words that appear frequently across many documents (like "the", "is", "and") receive
            lower weights, while words that are distinctive to certain articles receive higher
            weights. This makes TF-IDF particularly effective for text classification.
          </p>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
              gap: 12,
            }}
          >
            <StatBadge label="Max Features" value="10,000" />
            <StatBadge label="N-gram Range" value="(1, 2)" />
            <StatBadge label="Min Document Freq" value="2" />
            <StatBadge label="Sublinear TF" value="Yes" />
          </div>
        </div>

        {/* Models Section */}
        <div style={{ marginBottom: 28 }}>
          <div style={{ textAlign: 'center', marginBottom: 24 }}>
            <p
              style={{
                color: 'var(--primary)',
                fontSize: '0.8rem',
                fontWeight: 700,
                textTransform: 'uppercase',
                letterSpacing: '0.12em',
                marginBottom: 8,
              }}
            >
              Trained Classifiers
            </p>
            <h2
              style={{
                fontSize: '1.4rem',
                fontWeight: 750,
                color: 'var(--text-primary)',
              }}
            >
              Why Multiple Models?
            </h2>
          </div>

          <p
            style={{
              fontSize: '0.92rem',
              color: 'var(--text-secondary)',
              lineHeight: 1.7,
              textAlign: 'center',
              maxWidth: 650,
              margin: '0 auto 24px',
            }}
          >
            Multiple classifiers are trained and compared to ensure the best-performing model
            is selected. Each model has different strengths — comparing them provides a more
            robust evaluation of classification performance.
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {MODELS_INFO.map((model) => {
              const Icon = model.icon;
              return (
                <div
                  key={model.name}
                  className="glass-card fade-in"
                  style={{ padding: '24px 24px', borderLeft: `4px solid ${model.color}` }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 10 }}>
                    <div
                      style={{
                        width: 40,
                        height: 40,
                        borderRadius: 10,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        background: `${model.color}15`,
                        color: model.color,
                      }}
                    >
                      <Icon size={20} />
                    </div>
                    <h3
                      style={{
                        fontSize: '1.05rem',
                        fontWeight: 700,
                        color: 'var(--text-primary)',
                      }}
                    >
                      {model.name}
                    </h3>
                  </div>
                  <p
                    style={{
                      fontSize: '0.88rem',
                      color: 'var(--text-secondary)',
                      lineHeight: 1.65,
                      margin: '0 0 12px',
                    }}
                  >
                    {model.description}
                  </p>
                  <div>
                    <span
                      style={{
                        fontSize: '0.78rem',
                        fontWeight: 600,
                        color: 'var(--text-muted)',
                        textTransform: 'uppercase',
                        letterSpacing: '0.04em',
                      }}
                    >
                      Strengths:
                    </span>
                    <ul
                      style={{
                        margin: '6px 0 0',
                        paddingLeft: 18,
                        fontSize: '0.85rem',
                        color: 'var(--text-secondary)',
                        lineHeight: 1.6,
                      }}
                    >
                      {model.strengths.map((s, i) => (
                        <li key={i}>{s}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Model Comparison & Evaluation */}
        {loading ? (
          <LoadingState message="Loading model data..." />
        ) : error ? (
          <div
            className="glass-card"
            style={{
              textAlign: 'center',
              padding: '32px 24px',
              maxWidth: 500,
              margin: '0 auto',
            }}
          >
            <AlertTriangle size={36} style={{ color: 'var(--accent-ambiguous)', marginBottom: 12 }} />
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
              Unable to load model data. Ensure the backend is running.
            </p>
            <button
              className="btn btn-secondary"
              style={{ marginTop: 12 }}
              onClick={() => window.location.reload()}
            >
              <RefreshCw size={14} />
              Retry
            </button>
          </div>
        ) : (
          <>
            {/* Best Model */}
            {modelInfo?.best_model_name && (
              <div
                className="glass-card fade-in"
                style={{
                  marginBottom: 28,
                  padding: '24px 24px',
                  textAlign: 'center',
                  background: 'var(--primary-glow)',
                  border: '1px solid var(--primary)',
                }}
              >
                <Award
                  size={28}
                  style={{ color: 'var(--primary)', marginBottom: 8 }}
                />
                <h3
                  style={{
                    fontSize: '1.2rem',
                    fontWeight: 800,
                    color: 'var(--text-primary)',
                    marginBottom: 6,
                  }}
                >
                  Best Model: {modelInfo.best_model_name}
                </h3>
                {modelInfo.validation_metrics && (
                  <p
                    style={{
                      fontSize: '0.88rem',
                      color: 'var(--text-secondary)',
                      margin: 0,
                    }}
                  >
                    Validation F1-Score:{' '}
                    <strong>
                      {formatPercentage(modelInfo.validation_metrics.F1_Score)}
                    </strong>
                    {modelInfo.test_metrics && (
                      <>
                        {' '} · Test F1-Score:{' '}
                        <strong>
                          {formatPercentage(modelInfo.test_metrics.f1_score)}
                        </strong>
                      </>
                    )}
                  </p>
                )}
              </div>
            )}

            {/* Model Comparison */}
            {metrics?.model_comparison && (
              <div
                className="glass-card fade-in"
                style={{ marginBottom: 28, padding: '28px 24px' }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16 }}>
                  <BarChart3 size={20} style={{ color: 'var(--primary)' }} />
                  <h3
                    style={{
                      fontSize: '1.1rem',
                      fontWeight: 700,
                      color: 'var(--text-primary)',
                    }}
                  >
                    Evaluation Metrics (Test Set)
                  </h3>
                </div>
                <ModelComparison data={metrics.model_comparison} />
              </div>
            )}

            {/* Evaluation Explanation */}
            <div
              className="glass-card fade-in"
              style={{ padding: '28px 24px' }}
            >
              <h3
                style={{
                  fontSize: '1.05rem',
                  fontWeight: 700,
                  color: 'var(--text-primary)',
                  marginBottom: 14,
                }}
              >
                Understanding the Metrics
              </h3>
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
                  gap: 16,
                }}
              >
                <MetricExplanation
                  title="Accuracy"
                  desc="The proportion of all predictions that were correct. Calculated as (TP + TN) / Total."
                />
                <MetricExplanation
                  title="Precision"
                  desc="Of all articles predicted as fake, how many were actually fake. High precision means fewer false alarms."
                />
                <MetricExplanation
                  title="Recall"
                  desc="Of all actual fake articles, how many did the model catch. High recall means fewer missed fakes."
                />
                <MetricExplanation
                  title="F1-Score"
                  desc="The harmonic mean of Precision and Recall. Provides a single balanced metric, used to select the best model."
                />
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

function StatBadge({ label, value }) {
  return (
    <div
      style={{
        padding: '10px 14px',
        borderRadius: 10,
        background: 'var(--bg-tertiary)',
        border: '1px solid var(--border-color)',
        textAlign: 'center',
      }}
    >
      <span
        style={{
          fontSize: '0.72rem',
          fontWeight: 500,
          color: 'var(--text-muted)',
          textTransform: 'uppercase',
          letterSpacing: '0.04em',
          display: 'block',
          marginBottom: 3,
        }}
      >
        {label}
      </span>
      <span
        style={{
          fontSize: '1.1rem',
          fontWeight: 700,
          color: 'var(--text-primary)',
        }}
      >
        {value}
      </span>
    </div>
  );
}

function MetricExplanation({ title, desc }) {
  return (
    <div
      style={{
        padding: '14px 16px',
        borderRadius: 10,
        background: 'var(--bg-tertiary)',
        border: '1px solid var(--border-color)',
      }}
    >
      <h4
        style={{
          fontSize: '0.9rem',
          fontWeight: 700,
          color: 'var(--text-primary)',
          marginBottom: 4,
        }}
      >
        {title}
      </h4>
      <p
        style={{
          fontSize: '0.82rem',
          color: 'var(--text-secondary)',
          lineHeight: 1.55,
          margin: 0,
        }}
      >
        {desc}
      </p>
    </div>
  );
}
