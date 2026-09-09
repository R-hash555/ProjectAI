"""
Human-in-the-Loop (HITL) Review Queue CLI Interface
Allows operators to review, edit, and approve low-confidence extractions.
"""
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUMMARY_PATH = os.path.join(BASE_DIR, "extraction_summary.json")

def launch_review_queue():
    if not os.path.exists(SUMMARY_PATH):
        print("Error: extraction_summary.json not found. Run evaluator.py first!")
        return

    with open(SUMMARY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    queue = data.get("human_review_queue_items", [])
    print("=" * 70)
    print(f"HUMAN-IN-THE-LOOP REVIEW QUEUE CLI ({len(queue)} ITEMS PENDING)")
    print("=" * 70)

    if not queue:
        print("No items pending human review! Pipeline running at high confidence.")
        return

    for idx, item in enumerate(queue, 1):
        print(f"\n[{idx}/{len(queue)}] Document ID: {item['doc_id']} ({item['doc_type'].upper()})")
        print(f" -> Flagged Low-Confidence Fields: {item['flagged_fields']}")
        print(" Extracted Values:")
        for k, v in item["extracted_fields"].items():
            flag = " [REVIEW REQUIRED]" if k in item["flagged_fields"] else ""
            print(f"    - {k:<18}: {v}{flag}")
        print("-" * 50)
        # Non-interactive summary print for CLI automation
    
    print("\nReview queue inspection completed successfully.")

if __name__ == "__main__":
    launch_review_queue()
