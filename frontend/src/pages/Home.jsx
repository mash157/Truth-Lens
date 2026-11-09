import { Link } from 'react-router-dom';
import { ArrowRight, BarChart3, BookOpen, BrainCircuit, CheckCircle2, FileText, Lightbulb, Search, ShieldCheck, Sparkles } from 'lucide-react';
import Disclaimer from '../components/Disclaimer';
import GlobalBackground from '../components/GlobalBackground';

const FEATURES = [
  { icon: BrainCircuit, title: 'NLP Classification', desc: 'TF-IDF vectorization extracts meaningful textual features from news articles for supervised classification.', tone: 'pink' },
  { icon: Lightbulb, title: 'Explainable AI', desc: "See which words and phrases influenced the model's prediction — no black box.", tone: 'purple' },
  { icon: BarChart3, title: 'Model Insights', desc: 'Explore performance, key features, and prediction confidence in an interactive dashboard.', tone: 'blue' },
];

function NewsCard() {
  return (
    <div className="news-float glass-float-card">
      <div className="news-card-inner">
        <div className="news-icon">
          <FileText size={22} strokeWidth={2} />
        </div>

        <div className="news-card-info">
          <div className="news-card-title">News Analysis</div>

          <div className="news-placeholder-lines">
            <span />
            <span />
            <span />
          </div>
        </div>

        <div className="news-check">
          <CheckCircle2 size={19} strokeWidth={2} />
        </div>
      </div>
    </div>
  );
}

function PredictionCard() {
  return (
    <div className="prediction-float glass-float-card">
      <div className="prediction-card-inner">
        <div className="prediction-card-header">
          <BarChart3 size={21} strokeWidth={2} />
          <span>AI Prediction</span>
        </div>

        <div className="prediction-card-details">
          <div className="prediction-ring">
            <div className="prediction-ring-center">
              <span>92%</span>
            </div>
          </div>

          <div className="prediction-indicators">
            <div><i /><span /></div>
            <div><i /><span /></div>
            <div><i /><span /></div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <div className="home-page">
      <section className="hero-section">
        <GlobalBackground variant="home" embedded />
        <div className="hero-content">
          {/* Badge, heading, description, CTA buttons, disclaimer */}
          <div className="hero-badge"><Sparkles size={16} /> Explainable AI · NLP · Machine Learning</div>
          <h1>Question the News.<br /><span>Understand the Signal.</span></h1>
          <p>TruthLens uses Natural Language Processing and Machine Learning to classify news content and reveal the textual patterns behind its prediction.</p>
          <div className="hero-actions"><Link to="/analyze" className="btn btn-primary"><Search size={19} /> Analyze News <ArrowRight size={17} /></Link><Link to="/research" className="btn btn-secondary"><BookOpen size={19} /> Explore Research</Link></div>
          <div className="hero-disclaimer"><ShieldCheck size={17} /> Machine-learning prediction — <b>not independent fact verification</b></div>
        </div>
        <div className="hero-cards">
          <NewsCard />
          <PredictionCard />
        </div>
      </section>

      <section className="features-section container">
        <div className="section-heading">
          <span>Built for transparency</span>
          <div className="section-title-row"><i aria-hidden="true" /><h2>Core Features</h2><i aria-hidden="true" /></div>
        </div>
        <div className="feature-grid">{FEATURES.map(({ icon: Icon, title, desc, tone }) => <article className={`feature-card ${tone}`} key={title}><div className="feature-icon"><Icon size={25} /></div><div><h3>{title}</h3><p>{desc}</p></div></article>)}</div>
      </section>
      <section className="container home-lower"><div className="section-heading"><span>From text to insight</span><h2>How TruthLens Works</h2></div><div className="steps-grid">{['Input','Preprocess','Vectorize','Classify','Explain','Result'].map((step, i) => <div className="step-card glass-card" key={step}><b>0{i + 1}</b><h4>{step}</h4><p>{['Paste a news article.','Text is cleaned and normalized.','TF-IDF converts text to features.','ML model predicts the class.','Key features are highlighted.','Prediction and explanation displayed.'][i]}</p></div>)}</div></section>
      <section className="container home-lower"><div className="research-callout glass-card"><div><h2>Built as a research project, not just a classifier.</h2><p>Explore the dataset, methodology, model comparison, evaluation metrics, and Explainable AI approach behind TruthLens.</p></div><Link to="/research" className="btn btn-secondary">View Methodology <ArrowRight size={16} /></Link></div></section>
      <section className="container home-disclaimer"><Disclaimer /></section>
    </div>
  );
}