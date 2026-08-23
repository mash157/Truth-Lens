import {
  AlertCircle,
  HelpCircle,
  Target,
  Database,
  Eraser,
  Scissors,
  Binary,
  GraduationCap,
  GitCompare,
  Trophy,
  LineChart,
  BrainCircuit,
  Sparkles,
  ArrowDown,
} from 'lucide-react';
import {
  RESEARCH_PROBLEM,
  RESEARCH_QUESTION,
  OBJECTIVES,
} from '../utils/constants';

const PIPELINE_STEPS = [
  { icon: Database, label: 'Dataset', desc: 'WELFake dataset with 72,134 articles' },
  { icon: Eraser, label: 'Data Cleaning', desc: 'Remove duplicates, handle missing values' },
  { icon: Scissors, label: 'Train / Validation / Test Split', desc: 'Stratified 70/15/15 split' },
  { icon: Binary, label: 'TF-IDF', desc: 'Text to numerical feature vectors' },
  { icon: GraduationCap, label: 'Model Training', desc: 'Train 3 classifiers' },
  { icon: GitCompare, label: 'Model Comparison', desc: 'Compare Accuracy, Precision, Recall, F1' },
  { icon: Trophy, label: 'Best Model', desc: 'Select highest-performing model' },
  { icon: LineChart, label: 'Prediction', desc: 'Classify new articles' },
  { icon: BrainCircuit, label: 'Explainable AI', desc: 'Feature contribution analysis' },
  { icon: Sparkles, label: 'Result', desc: 'Prediction with explanation' },
];

export default function Research() {
  return (
    <div style={{ paddingBottom: 80 }}>
      {/* Page Header */}
      <section
        style={{
          textAlign: 'center',
          padding: '50px 24px 30px',
          maxWidth: 800,
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
          Research Methodology
        </h1>
        <p
          style={{
            fontSize: '1rem',
            color: 'var(--text-secondary)',
            lineHeight: 1.65,
          }}
        >
          The academic foundation behind TruthLens: problem definition,
          research questions, objectives, and the end-to-end methodology.
        </p>
      </section>

      <div className="container">
        {/* Research Problem */}
        <div
          className="glass-card fade-in"
          style={{ marginBottom: 28, padding: '28px 24px', borderLeft: '4px solid var(--accent-fake)' }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 14 }}>
            <AlertCircle size={20} style={{ color: 'var(--accent-fake)' }} />
            <h2
              style={{
                fontSize: '1.2rem',
                fontWeight: 750,
                color: 'var(--text-primary)',
              }}
            >
              Research Problem
            </h2>
          </div>
          <p
            style={{
              fontSize: '0.95rem',
              color: 'var(--text-secondary)',
              lineHeight: 1.75,
              margin: 0,
            }}
          >
            {RESEARCH_PROBLEM}
          </p>
        </div>

        {/* Research Question */}
        <div
          className="glass-card fade-in"
          style={{ marginBottom: 28, padding: '28px 24px', borderLeft: '4px solid var(--primary)' }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 14 }}>
            <HelpCircle size={20} style={{ color: 'var(--primary)' }} />
            <h2
              style={{
                fontSize: '1.2rem',
                fontWeight: 750,
                color: 'var(--text-primary)',
              }}
            >
              Research Question
            </h2>
          </div>
          <p
            style={{
              fontSize: '0.95rem',
              color: 'var(--text-secondary)',
              lineHeight: 1.75,
              fontStyle: 'italic',
              margin: 0,
            }}
          >
            {RESEARCH_QUESTION}
          </p>
        </div>

        {/* Objectives */}
        <div
          className="glass-card fade-in"
          style={{ marginBottom: 28, padding: '28px 24px' }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 18 }}>
            <Target size={20} style={{ color: 'var(--accent-genuine)' }} />
            <h2
              style={{
                fontSize: '1.2rem',
                fontWeight: 750,
                color: 'var(--text-primary)',
              }}
            >
              Research Objectives
            </h2>
          </div>
          <ol
            style={{
              paddingLeft: 20,
              margin: 0,
              display: 'flex',
              flexDirection: 'column',
              gap: 10,
            }}
          >
            {OBJECTIVES.map((obj, i) => (
              <li
                key={i}
                style={{
                  fontSize: '0.92rem',
                  color: 'var(--text-secondary)',
                  lineHeight: 1.6,
                }}
              >
                {obj}
              </li>
            ))}
          </ol>
        </div>

        {/* Methodology Pipeline */}
        <div
          className="glass-card fade-in"
          style={{ padding: '28px 24px' }}
        >
          <div style={{ textAlign: 'center', marginBottom: 28 }}>
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
              End-to-end pipeline
            </p>
            <h2
              style={{
                fontSize: '1.4rem',
                fontWeight: 750,
                color: 'var(--text-primary)',
              }}
            >
              Methodology Flow
            </h2>
          </div>

          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 0,
            }}
          >
            {PIPELINE_STEPS.map((step, i) => {
              const Icon = step.icon;
              const isLast = i === PIPELINE_STEPS.length - 1;
              return (
                <div key={i} style={{ textAlign: 'center', width: '100%', maxWidth: 400 }}>
                  <div
                    className="glass-card"
                    style={{
                      padding: '14px 20px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: 14,
                      margin: '0 auto',
                      borderLeft: `4px solid var(--primary)`,
                    }}
                  >
                    <div
                      style={{
                        width: 38,
                        height: 38,
                        borderRadius: 10,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        background: 'var(--primary-glow)',
                        color: 'var(--primary)',
                        flexShrink: 0,
                      }}
                    >
                      <Icon size={18} />
                    </div>
                    <div style={{ textAlign: 'left' }}>
                      <h4
                        style={{
                          fontSize: '0.9rem',
                          fontWeight: 700,
                          color: 'var(--text-primary)',
                          margin: 0,
                        }}
                      >
                        {step.label}
                      </h4>
                      <p
                        style={{
                          fontSize: '0.78rem',
                          color: 'var(--text-muted)',
                          margin: '2px 0 0',
                        }}
                      >
                        {step.desc}
                      </p>
                    </div>
                  </div>
                  {!isLast && (
                    <div
                      style={{
                        display: 'flex',
                        justifyContent: 'center',
                        padding: '6px 0',
                      }}
                    >
                      <ArrowDown
                        size={18}
                        style={{ color: 'var(--text-muted)' }}
                      />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
