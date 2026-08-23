import os
import sys
import traceback
import time

# Add root directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.preprocessing.prepare_dataset import inspect_and_prepare
from ml.training.train_models import train_and_evaluate
from ml.training.compare_models import select_best_model
from ml.training.tune_model import tune_hyperparameters
from ml.evaluation.evaluate import evaluate_best_model
from ml.explainability.feature_importance import extract_global_feature_importance

def main():
    print("======================================================================")
    print("                 TRUTHLENS ML PIPELINE INITIALIZATION                 ")
    print("======================================================================")
    start_time = time.time()
    
    try:
        # Phase 1: Preprocess and Prepare
        print("\n>>> Phase 1: Preprocessing & Inspecting Dataset...")
        inspect_and_prepare()
        
        # Phase 2: Hyperparameter Tuning
        print("\n>>> Phase 2: Hyperparameter Tuning...")
        tune_hyperparameters()
        
        # Phase 3: Train and Evaluate Models
        print("\n>>> Phase 3: Training All Classifiers (Logistic Regression, MNB, Linear SVM)...")
        train_and_evaluate()
        
        # Phase 4: Model Selection
        print("\n>>> Phase 4: Comparing Models & Selecting Best Model...")
        best_model_name, best_perf = select_best_model()
        
        # Phase 5: Final Evaluation on Test Set
        print("\n>>> Phase 5: Evaluating Selected Best Model on Touched Test Dataset...")
        test_metrics = evaluate_best_model()
        
        # Phase 6: Explainability Feature Importance Extraction
        print("\n>>> Phase 6: Extracting Global Feature Importance...")
        extract_global_feature_importance()
        
        elapsed = time.time() - start_time
        print("\n======================================================================")
        print("                 TRUTHLENS ML PIPELINE COMPLETED                      ")
        print(f"Elapsed Time: {elapsed/60:.2f} minutes")
        print(f"Best Model Selected: {best_model_name}")
        print(f"Test Accuracy: {test_metrics['accuracy']:.4f}")
        print(f"Test F1-Score: {test_metrics['f1_score']:.4f}")
        print("======================================================================")
        
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed with error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
