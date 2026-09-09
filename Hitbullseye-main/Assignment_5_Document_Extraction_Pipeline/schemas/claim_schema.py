"""
Pydantic schema definition for Insurance Claim Form Document Extraction
"""
import re
from typing import Dict, Any

class ClaimSchema:
    def __init__(self, data: Dict[str, Any]):
        self.claim_id: str = str(data.get("claim_id", "")).strip()
        self.policy_number: str = str(data.get("policy_number", "")).strip()
        self.claimant_name: str = str(data.get("claimant_name", "")).strip()
        self.incident_date: str = str(data.get("incident_date", "")).strip()
        self.claim_amount: float = float(data.get("claim_amount", 0.0))
        self.diagnosis_code: str = str(data.get("diagnosis_code", "")).strip()
        self.hospital_name: str = str(data.get("hospital_name", "")).strip()

    def validate(self) -> Dict[str, bool]:
        return {
            "claim_id": bool(re.match(r"^CLM-[0-9]{4,8}$", self.claim_id, re.I)),
            "policy_number": bool(re.match(r"^POL-[A-Z0-9]{6,12}$", self.policy_number, re.I)),
            "claimant_name": len(self.claimant_name) >= 2,
            "incident_date": bool(re.match(r"^\d{4}-\d{2}-\d{2}$", self.incident_date)) or bool(re.match(r"^\d{2}/\d{2}/\d{4}$", self.incident_date)),
            "claim_amount": self.claim_amount > 0.0,
            "diagnosis_code": bool(re.match(r"^[A-Z][0-9]{2}(\.[0-9]{1,2})?$", self.diagnosis_code, re.I)), # ICD-10 format
            "hospital_name": len(self.hospital_name) >= 3
        }
