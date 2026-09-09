"""
Pydantic schema definition for Identity Card Document Extraction
"""
import re
from typing import Dict, Any

class IDCardSchema:
    def __init__(self, data: Dict[str, Any]):
        self.id_number: str = str(data.get("id_number", "")).strip()
        self.full_name: str = str(data.get("full_name", "")).strip()
        self.date_of_birth: str = str(data.get("date_of_birth", "")).strip()
        self.issue_date: str = str(data.get("issue_date", "")).strip()
        self.expiry_date: str = str(data.get("expiry_date", "")).strip()
        self.address: str = str(data.get("address", "")).strip()
        self.nationality: str = str(data.get("nationality", "")).strip()

    def validate(self) -> Dict[str, bool]:
        return {
            "id_number": len(self.id_number) >= 5,
            "full_name": len(self.full_name) >= 3,
            "date_of_birth": bool(re.match(r"^\d{4}-\d{2}-\d{2}$", self.date_of_birth)) or bool(re.match(r"^\d{2}/\d{2}/\d{4}$", self.date_of_birth)),
            "issue_date": bool(re.match(r"^\d{4}-\d{2}-\d{2}$", self.issue_date)) or bool(re.match(r"^\d{2}/\d{2}/\d{4}$", self.issue_date)),
            "expiry_date": bool(re.match(r"^\d{4}-\d{2}-\d{2}$", self.expiry_date)) or bool(re.match(r"^\d{2}/\d{2}/\d{4}$", self.expiry_date)),
            "address": len(self.address) >= 5,
            "nationality": len(self.nationality) >= 2
        }
