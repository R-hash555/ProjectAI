"""
Structured Document Data Extractor
Extracts structured JSON payload matching target schema from OCR text blocks.
"""
import sys
import os
from typing import Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from schemas.invoice_schema import InvoiceSchema
from schemas.claim_schema import ClaimSchema
from schemas.id_card_schema import IDCardSchema

class DocumentExtractor:
    @staticmethod
    def extract_fields(doc_type: str, ocr_result: Dict[str, Any]) -> Dict[str, Any]:
        blocks = ocr_result.get("extracted_blocks", {})
        if ocr_result.get("is_corrupt", False):
            return {"error": "Corrupt document format"}

        raw_data = {}
        for field, val in blocks.items():
            # Clean OCR artifacts
            clean_val = str(val).rstrip(" #").strip()
            raw_data[field] = clean_val

        # Instantiate schema class to enforce types
        if doc_type == "invoice":
            schema_inst = InvoiceSchema(raw_data)
            extracted = {
                "invoice_no": schema_inst.invoice_no,
                "vendor_name": schema_inst.vendor_name,
                "date": schema_inst.date,
                "tax_amount": schema_inst.tax_amount,
                "total_amount": schema_inst.total_amount,
                "currency": schema_inst.currency,
                "line_items_count": schema_inst.line_items_count
            }
            validation = schema_inst.validate()

        elif doc_type == "claim":
            schema_inst = ClaimSchema(raw_data)
            extracted = {
                "claim_id": schema_inst.claim_id,
                "policy_number": schema_inst.policy_number,
                "claimant_name": schema_inst.claimant_name,
                "incident_date": schema_inst.incident_date,
                "claim_amount": schema_inst.claim_amount,
                "diagnosis_code": schema_inst.diagnosis_code,
                "hospital_name": schema_inst.hospital_name
            }
            validation = schema_inst.validate()

        elif doc_type == "id_card":
            schema_inst = IDCardSchema(raw_data)
            extracted = {
                "id_number": schema_inst.id_number,
                "full_name": schema_inst.full_name,
                "date_of_birth": schema_inst.date_of_birth,
                "issue_date": schema_inst.issue_date,
                "expiry_date": schema_inst.expiry_date,
                "address": schema_inst.address,
                "nationality": schema_inst.nationality
            }
            validation = schema_inst.validate()

        else:
            raise ValueError(f"Unknown document type: {doc_type}")

        return {
            "extracted_fields": extracted,
            "validation_status": validation
        }
