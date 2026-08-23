// API configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Disclaimer
export const RESEARCH_DISCLAIMER = 
  "TruthLens provides a machine-learning-based classification based on patterns learned from labelled training data. " +
  "It does not independently verify factual claims. Predictions may be incorrect, so important information should always " +
  "be verified using reliable independent sources.";

// Academic research definitions
export const RESEARCH_QUESTION = 
  "How effectively can NLP-based Machine Learning models classify fake and genuine news using textual features, " +
  "and how can Explainable AI help users understand the model's predictions?";

export const RESEARCH_PROBLEM = 
  "Online misinformation spreads rapidly through digital platforms. Users often find it difficult to distinguish " +
  "potentially misleading news from reliable news. TruthLens proposes an NLP and Machine Learning-based classification " +
  "system that analyzes the textual patterns of news articles and provides an explainable prediction.";

export const OBJECTIVES = [
  "Develop a Machine Learning-based fake-news classification system.",
  "Use NLP techniques for processing news text.",
  "Apply TF-IDF for feature extraction.",
  "Train multiple supervised Machine Learning models.",
  "Compare model performance.",
  "Select the best-performing practical model.",
  "Use Explainable AI to identify important textual features.",
  "Develop a user-friendly web application.",
  "Evaluate the system using standard classification metrics.",
  "Clearly communicate the limitations of automated fake-news classification."
];
