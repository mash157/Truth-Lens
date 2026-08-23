# TruthLens

### AI-Based Fake News Classification & Explainable Analysis System

> *Question the News. Understand the Signal.*

TruthLens is an NLP and Machine Learning based system that classifies news articles as **Likely Genuine** or **Likely Fake** and provides explainable textual features behind the prediction. It uses TF-IDF vectorization, multiple supervised classifiers, and Explainable AI to reveal which words and phrases influenced the model's decision.

TruthLens is **not** an independent fact-checking system. It predicts based on patterns learned from labelled training data.

---

## Live Demo

- **Frontend:** Coming Soon
- **Backend API:** Coming Soon

---

## Key Features

- NLP-based Fake News Classification
- TF-IDF Feature Extraction (unigrams & bigrams)
- Three trained classifiers: Logistic Regression, Multinomial Naive Bayes, Linear SVM
- Model comparison with Accuracy, Precision, Recall, and F1-Score
- Best model selection based on validation performance
- Explainable AI with supporting and opposing feature contributions
- Confusion matrix visualization
- Research Dashboard with dataset statistics and feature importance
- Light / Dark mode toggle
- FastAPI backend with local ML inference
- React + Vite frontend

---

## How It Works

```
News Article
      ↓
Text Cleaning
      ↓
Title + Body Combination
      ↓
TF-IDF Vectorization
      ↓
Machine Learning Classification
      ↓
Confidence Calculation
      ↓
Explainable AI
      ↓
Result + Important Features
```

The user enters a news headline and article body. The text is cleaned, combined, and converted into TF-IDF feature vectors. The best-trained classifier predicts the class and a confidence score. Feature contribution analysis then identifies the words that most supported or opposed the prediction.

---

## Screenshots

### Home Page

![Home Page](screenshots/home.png)

### Analyze — Genuine News

![Genuine News Analysis](screenshots/analyze-genuine.png)

### Analyze — Fake News

![Fake News Analysis](screenshots/analyze-fake.png)

### Explainable AI & Feature Importance

![Dashboard — Explainable AI](screenshots/dashboard.png)

### Research Methodology

![Research Page](screenshots/research.png)

### Model Information

![Model Page](screenshots/model.png)

### How It Works

![How It Works](screenshots/how-it-works.png)

### Dark Mode

![Dark Mode](screenshots/dark-mode.png)

---

## Technology Stack

### Frontend

| Technology | Purpose |
|---|---|
| React | UI framework |
| Vite | Build tool and dev server |
| JavaScript | Application logic |
| CSS | Styling with CSS variables |
| Lucide React | Icon library |
| Recharts | Chart visualizations |

### Backend

| Technology | Purpose |
|---|---|
| Python | Server-side language |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |

### Machine Learning

| Technology | Purpose |
|---|---|
| Scikit-learn | ML framework |
| TF-IDF | Text feature extraction |
| Logistic Regression | Classifier |
| Multinomial Naive Bayes | Classifier |
| Linear SVM (Calibrated) | Classifier |

### Explainability

Feature importance and textual feature contribution analysis using model coefficients and TF-IDF weights. For each prediction, supporting features (words pushing toward the predicted class) and opposing features (words pushing against it) are extracted and displayed.

---

## ML Pipeline

1. **Dataset Preparation** — Load the WELFake dataset (72,134 articles)
2. **Missing Value Handling** — Fill or drop rows with missing title/text
3. **Duplicate Removal** — Remove duplicate title+text pairs
4. **Text Cleaning** — Lowercase, HTML stripping, whitespace normalization
5. **Title + Body Combination** — Merge headline and article text
6. **Stratified Split** — Train (70%), Validation (15%), Test (15%)
7. **TF-IDF Vectorization** — 10,000 features, unigrams & bigrams, sublinear TF
8. **Model Training** — Train Logistic Regression, Multinomial Naive Bayes, Linear SVM
9. **Model Comparison** — Evaluate on validation set using Accuracy, Precision, Recall, F1-Score
10. **Best Model Selection** — Select the classifier with the highest F1-Score
11. **Test Evaluation** — Final evaluation on the held-out test set
12. **Feature Importance** — Extract global and local feature contributions

---

## Model Evaluation

### Validation Set Comparison

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.9580 | 0.9522 | 0.9555 | 0.9538 |
| Multinomial Naive Bayes | 0.8592 | 0.8239 | 0.8770 | 0.8496 |
| **Linear SVM** | **0.9672** | **0.9651** | **0.9626** | **0.9638** |

### Best Model — Linear SVM (Test Set)

| Metric | Value |
|---|---:|
| Accuracy | 0.9644 |
| Precision | 0.9616 |
| Recall | 0.9598 |
| F1-Score | 0.9607 |

### Confusion Matrix (Test Set)

|  | Predicted Genuine | Predicted Fake |
|---|---:|---:|
| **Actual Genuine** | 5,053 (TN) | 166 (FP) |
| **Actual Fake** | 174 (FN) | 4,159 (TP) |

---

## Research Objectives

1. Develop a Machine Learning-based fake-news classification system.
2. Use NLP techniques for processing news text.
3. Apply TF-IDF for feature extraction.
4. Train multiple supervised Machine Learning models.
5. Compare model performance.
6. Select the best-performing practical model.
7. Use Explainable AI to identify important textual features.
8. Develop a user-friendly web application.
9. Evaluate the system using standard classification metrics.
10. Clearly communicate the limitations of automated fake-news classification.

---

## Research Question

> How effectively can NLP-based Machine Learning models classify fake and genuine news using textual features, and how can Explainable AI help users understand the model's predictions?

---

## Disclaimer

TruthLens provides a machine-learning-based classification based on patterns learned from labelled training data. It does not independently verify factual claims. Predictions may be incorrect, so important information should always be verified using reliable independent sources.

TruthLens is **not** an independent fact-checking system. It is an academic research project demonstrating NLP-based text classification with explainable AI.

---

## Project Structure

```
TruthLens/
├── backend/            # FastAPI backend server
│   └── app/
│       ├── main.py     # Application entry point
│       ├── routes/     # API route handlers
│       ├── services/   # Prediction, explanation, metrics
│       ├── ml/         # Model loader, preprocessing
│       ├── schemas/    # Pydantic request/response models
│       └── utils/      # Config, logging
├── frontend/           # React + Vite application
│   └── src/
│       ├── components/ # UI components
│       ├── pages/      # Route pages
│       ├── hooks/      # Custom hooks (useTheme)
│       ├── services/   # API client
│       └── utils/      # Constants, formatters
├── ml/                 # Machine learning pipeline
│   ├── artifacts/      # Trained models, vectorizer, metadata
│   ├── results/        # Metrics, comparisons, feature importance
│   ├── preprocessing/  # Text cleaning, dataset preparation
│   ├── training/       # Model training and comparison
│   ├── evaluation/     # Test set evaluation
│   └── explainability/ # Feature importance, LIME
├── dataset/            # WELFake dataset (raw and processed)
├── scripts/            # Training entry point
├── screenshots/        # Project screenshots
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm

### Backend Setup

```bash
pip install -r backend/requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173` and the backend at `http://localhost:8000`.

---

## Author

Made With ❤️ by **@mash157**

© All Rights Reserved 2026
