import pandas as pd
import numpy as np

# Define codes
icd_codes = {
    "I10": "Essential (primary) hypertension",
    "E11": "Type 2 diabetes mellitus",
    "J45": "Asthma",
    "M54": "Dorsalgia (back pain)",
    "F32": "Major depressive disorder",
    "K21": "Gastro-esophageal reflux disease",
    "N39": "Urinary tract infection",
    "R51": "Headache",
    "M25": "Joint pain",
    "L03": "Cellulitis"
}

cpt_codes = {
    "99213": "Office visit (established patient)",
    "93000": "Electrocardiogram",
    "80050": "General health panel",
    "85025": "Complete blood count",
    "71020": "Chest X-ray",
    "90791": "Psychiatric diagnostic evaluation",
    "36415": "Blood draw",
    "11720": "Nail debridement",
    "12001": "Simple wound repair",
    "99173": "Visual acuity screening"
}


n = 108475
ehr = pd.DataFrame({
    "Patient_ID": [f"P{1000+i}" for i in range(n)],
    "Name": [f"Patient_{i}" for i in range(n)],
    "DOB": pd.to_datetime(np.random.choice(pd.date_range("1950-01-01", "2005-12-31"), n)),
    "Gender": np.random.choice(["Male", "Female", "Other"], n),
    "Admission_Date": pd.to_datetime(np.random.choice(pd.date_range("2023-01-01", "2025-01-01"), n)),
    "Length_of_Stay": np.random.randint(1, 15, size=n),
    "Provider": np.random.choice(["Dr. Smith", "Dr. Lee", "Dr. Gomez", "Dr. Patel"], n),
    "Diagnosis_Code": np.random.choice(list(icd_codes.keys()), n),
    "Procedure_Code": np.random.choice(list(cpt_codes.keys()), n),
    "Notes": np.random.choice(["Stable", "Follow-up needed", "Critical", "Monitor closely"], n)
})
ehr["Discharge_Date"] = ehr["Admission_Date"] + pd.to_timedelta(ehr["Length_of_Stay"], unit="D")
ehr["Diagnosis_Description"] = ehr["Diagnosis_Code"].map(icd_codes)
ehr["Procedure_Description"] = ehr["Procedure_Code"].map(cpt_codes)
ehr.to_csv("ehr_data_large.csv", index=False)

claims = pd.DataFrame({
    "Claim_ID": [f"C{2000+i}" for i in range(n)],
    "Patient_ID": ehr["Patient_ID"],
    "Service_Date": ehr["Admission_Date"],
    "ICD_Code": ehr["Diagnosis_Code"],
    "CPT_Code": ehr["Procedure_Code"],
    "Billed_Amount": np.random.randint(200, 3000, n),
    "Paid_Amount": [np.random.randint(0, b) for b in np.random.randint(200, 3000, n)],
    "Status": np.random.choice(["Paid", "Pending", "Denied"], n)
})
claims.to_csv("claims_data_large.csv", index=False)
