"""
Human-in-the-Loop Routing Engine & Rejection Logic
"""
from typing import Dict, Any

class DocumentRouter:
    AUTO_ACCEPT_THRESHOLD = 0.85
    MIN_FIELD_THRESHOLD = 0.78
    REJECT_THRESHOLD = 0.50

    @classmethod
    def route_document(cls, extraction_res: Dict[str, Any], conf_res: Dict[str, Any], is_corrupt: bool = False) -> Dict[str, Any]:
        if is_corrupt or "error" in extraction_res:
            return {
                "route": "REJECTED",
                "reason": "Corrupt document format or unreadable OCR stream",
                "requires_human_review": False
            }

        overall_conf = conf_res.get("overall_document_confidence", 0.0)
        field_confs = conf_res.get("field_confidence", {})

        min_field_conf = min(field_confs.values()) if field_confs else 0.0

        if overall_conf >= cls.AUTO_ACCEPT_THRESHOLD and min_field_conf >= cls.MIN_FIELD_THRESHOLD:
            return {
                "route": "AUTO_ACCEPTED",
                "reason": f"Overall confidence ({overall_conf}) and min field confidence ({min_field_conf}) meet criteria.",
                "requires_human_review": False
            }

        elif overall_conf >= cls.REJECT_THRESHOLD:
            low_fields = [f for f, c in field_confs.items() if c < cls.MIN_FIELD_THRESHOLD]
            return {
                "route": "HUMAN_REVIEW_QUEUE",
                "reason": f"Low confidence detected on fields: {low_fields} (Overall: {overall_conf}).",
                "requires_human_review": True,
                "flagged_fields": low_fields
            }

        else:
            return {
                "route": "REJECTED",
                "reason": f"Document confidence ({overall_conf}) below rejection threshold ({cls.REJECT_THRESHOLD}).",
                "requires_human_review": False
            }
