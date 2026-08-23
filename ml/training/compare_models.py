import os
import sys
import pandas as pd
import joblib
import json
import shutil
from pathlib import Path

# Add parent directory to path to ensure ml package is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.config import ARTIFACTS_DIR, RESULTS_DIR

def select_best_model():
    print("Selecting the best performing model...")
    comparison_json_path = RESULTS_DIR / "model_comparison.json"
    
    if not comparison_json_path.exists():
        raise FileNotFoundError(f"Model comparison metrics not found at {comparison_json_path}. Please run train_models.py first.")
        
    with open(comparison_json_path, 'r') as f:
        results = json.load(f)
        
    if not results:
        raise ValueError("Comparison results JSON is empty.")
        
    # Sort by F1-Score descending (and accuracy as tie-breaker)
    sorted_results = sorted(results, key=lambda x: (x['F1_Score'], x['Accuracy']), reverse=True)
    
    best_perf = sorted_results[0]
    best_model_name = best_perf['Model']
    print(f"\n==================================================")
    print(f"BEST MODEL SELECTED: {best_model_name}")
    print(f"F1-Score: {best_perf['F1_Score']:.4f}")
    print(f"Accuracy: {best_perf['Accuracy']:.4f}")
    print(f"==================================================\n")
    
    # Copy best model file to best_model.joblib
    model_filename = best_model_name.lower().replace(" ", "_") + ".joblib"
    src_model_path = ARTIFACTS_DIR / model_filename
    dst_model_path = ARTIFACTS_DIR / "best_model.joblib"
    
    if not src_model_path.exists():
        raise FileNotFoundError(f"Source model file {src_model_path} not found.")
        
    shutil.copyfile(src_model_path, dst_model_path)
    print(f"Copied {src_model_path.name} to {dst_model_path.name}")
    
    # Save model metadata
    metadata = {
        "best_model_name": best_model_name,
        "validation_metrics": best_perf,
        "hyperparameters": {
            "Logistic Regression": {"max_iter": 1000, "C": 1.0},
            "Multinomial Naive Bayes": {"alpha": 1.0},
            "Linear SVM": {"C": 1.0, "dual": False, "calibrated": True}
        }
    }
    
    metadata_path = ARTIFACTS_DIR / "model_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print(f"Saved best model metadata to {metadata_path}")
    
    # Keep directory clean - optionally remove intermediate model files to save space
    # but we can keep them for presentation / display in the dashboard
    
    return best_model_name, best_perf

if __name__ == "__main__":
    select_best_model()
