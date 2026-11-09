import os
import sys
import pandas as pd
import joblib
import json
import matplotlib
# Use Agg backend for matplotlib to prevent GUI popup windows in headless environments
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)

# Add parent directory to path to ensure ml package is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.config import (
    TEST_DATA_PATH,
    ARTIFACTS_DIR,
    RESULTS_DIR
)

def evaluate_best_model():
    print("Evaluating best model on test set...")
    
    # 1. Load Artifacts
    best_model_path = ARTIFACTS_DIR / "best_model.joblib"
    vectorizer_path = ARTIFACTS_DIR / "tfidf_vectorizer.joblib"
    metadata_path = ARTIFACTS_DIR / "model_metadata.json"
    
    if not (best_model_path.exists() and vectorizer_path.exists() and metadata_path.exists()):
        raise FileNotFoundError("Best model artifacts not found. Please run training and selection first.")
        
    model = joblib.load(best_model_path)
    vectorizer = joblib.load(vectorizer_path)
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
        
    best_model_name = metadata["best_model_name"]
    print(f"Loaded best model: {best_model_name}")
    
    # 2. Load Test Data
    test_df = pd.read_csv(TEST_DATA_PATH)
    test_df['combined_text'] = test_df['combined_text'].fillna("")
    
    X_test = test_df['combined_text']
    y_test = test_df['label']
    
    print(f"Test dataset size: {len(X_test)}")
    
    # 3. Vectorize and Predict
    X_test_vec = vectorizer.transform(X_test)
    preds = model.predict(X_test_vec)
    
    # Check if probabilities are available
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X_test_vec)
    else:
        probs = None
        
    # 4. Calculate Metrics
    accuracy = accuracy_score(y_test, preds)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, preds, average='binary')
    
    report_dict = classification_report(y_test, preds, output_dict=True)
    report_str = classification_report(y_test, preds)
    
    print("\nTest Set Classification Report:")
    print(report_str)
    
    # 5. Confusion Matrix
    cm = confusion_matrix(y_test, preds)
    print("Confusion Matrix:")
    print(cm)
    
    # Plot Confusion Matrix
    plt.figure(figsize=(6, 5))
    # Labels: 0 = Genuine, 1 = Fake
    classes = ['Genuine', 'Fake']
    
    # Custom color palette matching the sleek look: deep blues
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(f'Confusion Matrix - {best_model_name}', fontsize=12, pad=15)
    plt.colorbar()
    
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=0)
    plt.yticks(tick_marks, classes)
    
    # Text annotations in matrix cells
    thresh = cm.max() / 2.
    for i, j in np.ndindex(cm.shape):
        plt.text(j, i, format(cm[i, j], 'd'),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black",
                 fontsize=14, weight='bold')
                 
    plt.ylabel('Actual Label', fontsize=10, labelpad=10)
    plt.xlabel('Predicted Label', fontsize=10, labelpad=10)
    plt.tight_layout()
    
    cm_plot_path = RESULTS_DIR / "confusion_matrix.png"
    plt.savefig(cm_plot_path, dpi=300)
    plt.close()
    print(f"Saved confusion matrix plot to {cm_plot_path}")
    
    # 6. Save Metrics JSON
    metrics_summary = {
        "model_name": best_model_name,
        "accuracy": float(round(accuracy, 4)),
        "precision": float(round(precision, 4)),
        "recall": float(round(recall, 4)),
        "f1_score": float(round(f1, 4)),
        "confusion_matrix": {
            "true_negative": int(cm[0, 0]),
            "false_positive": int(cm[0, 1]),
            "false_negative": int(cm[1, 0]),
            "true_positive": int(cm[1, 1])
        },
        "classification_report": report_dict
    }
    
    metrics_json_path = RESULTS_DIR / "metrics.json"
    with open(metrics_json_path, 'w') as f:
        json.dump(metrics_summary, f, indent=4)
        
    print(f"Saved final evaluation metrics to {metrics_json_path}")
    
    # Update model metadata with final test metrics
    metadata["test_metrics"] = {
        "accuracy": metrics_summary["accuracy"],
        "precision": metrics_summary["precision"],
        "recall": metrics_summary["recall"],
        "f1_score": metrics_summary["f1_score"]
    }
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    return metrics_summary

if __name__ == "__main__":
    evaluate_best_model()
