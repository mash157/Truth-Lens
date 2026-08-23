import { Link } from 'react-router-dom';
import {
  BrainCircuit,
  Lightbulb,
  BarChart3,
  GraduationCap,
  Search,
  BookOpen,
  ArrowRight,
  ShieldCheck,
  Sparkles,
} from 'lucide-react';
import Disclaimer from '../components/Disclaimer';

const FEATURES = [
  {
    icon: BrainCircuit,
    title: 'NLP Classification',
    desc: 'TF-IDF vectorization extracts meaningful textual features from news articles for supervised classification.',
  },
  {
    icon: Lightbulb,
    title: 'Explainable AI',
    desc: "See which words and phrases influenced the model's prediction — no black box.",
  },
  {
    icon: BarChart3,
    title: 'Model Comparison',
    desc: 'Three classifiers compared using Accuracy, Precision, Recall, and F1-Score.',
  },
  {
    icon: GraduationCap,
    title: 'Research Dashboard',
    desc: 'Academic-grade metrics, confusion matrices, and dataset statistics in one view.',
  },
];

const STEPS = [
  {
    num: '01',
    title: 'Input',
    desc: 'Paste a news article.',
  },
  {
    num: '02',
    title: 'Preprocess',
    desc: 'Text is cleaned and normalized.',
  },
  {
    num: '03',
    title: 'Vectorize',
    desc: 'TF-IDF converts text to features.',
  },
  {
    num: '04',
    title: 'Classify',
    desc: 'ML model predicts the class.',
  },
  {
    num: '05',
    title: 'Explain',
    desc: 'Key features are highlighted.',
  },
  {
    num: '06',
    title: 'Result',
    desc: 'Prediction and explanation displayed.',
  },
];

