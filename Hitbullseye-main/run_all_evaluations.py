"""
Master Reproducible Evaluation Suite Runner
Runs unit tests, benchmark evaluation engines, chart visualizer exporters, and CSV report generators across all 3 assignments.
"""
import os
import sys
import subprocess
import json
from typing import List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_step(step_name: str, cmd: List[str], cwd: str):
    print(f"\n[{step_name}] Executing: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED [{step_name}]:\n{res.stderr}")
        sys.exit(1)
    print(f"SUCCESS [{step_name}]")
    return res.stdout

def main():
    print("=" * 80)
    print("REPRODUCIBLE AI/ML BENCHMARK SUITE - MASTER EVALUATION RUNNER")
    print("=" * 80)

    # 1. Assignment 3 Evaluation
    a3_dir = os.path.join(BASE_DIR, "Assignment_3_Prompt_Engineering_Library")
    run_step("Assignment 3 Tests", [sys.executable, "-m", "pytest", "tests/test_evaluator.py"], cwd=a3_dir)
    run_step("Assignment 3 Evaluation", [sys.executable, "evaluate.py"], cwd=a3_dir)

    # 2. Assignment 4 Evaluation
    a4_dir = os.path.join(BASE_DIR, "Assignment_4_AI_Coding_Workflow")
    run_step("Assignment 4 Evaluation", [sys.executable, "evaluation_runner.py"], cwd=a4_dir)

    # 3. Assignment 5 Evaluation
    a5_dir = os.path.join(BASE_DIR, "Assignment_5_Document_Extraction_Pipeline")
    run_step("Assignment 5 Data Generator", [sys.executable, "generate_data.py"], cwd=a5_dir)
    run_step("Assignment 5 Evaluation", [sys.executable, "evaluator.py"], cwd=a5_dir)

    # 4. Integrity Check on Output Artifacts
    expected_files = [
        # Assignment 3
        os.path.join(a3_dir, "evaluation_results.json"),
        os.path.join(a3_dir, "assignment3_results.csv"),
        os.path.join(a3_dir, "charts", "prompt_performance_comparison.png"),
        os.path.join(a3_dir, "charts", "format_compliance_breakdown.png"),
        # Assignment 4
        os.path.join(a4_dir, "productivity_summary.json"),
        os.path.join(a4_dir, "assignment4_results.csv"),
        os.path.join(a4_dir, "charts", "coding_time_breakdown.png"),
        os.path.join(a4_dir, "charts", "task_category_speedup_defects.png"),
        # Assignment 5
        os.path.join(a5_dir, "extraction_summary.json"),
        os.path.join(a5_dir, "assignment5_results.csv"),
        os.path.join(a5_dir, "charts", "field_accuracy_breakdown.png"),
        os.path.join(a5_dir, "charts", "cost_and_routing_economics.png")
    ]

    print("\n" + "=" * 80)
    print("OUTPUT ARTIFACT INTEGRITY VERIFICATION")
    print("=" * 80)
    all_ok = True
    for fpath in expected_files:
        rel_path = os.path.relpath(fpath, BASE_DIR)
        if os.path.exists(fpath) and os.path.getsize(fpath) > 0:
            print(f" [PASS] {rel_path:<60} ({os.path.getsize(fpath)} bytes)")
        else:
            print(f" [FAIL] {rel_path:<60} (Missing or empty!)")
            all_ok = False

    print("=" * 80)
    if all_ok:
        print("ALL EVALUATIONS AND VISUALIZATION ARTIFACTS GENERATED SUCCESSFULLY!")
    else:
        print("SOME ARTIFACTS WERE MISSING OR FAILED TO GENERATE.")
    print("=" * 80)

if __name__ == "__main__":
    main()
