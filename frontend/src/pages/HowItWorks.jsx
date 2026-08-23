import {
  FileText,
  Eraser,
  Merge,
  Binary,
  BrainCircuit,
  Gauge,
  Lightbulb,
  Sparkles,
  ArrowDown,
} from 'lucide-react';

const PIPELINE = [
  {
    icon: FileText,
    title: 'User Enters News',
    description:
      'The user pastes a news headline and article body into the TruthLens interface. The system accepts the raw text input for analysis.',
  },
  {
    icon: Eraser,
    title: 'Text Cleaning',
    description:
      'The raw text is preprocessed: HTML tags are removed, text is converted to lowercase, extra whitespace is normalized, and empty or invalid characters are stripped.',
  },
  {
    icon: Merge,
    title: 'Title + Article Combination',
    description:
      'The cleaned headline and body text are combined into a single text string. This gives the model access to both the title context and the full article content.',
  },
  {
    icon: Binary,
    title: 'TF-IDF Vectorization',
    description:
      'Term Frequency-Inverse Document Frequency (TF-IDF) converts the combined text into numerical feature vectors. Words that are common across articles receive lower weights, while distinctive words receive higher weights.',
  },
  {
    icon: BrainCircuit,
    title: 'Machine Learning Prediction',
    description:
      'The pre-trained best classification model (Linear SVM) processes the TF-IDF vectors and predicts whether the article is likely fake or likely genuine.',
  },
  {
    icon: Gauge,
    title: 'Confidence Calculation',
    description:
      'The model calculates a confidence score representing how strongly it supports its predicted class. This score helps users understand the certainty of the prediction.',
  },
  {
    icon: Lightbulb,
    title: 'Explainable AI',
    description:
      'Feature contribution analysis identifies which words and phrases most influenced the prediction. Supporting and opposing features are extracted using model coefficients and TF-IDF weights.',
  },
  {
    icon: Sparkles,
    title: 'Result Display',
    description:
      'The classification result, confidence score, and explainable feature contributions are displayed in a clear, academic format for the user to review.',
  },
];

export default function HowItWorks() {
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
            letterSpacing: '-0.03em',
            marginBottom: 12,
            background: 'linear-gradient(135deg, var(--primary) 0%, #06b6d4 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          How TruthLens Works
        </h1>
        <p
          style={{
            fontSize: '1rem',
            color: 'var(--text-secondary)',
            lineHeight: 1.65,
          }}
        >
          A step-by-step breakdown of the TruthLens classification and
          explainability pipeline.
        </p>
      </section>

      <div className="container" style={{ maxWidth: 700 }}>
        {/* Pipeline */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 0,
          }}
        >
          {PIPELINE.map((step, i) => {
            const Icon = step.icon;
            const isLast = i === PIPELINE.length - 1;
            return (
              <div key={i} style={{ width: '100%', textAlign: 'center' }}>
                <div
                  className="glass-card fade-in"
                  style={{
                    padding: '24px 28px',
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: 20,
                    textAlign: 'left',
                  }}
                >
                  <div
                    style={{
                      width: 50,
                      height: 50,
                      borderRadius: 14,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      background: 'var(--primary-glow)',
                      color: 'var(--primary)',
                      flexShrink: 0,
                    }}
                  >
                    <Icon size={24} />
                  </div>
                  <div>
                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 10,
                        marginBottom: 6,
                      }}
                    >
                      <span
                        style={{
                          fontSize: '0.72rem',
                          fontWeight: 700,
                          color: 'var(--primary)',
                          background: 'var(--primary-glow)',
                          padding: '2px 8px',
                          borderRadius: 999,
                          textTransform: 'uppercase',
                          letterSpacing: '0.06em',
                        }}
                      >
                        Step {i + 1}
                      </span>
                      <h3
                        style={{
                          fontSize: '1.05rem',
                          fontWeight: 700,
                          color: 'var(--text-primary)',
                          margin: 0,
                        }}
                      >
                        {step.title}
                      </h3>
                    </div>
                    <p
                      style={{
                        fontSize: '0.88rem',
                        color: 'var(--text-secondary)',
                        lineHeight: 1.65,
                        margin: 0,
                      }}
                    >
                      {step.description}
                    </p>
                  </div>
                </div>
                {!isLast && (
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'center',
                      padding: '8px 0',
                    }}
                  >
                    <ArrowDown
                      size={20}
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
  );
}