export default function Home() {
  return (
    <div style={{ paddingBottom: 80 }}>
      {/* HERO */}
      <section
        style={{
          textAlign: 'center',
          padding: '90px 24px 70px',
          maxWidth: 900,
          margin: '0 auto',
        }}
      >
        {/* Small badge */}
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 8,
            padding: '8px 14px',
            borderRadius: 999,
            background: 'var(--primary-glow)',
            border: '1px solid var(--border)',
            color: 'var(--primary)',
            fontSize: '0.82rem',
            fontWeight: 600,
            marginBottom: 22,
          }}
        >
          <Sparkles size={15} />
          Explainable AI · NLP · Machine Learning
        </div>

        <h1
          style={{
            fontSize: 'clamp(2.4rem, 6vw, 4.4rem)',
            fontWeight: 850,
            lineHeight: 1.08,
            letterSpacing: '-0.04em',
            marginBottom: 20,
            background:
              'linear-gradient(135deg, var(--primary) 0%, #06b6d4 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          Question the News.
          <br />
          Understand the Signal.
        </h1>

        <p
          style={{
            fontSize: '1.12rem',
            color: 'var(--text-secondary)',
            maxWidth: 680,
            margin: '0 auto 34px',
            lineHeight: 1.75,
          }}
        >
          TruthLens uses Natural Language Processing and Machine Learning to
          classify news content and reveal the textual patterns behind its
          prediction.
        </p>

        <div
          style={{
            display: 'flex',
            gap: 14,
            justifyContent: 'center',
            flexWrap: 'wrap',
          }}
        >
          <Link to="/analyze" className="btn btn-primary">
            <Search size={17} />
            Analyze News
            <ArrowRight size={16} />
          </Link>

          <Link to="/research" className="btn btn-secondary">
            <BookOpen size={17} />
            Explore Research
          </Link>
        </div>

        {/* Academic disclaimer */}
        <div
          style={{
            marginTop: 28,
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            gap: 8,
            color: 'var(--text-secondary)',
            fontSize: '0.78rem',
          }}
        >
          <ShieldCheck size={15} />
          Machine-learning prediction — not independent fact verification
        </div>
      </section>

      {/* FEATURES */}
      <section className="container" style={{ marginTop: 25 }}>
        <div style={{ textAlign: 'center', marginBottom: 34 }}>
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
            Built for transparency
          </p>

          <h2
            style={{
              fontSize: '1.8rem',
              fontWeight: 750,
              color: 'var(--text-primary)',
            }}
          >
            Core Features
          </h2>
        </div>

        <div className="grid-2">
          {FEATURES.map((feature) => {
            const Icon = feature.icon;

            return (
              <div
                key={feature.title}
                className="glass-card"
                style={{
                  position: 'relative',
                  overflow: 'hidden',
                }}
              >
                <div
                  style={{
                    width: 46,
                    height: 46,
                    borderRadius: 14,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: 'var(--primary-glow)',
                    color: 'var(--primary)',
                    marginBottom: 16,
                  }}
                >
                  <Icon size={22} />
                </div>

                <h3
                  style={{
                    fontSize: '1.08rem',
                    fontWeight: 700,
                    marginBottom: 8,
                    color: 'var(--text-primary)',
                  }}
                >
                  {feature.title}
                </h3>

                <p
                  style={{
                    fontSize: '0.88rem',
                    color: 'var(--text-secondary)',
                    lineHeight: 1.65,
                    margin: 0,
                  }}
                >
                  {feature.desc}
                </p>
              </div>
            );
          })}
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="container" style={{ marginTop: 75 }}>
        <div style={{ textAlign: 'center', marginBottom: 34 }}>
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
            From text to insight
          </p>

          <h2
            style={{
              fontSize: '1.8rem',
              fontWeight: 750,
              color: 'var(--text-primary)',
            }}
          >
            How TruthLens Works
          </h2>
        </div>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns:
              'repeat(auto-fit, minmax(150px, 1fr))',
            gap: 16,
          }}
        >
          {STEPS.map((step) => (
            <div
              key={step.num}
              className="glass-card"
              style={{
                textAlign: 'center',
                padding: '24px 14px',
              }}
            >
              <span
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: 42,
                  height: 42,
                  borderRadius: '50%',
                  background: 'var(--primary-glow)',
                  color: 'var(--primary)',
                  fontWeight: 800,
                  fontSize: '0.8rem',
                  marginBottom: 13,
                }}
              >
                {step.num}
              </span>

              <h4
                style={{
                  fontSize: '0.95rem',
                  fontWeight: 700,
                  color: 'var(--text-primary)',
                  marginBottom: 6,
                }}
              >
                {step.title}
              </h4>

              <p
                style={{
                  fontSize: '0.8rem',
                  color: 'var(--text-secondary)',
                  lineHeight: 1.5,
                  margin: 0,
                }}
              >
                {step.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* RESEARCH CALLOUT */}
      <section
        className="container"
        style={{
          marginTop: 70,
        }}
      >
        <div
          className="glass-card"
          style={{
            padding: '32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: 24,
            flexWrap: 'wrap',
          }}
        >
          <div style={{ maxWidth: 650 }}>
            <h2
              style={{
                fontSize: '1.35rem',
                fontWeight: 750,
                color: 'var(--text-primary)',
                marginBottom: 8,
              }}
            >
              Built as a research project, not just a classifier.
            </h2>

            <p
              style={{
                margin: 0,
                color: 'var(--text-secondary)',
                fontSize: '0.9rem',
                lineHeight: 1.65,
              }}
            >
              Explore the dataset, methodology, model comparison,
              evaluation metrics, and Explainable AI approach behind
              TruthLens.
            </p>
          </div>

          <Link to="/research" className="btn btn-secondary">
            View Methodology
            <ArrowRight size={16} />
          </Link>
        </div>
      </section>

      {/* DISCLAIMER */}
      <section className="container" style={{ marginTop: 50 }}>
        <Disclaimer />
      </section>
    </div>
  );
}