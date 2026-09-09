# Document Extraction Pipeline: Empirical Accuracy & Cost Report

## Executive Summary

This report presents field-level extraction accuracy, confidence calibration metrics, human-in-the-loop (HITL) routing rules, and unit cost accounting for a 100-document evaluation benchmark across BFSI back-office document types (Invoices, Insurance Claims, and Identity Cards).

---

## 1. Field-Level Accuracy Breakdown

> [!IMPORTANT]
> Aggregate document accuracy of ~96% masks field-level noise variations. High-precision structured fields (e.g., `date`, `claim_id`, `total_amount`) perform at **100.0%**, while noisy or low-contrast fields (e.g., `id_number`, `hospital_name`) range between **89.66%** and **91.18%**.

| Field Name | Target Entity | Benchmark Accuracy | Failure Mode / Note |
|---|---|---|---|
| `date` / `tax_amount` / `total_amount` | Invoice | **100.0%** | Passed clean validation |
| `claim_id` / `claimant_name` / `incident_date` | Insurance Claim | **100.0%** | Passed clean validation |
| `full_name` / `date_of_birth` / `issue_date` | Identity Card | **100.0%** | Passed clean validation |
| `invoice_no` | Invoice | **97.06%** | Minor OCR character confusion (0 vs O) |
| `address` | Identity Card | **96.55%** | Suite number OCR noise |
| `vendor_name` / `policy_number` / `diagnosis_code` | Various | **94.12%** | High regex precision |
| `hospital_name` | Claim | **91.18%** | Long text string OCR error |
| `id_number` | Identity Card | **89.66%** | Low contrast scan noise |

---

## 2. Confidence Calibration & Routing Threshold Tuning

### Routing Rule Architecture
- **Auto-Acceptance Threshold**: Overall Document Confidence $\ge 0.85$ AND All Field Confidences $\ge 0.78$.
- **Human Review Queue**: Overall Confidence between $0.50$ and $0.85$ OR Any Field Confidence $< 0.78$.
- **Rejection Threshold**: Document corrupt OR Overall Confidence $< 0.50$.

### Benchmark Routing Results
- **Auto-Accepted (Zero-Touch)**: **34.0%** (34 docs)
- **Human Review Queue**: **63.0%** (63 docs)
- **System Rejected**: **3.0%** (3 corrupt/unreadable docs)

---

## 3. Unit Cost Accounting & ROI Analysis

| Cost Factor | Pure Manual Entry | Hybrid AI Extraction Pipeline |
|---|---|---|
| **Cost per Document** | **$2.50** | **$0.838** ($0.05 API + $0.788 review labor) |
| **Total Batch Cost (100 Docs)** | **$250.00** | **$83.75** |
| **Net Cost Savings** | Baseline | **66.5% Savings** ($166.25 saved per 100 docs) |
| **Processing Velocity** | 4-6 hours | **< 2 minutes total batch time** |

---

## Operational Recommendations

1. **Review Flagged Fields First**: Operators in the HITL review queue inspect only low-confidence flagged fields rather than re-entering full forms.
2. **Confidence Calibration**: Combining OCR log probabilities with Pydantic regex schema validation corrected the calibration gap, ensuring low-confidence fields trigger review accurately.
3. **Rejection Path**: Corrupt or illegible documents are immediately rejected rather than forcing operators to process invalid files.
