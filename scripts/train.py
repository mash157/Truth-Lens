import os
import sys
import traceback
import time

# Add root directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.preprocessing.prepare_dataset import inspect_and_prepare
from ml.training import experiment_pipeline as ep

N_CV_FOLDS = ep.N_CV_FOLDS


def main():
    print("======================================================================")
    print("                 TRUTHLENS ML PIPELINE INITIALIZATION                 ")
    print("======================================================================")
    start_time = time.time()

    try:
        # Phase 1: Preprocess and Prepare (dedup + stratified splits)
        print("\n>>> Phase 1: Preprocessing & Inspecting Dataset...")
        inspect_and_prepare()

        # Phase 2: Experiments (checkpointed stages)
        print("\n>>> Phase 2: Running Experiment Stages...")
        stage_fns = {
            "exp1": ep.ExperimentStages.exp1_baseline,
            "exp2": ep.ExperimentStages.exp2_word_configs,
            "exp3": ep.ExperimentStages.exp3_char,
            "exp4": ep.ExperimentStages.exp4_combined,
            "exp5": ep.ExperimentStages.exp5_model_comparison,
            "exp6": ep.ExperimentStages.exp6_svm_tuning,
        }
        for stage, fn in stage_fns.items():
            print(f"\n--- Stage {stage} ---")
            fn()

        # Phase 3: 5-fold Cross-Validation on train+val only
        print(f"\n>>> Phase 3: {N_CV_FOLDS}-Fold Cross-Validation...")
        for fold in range(N_CV_FOLDS):
            ep.run_cv_fold_stage(fold)

        # Phase 4: Final model, calibration, artifacts, external eval interface
        print("\n>>> Phase 4: Final Model + Artifacts...")
        ep.FinalStage.run()

        elapsed = time.time() - start_time
        print("\n======================================================================")
        print("                 TRUTHLENS ML PIPELINE COMPLETED                      ")
        print(f"Elapsed Time: {elapsed/60:.2f} minutes")
        print("======================================================================")

    except Exception as e:
        print(f"\n[ERROR] Pipeline failed with error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
