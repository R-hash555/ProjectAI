"""
Pydantic schema definition for Invoice Document Extraction
"""
import re
from typing import Optional, List, Dict, Any

class InvoiceSchema:
    def __init__(self, data: Dict[str, Any]):
        self.invoice_no: str = str(data.get("invoice_no", "")).strip()
        self.vendor_name: str = str(data.get("vendor_name", "")).strip()
        self.date: str = str(data.get("date", "")).strip()
        self.tax_amount: float = float(data.get("tax_amount", 0.0))
        self.total_amount: float = float(data.get("total_amount", 0.0))
        self.currency: str = str(data.get("currency", "USD")).strip()
        self.line_items_count: int = int(data.get("line_items_count", 0))

    def validate(self) -> Dict[str, bool]:
        """Returns validation status per field."""
        return {
            "invoice_no": bool(re.match(r"^[A-Z0-9\-\/]{3,20}$", self.invoice_no, re.I)),
            "vendor_name": len(self.vendor_name) >= 2,
            "date": bool(re.match(r"^\d{4}-\d{2}-\d{2}$", self.date)) or bool(re.match(r"^\d{2}/\d{2}/\d{4}$", self.date)),
            "tax_amount": self.tax_amount >= 0.0,
            "total_amount": self.total_amount > 0.0 and self.total_amount >= self.tax_amount,
            "currency": len(self.currency) == 3,
            "line_items_count": self.line_items_count >= 1
        }
