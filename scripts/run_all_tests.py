import os
import sys
import subprocess

def run_tests():
    print("======================================================================")
    print("                    TRUTHLENS TEST SUITE RUNNER                       ")
    print("======================================================================")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    backend_dir = os.path.join(project_root, "backend")
    
    # Verify pytest is installed
    try:
        import pytest
    except ImportError:
        print("[ERROR] pytest is not installed. Please run 'pip install pytest' first.")
        sys.exit(1)
        
    print(f"Running pytest inside: {backend_dir}")
    
    # Run pytest command using subprocess inside the backend directory
    # Cwd must be the backend directory so pytest.ini is read correctly
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v"],
        cwd=backend_dir,
        capture_output=False
    )
    
    print("======================================================================")
    if result.returncode == 0:
        print("                  TEST SUITE PASSED SUCCESSFULLY                      ")
    else:
        print("                  TEST SUITE FAILED (See errors above)                ")
    print("======================================================================")
    
    sys.exit(result.returncode)

if __name__ == "__main__":
    run_tests()
