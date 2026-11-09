import { useState, useEffect } from 'react';
import {
  BarChart3,
  BrainCircuit,
  Database,
  AlertTriangle,
  RefreshCw,
} from 'lucide-react';
import { api } from '../services/api';
import MetricCard from '../components/MetricCard';
import ModelComparison from '../components/ModelComparison';
import ConfusionMatrix from '../components/ConfusionMatrix';
import LoadingState from '../components/LoadingState';
import { formatPercentage } from '../utils/formatters';

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);
  const [featureImportance, setFeatureImportance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [metricsData, modelData, featureData] = await Promise.allSettled([
        api.getMetrics(),
        api.getModelInfo(),
        api.getFeatureImportance(),
      ]);

      if (metricsData.status === 'fulfilled') setMetrics(metricsData.value);
      if (modelData.status === 'fulfilled') setModelInfo(modelData.value);
      if (featureData.status === 'fulfilled') setFeatureImportance(featureData.value);

      // Check if at least one succeeded
      if (
        metricsData.status === 'rejected' &&
        modelData.status === 'rejected' &&
        featureData.status === 'rejected'
      ) {
        setError(
          'Unable to load dashboard data. Please ensure the backend is running and the model has been trained.'
        );
      }
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return (
      <div style={{ paddingBottom: 80 }}>
        <section style={{ textAlign: 'center', padding: '50px 24px 30px' }}>
          <h1
            style={{
              fontSize: 'clamp(1.8rem, 4vw, 2.6rem)',
              fontWeight: 800,
              letterSpacing: '-0.03em',
              background: 'linear-gradient(135deg, var(--primary) 0%, #06b6d4 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            Model Dashboard
          </h1>
        </section>
        <LoadingState message="Loading dashboard data..." />
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ paddingBottom: 80 }}>
        <section style={{ textAlign: 'center', padding: '50px 24px 30px' }}>
          <h1
            style={{
              fontSize: 'clamp(1.8rem, 4vw, 2.6rem)',
              fontWeight: 800,
              letterSpacing: '-0.03em',
              background: 'linear-gradient(135deg, var(--primary) 0%, #06b6d4 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            Model Dashboard
          </h1>
        </section>
        <section className="container">
          <div
            className="glass-card"
            style={{
              maxWidth: 600,
              margin: '0 auto',
              textAlign: 'center',
              padding: '40px 24px',
            }}
          >
            <AlertTriangle
              size={40}
              style={{ color: 'var(--accent-ambiguous)', marginBottom: 16 }}
            />
            <h3
              style={{
                fontSize: '1.15rem',
                fontWeight: 700,
                color: 'var(--text-primary)',
                marginBottom: 10,
              }}
            >
              Data Unavailable
            </h3>
            <p
              style={{
                fontSize: '0.9rem',
                color: 'var(--text-secondary)',
                lineHeight: 1.6,
                marginBottom: 20,
              }}
            >
              {error}
            </p>
            <button className="btn btn-primary" onClick={fetchData}>
              <RefreshCw size={16} />
              Retry
            </button>
          </div>
        </section>
      </div>
    );
  }

  const evalMetrics = metrics?.evaluation_metrics;
  const datasetStats = metrics?.dataset_statistics;
  const modelComparison = metrics?.model_comparison;

  return (
    <div style={{ paddingBottom: 80 }}>
      {/* Page Header */}
      <section style={{ textAlign: 'center', padding: '50px 24px 30px' }}>
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
          Model Dashboard
        </h1>
        <p
          style={{
            fontSize: '1rem',
            color: 'var(--text-secondary)',
            maxWidth: 560,
            margin: '0 auto',
            lineHeight: 1.65,
          }}
        >
          Real-time metrics and evaluation data from the trained TruthLens
          classification model.
        </p>
      </section>

      <div className="container">
        {/* Best Model Banner */}
        {modelInfo?.best_model_name && (
          <div
            className="glass-card fade-in"
            style={{
              textAlign: 'center',
              padding: '20px 24px',
              marginBottom: 28,
              background: 'var(--primary-glow)',
              border: '1px solid var(--primary)',
            }}
          >
            <span
              style={{
                fontSize: '0.78rem',
                fontWeight: 600,
                color: 'var(--primary)',
                textTransform: 'uppercase',
                letterSpacing: '0.08em',
              }}
            >
              Best Performing Model
            </span>
            <h2
              style={{
                fontSize: '1.5rem',
                fontWeight: 800,
                color: 'var(--text-primary)',
                margin: '6px 0 0',
              }}
            >
              <BrainCircuit
                size={22}
                style={{
                  display: 'inline-block',
                  verticalAlign: 'middle',
                  marginRight: 8,
                  color: 'var(--primary)',
                }}
              />
              {modelInfo.best_model_name}
            </h2>
          </div>
        )}

        {/* Metric Cards */}
        {evalMetrics && (
          <div className="kpi-grid">
            <MetricCard
              label="Accuracy"
              value={formatPercentage(evalMetrics.accuracy)}
              color="var(--primary)"
            />
            <MetricCard
              label="Precision"
              value={formatPercentage(evalMetrics.precision)}
              color="var(--accent-genuine)"
            />
            <MetricCard
              label="Recall"
              value={formatPercentage(evalMetrics.recall)}
              color="var(--accent-ambiguous)"
            />
            <MetricCard
              label="F1 Score"
              value={formatPercentage(evalMetrics.f1_score)}
              color="var(--accent-fake)"
            />
          </div>
        )}

        {/* Confusion Matrix */}
        <div className="glass-card fade-in" style={{ marginBottom: 28, padding: '28px 24px' }}>
          <ConfusionMatrix />

          {evalMetrics?.confusion_matrix && (
            <div style={{ marginTop: 20 }}>
              <h4
                style={{
                  fontSize: '0.88rem',
                  fontWeight: 600,
                  color: 'var(--text-secondary)',
                  marginBottom: 12,
                  textTransform: 'uppercase',
                  letterSpacing: '0.04em',
                }}
              >
                Understanding the Matrix
              </h4>
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                  gap: 12,
                  fontSize: '0.84rem',
                  color: 'var(--text-secondary)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span
                    style={{
                      width: 10,
                      height: 10,
                      borderRadius: 3,
                      background: 'var(--accent-genuine)',
                      flexShrink: 0,
                    }}
                  />
                  <span>
                    <strong>True Negative:</strong>{' '}
                    {evalMetrics.confusion_matrix.true_negative.toLocaleString()} — Correctly
                    identified as genuine
                  </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span
                    style={{
                      width: 10,
                      height: 10,
                      borderRadius: 3,
                      background: 'var(--accent-fake)',
                      flexShrink: 0,
                    }}
                  />
                  <span>
                    <strong>True Positive:</strong>{' '}
                    {evalMetrics.confusion_matrix.true_positive.toLocaleString()} — Correctly
                    identified as fake
                  </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span
                    style={{
                      width: 10,
                      height: 10,
                      borderRadius: 3,
                      background: 'var(--accent-ambiguous)',
                      flexShrink: 0,
                    }}
                  />
                  <span>
                    <strong>False Positive:</strong>{' '}
                    {evalMetrics.confusion_matrix.false_positive.toLocaleString()} — Genuine
                    article misclassified as fake
                  </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span
                    style={{
                      width: 10,
                      height: 10,
                      borderRadius: 3,
                      background: '#f59e0b',
                      flexShrink: 0,
                    }}
                  />
                  <span>
                    <strong>False Negative:</strong>{' '}
                    {evalMetrics.confusion_matrix.false_negative.toLocaleString()} — Fake
                    article misclassified as genuine
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Model Comparison */}
        {modelComparison && (
          <div className="glass-card fade-in" style={{ marginBottom: 28, padding: '28px 24px' }}>
            <ModelComparison data={modelComparison} />
          </div>
        )}

        {/* Dataset Statistics */}
        {datasetStats && (
          <div className="glass-card fade-in" style={{ marginBottom: 28, padding: '28px 24px' }}>
            <h3 className="panel-heading">
              <Database size={20} aria-hidden="true" />
              Dataset Statistics
            </h3>

            <div className="stat-grid">
              <StatItem
                label="Raw Records"
                value={datasetStats.raw_record_count?.toLocaleString()}
              />
              <StatItem
                label="Clean Records"
                value={datasetStats.clean_record_count?.toLocaleString()}
              />
              <StatItem
                label="Duplicates Removed"
                value={datasetStats.duplicate_records?.toLocaleString()}
              />
              <StatItem
                label="Genuine Articles"
                value={datasetStats.class_distribution?.genuine?.toLocaleString()}
                sub={datasetStats.class_percentages?.genuine ? `${datasetStats.class_percentages.genuine}%` : ''}
              />
              <StatItem
                label="Fake Articles"
                value={datasetStats.class_distribution?.fake?.toLocaleString()}
                sub={datasetStats.class_percentages?.fake ? `${datasetStats.class_percentages.fake}%` : ''}
              />
              <StatItem
                label="Avg Word Count"
                value={datasetStats.text_length?.avg_words?.toFixed(0)}
              />
              <StatItem
                label="Train Split"
                value={datasetStats.splits?.train?.toLocaleString()}
              />
              <StatItem
                label="Validation Split"
                value={datasetStats.splits?.validation?.toLocaleString()}
              />
              <StatItem
                label="Test Split"
                value={datasetStats.splits?.test?.toLocaleString()}
              />
            </div>
          </div>
        )}

        {/* Feature Importance */}
        {featureImportance && (
          <div className="glass-card fade-in" style={{ padding: '28px 24px' }}>
            <h3 className="panel-heading">
              <BarChart3 size={20} aria-hidden="true" />
              Global Feature Importance ({featureImportance.model_name})
            </h3>

            <p className="panel-subtitle">
              Words with the strongest model coefficients. Positive values indicate features
              associated with fake articles; negative values indicate features associated with
              genuine articles.
            </p>

            <div className="feature-columns">
              {/* Top Fake Features */}
              <div>
                <h4 className="feature-column-title fake">Top Fake-Associated Features</h4>
                <div className="bar-chart-container">
                  {featureImportance.top_fake_features?.slice(0, 10).map((f, i) => {
                    const maxVal =
                      featureImportance.top_fake_features[0]?.coefficient || 1;
                    const pct = Math.min(
                      (Math.abs(f.coefficient) / Math.abs(maxVal)) * 100,
                      100
                    );
                    return (
                      <div className="bar-row" key={i}>
                        <span className="bar-rank">{i + 1}</span>
                        <span className="bar-label" title={f.feature}>
                          {f.feature}
                        </span>
                        <div className="bar-track">
                          <div
                            className="bar-fill fill-fake"
                            style={{ width: `${pct}%` }}
                          />
                        </div>
                        <span className="bar-value">
                          {f.coefficient.toFixed(1)}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Top Genuine Features */}
              <div>
                <h4 className="feature-column-title genuine">Top Genuine-Associated Features</h4>
                <div className="bar-chart-container">
                  {featureImportance.top_genuine_features?.slice(0, 10).map((f, i) => {
                    const maxVal =
                      Math.abs(
                        featureImportance.top_genuine_features[0]?.coefficient
                      ) || 1;
                    const pct = Math.min(
                      (Math.abs(f.coefficient) / maxVal) * 100,
                      100
                    );
                    return (
                      <div className="bar-row" key={i}>
                        <span className="bar-rank">{i + 1}</span>
                        <span className="bar-label" title={f.feature}>
                          {f.feature}
                        </span>
                        <div className="bar-track">
                          <div
                            className="bar-fill fill-genuine"
                            style={{ width: `${pct}%` }}
                          />
                        </div>
                        <span className="bar-value">
                          {f.coefficient.toFixed(1)}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function StatItem({ label, value, sub }) {
  return (
    <div className="stat-card">
      <span className="stat-label">{label}</span>
      <span className="stat-value">{value}</span>
      {sub && <span className="stat-sub">{sub}</span>}
    </div>
  );
}
