import json
import os
import random

# Fixed seed for 100% deterministic dataset generation
random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "documents")
os.makedirs(DOCS_DIR, exist_ok=True)

dataset = []
ground_truth = {}

first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "Rajesh", "Priya", "Amit", "Sunita", "Vikram", "Ananya"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Sharma", "Verma", "Patel", "Gupta", "Singh", "Kumar", "Iyer"]
vendors = ["Acme Corp", "Global Supplies Ltd", "TechSystems Inc", "Apex Logistics", "Metro Healthcare", "Starlight Media", "Nexus Solutions", "Trident Industries"]
hospitals = ["City General Hospital", "St. Jude Medical Center", "Apollo Speciality Hospital", "Metro Health Institute", "Sunrise Care Clinic"]
icd_codes = ["J06.9", "M54.5", "E11.9", "I10.0", "K21.9", "S82.1", "R07.9", "Z00.0"]

# 1. Generate 35 Invoices
for i in range(1, 36):
    doc_id = f"DOC-INV-{i:03d}"
    quality = random.choice(["digital_clean", "digital_clean", "low_res_scan", "handwritten_field", "noisy_background"])
    if i == 35: quality = "invalid_corrupt"
    
    vendor = random.choice(vendors)
    inv_num = f"INV-2026-{1000 + i}"
    dt = f"2026-0${random.randint(1,9)}-{random.randint(10,28)}" if i < 10 else f"2026-05-{random.randint(10,28)}"
    tax = round(random.uniform(10.0, 150.0), 2)
    total = round(tax + random.uniform(100.0, 1500.0), 2)
    currency = "USD"
    items = random.randint(1, 10)
    
    doc_data = {
        "doc_id": doc_id,
        "doc_type": "invoice",
        "quality_profile": quality,
        "raw_image_path": f"documents/images/{doc_id}.png"
    }
    gt_fields = {
        "invoice_no": inv_num if quality != "invalid_corrupt" else "",
        "vendor_name": vendor if quality != "invalid_corrupt" else "",
        "date": dt if quality != "invalid_corrupt" else "",
        "tax_amount": tax if quality != "invalid_corrupt" else 0.0,
        "total_amount": total if quality != "invalid_corrupt" else 0.0,
        "currency": currency if quality != "invalid_corrupt" else "",
        "line_items_count": items if quality != "invalid_corrupt" else 0
    }
    dataset.append(doc_data)
    ground_truth[doc_id] = gt_fields

# 2. Generate 35 Insurance Claims
for i in range(1, 36):
    doc_id = f"DOC-CLM-{i:03d}"
    quality = random.choice(["digital_clean", "digital_clean", "low_res_scan", "handwritten_field", "noisy_background"])
    if i == 35: quality = "invalid_corrupt"
    
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    claim_id = f"CLM-2026-{5000 + i}"
    policy = f"POL-{random.randint(100000, 999999)}"
    dt = f"2026-04-{random.randint(10,28)}"
    amt = round(random.uniform(250.0, 5000.0), 2)
    diag = random.choice(icd_codes)
    hosp = random.choice(hospitals)
    
    doc_data = {
        "doc_id": doc_id,
        "doc_type": "claim",
        "quality_profile": quality,
        "raw_image_path": f"documents/images/{doc_id}.png"
    }
    gt_fields = {
        "claim_id": claim_id if quality != "invalid_corrupt" else "",
        "policy_number": policy if quality != "invalid_corrupt" else "",
        "claimant_name": name if quality != "invalid_corrupt" else "",
        "incident_date": dt if quality != "invalid_corrupt" else "",
        "claim_amount": amt if quality != "invalid_corrupt" else 0.0,
        "diagnosis_code": diag if quality != "invalid_corrupt" else "",
        "hospital_name": hosp if quality != "invalid_corrupt" else ""
    }
    dataset.append(doc_data)
    ground_truth[doc_id] = gt_fields

# 3. Generate 30 ID Cards
for i in range(1, 31):
    doc_id = f"DOC-IDC-{i:03d}"
    quality = random.choice(["digital_clean", "digital_clean", "low_res_scan", "handwritten_field", "noisy_background"])
    if i == 30: quality = "invalid_corrupt"
    
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    id_num = f"ID-{random.randint(1000000, 9999999)}"
    dob = f"19{random.randint(70,99)}-{random.randint(10,12)}-{random.randint(10,28)}"
    issue = f"2020-01-{random.randint(10,28)}"
    expiry = f"2030-01-{random.randint(10,28)}"
    addr = f"{random.randint(100,999)} Main Street, Suite {random.randint(1,50)}"
    nat = "USA"
    
    doc_data = {
        "doc_id": doc_id,
        "doc_type": "id_card",
        "quality_profile": quality,
        "raw_image_path": f"documents/images/{doc_id}.png"
    }
    gt_fields = {
        "id_number": id_num if quality != "invalid_corrupt" else "",
        "full_name": name if quality != "invalid_corrupt" else "",
        "date_of_birth": dob if quality != "invalid_corrupt" else "",
        "issue_date": issue if quality != "invalid_corrupt" else "",
        "expiry_date": expiry if quality != "invalid_corrupt" else "",
        "address": addr if quality != "invalid_corrupt" else "",
        "nationality": nat if quality != "invalid_corrupt" else ""
    }
    dataset.append(doc_data)
    ground_truth[doc_id] = gt_fields

with open(os.path.join(DOCS_DIR, "dataset.json"), "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2)

with open(os.path.join(BASE_DIR, "ground_truth.json"), "w", encoding="utf-8") as f:
    json.dump(ground_truth, f, indent=2)

print(f"Generated {len(dataset)} documents in dataset.json and ground_truth.json")
