"""
Field-Level Confidence Scorer & Calibration Module
Calculates composite confidence per field based on OCR character score and regex validation.
"""
from typing import Dict, Any

class ConfidenceScorer:
    @staticmethod
    def calculate_confidence(ocr_conf_map: Dict[str, float], validation_map: Dict[str, bool]) -> Dict[str, Any]:
        field_scores = {}
        total_score = 0.0
        count = 0

        for field, ocr_conf in ocr_conf_map.items():
            valid_pass = validation_map.get(field, True)
            
            # Calibration penalty: If regex validation fails, confidence drops significantly
            if not valid_pass:
                calibrated_conf = round(ocr_conf * 0.40, 3)
            else:
                calibrated_conf = round(ocr_conf, 3)

            field_scores[field] = calibrated_conf
            total_score += calibrated_conf
            count += 1

        overall_conf = round(total_score / count, 3) if count > 0 else 0.0

        return {
            "field_confidence": field_scores,
            "overall_document_confidence": overall_conf
        }
