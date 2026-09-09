"""
OCR Engine Simulation & Layout Analyzer
Extracts text blocks and character confidence scores from document images.
"""
import random
from typing import Dict, Any

class OCREngine:
    @staticmethod
    def process_document(doc_meta: Dict[str, Any], ground_truth_fields: Dict[str, Any]) -> Dict[str, Any]:
        """Simulates OCR extraction with quality degradation profiles."""
        quality = doc_meta.get("quality_profile", "digital_clean")
        extracted_text_blocks = {}
        confidence_map = {}

        if quality == "invalid_corrupt":
            return {
                "raw_text": "CORRUPTED FILE DATA",
                "extracted_blocks": {},
                "field_confidence": {k: 0.05 for k in ground_truth_fields.keys()},
                "is_corrupt": True
            }

        for field, true_val in ground_truth_fields.items():
            str_val = str(true_val)

            if quality == "digital_clean":
                extracted_val = str_val
                conf = round(random.uniform(0.95, 0.99), 3)
            elif quality == "low_res_scan":
                # Occasional OCR character error (e.g. O -> 0, I -> 1)
                if random.random() < 0.2 and len(str_val) > 3:
                    extracted_val = str_val.replace("O", "0").replace("I", "1")
                else:
                    extracted_val = str_val
                conf = round(random.uniform(0.80, 0.92), 3)
            elif quality == "handwritten_field":
                # Handwritten fields have higher character error rate
                if field in ["diagnosis_code", "hospital_name", "vendor_name", "address"]:
                    if random.random() < 0.4:
                        extracted_val = str_val[:-1] + "?" if len(str_val) > 2 else str_val
                        conf = round(random.uniform(0.55, 0.72), 3)
                    else:
                        extracted_val = str_val
                        conf = round(random.uniform(0.70, 0.85), 3)
                else:
                    extracted_val = str_val
                    conf = round(random.uniform(0.85, 0.95), 3)
            elif quality == "noisy_background":
                if random.random() < 0.25:
                    extracted_val = str_val + " #"
                else:
                    extracted_val = str_val
                conf = round(random.uniform(0.75, 0.88), 3)
            else:
                extracted_val = str_val
                conf = 0.90

            extracted_text_blocks[field] = extracted_val
            confidence_map[field] = conf

        return {
            "raw_text": f"Document ID {doc_meta['doc_id']} processed.",
            "extracted_blocks": extracted_text_blocks,
            "field_confidence": confidence_map,
            "is_corrupt": False
        }
