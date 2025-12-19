# schemes_data.py
# ---------------------------------------------------------
# DATABASE OF MAHARASHTRA & CENTRAL GOV SCHEMES
# ---------------------------------------------------------

SCHEMES_DB = [
    {
        "id": "majhi_ladki_bahin",
        "name": "Mukhyamantri Majhi Ladki Bahin Yojana",
        "category": "Women Welfare",
        "benefit": "₹1,500 per month direct transfer",
        "link": "https://ladkibahin.maharashtra.gov.in/",
        "rules": {
            "gender": "Female",
            "min_age": 21,
            "max_age": 65,
            "max_income": 250000,
            "residence": "Maharashtra"
        }
    },
    {
        "id": "pm_kisan",
        "name": "PM Kisan Samman Nidhi",
        "category": "Agriculture",
        "benefit": "₹6,000/year for landholding farmers",
        "link": "https://pmkisan.gov.in/",
        "rules": {
            "occupation": ["Farmer"],
            "max_land_holding": 2.0,  # Max 2 Hectares
            "max_income": 2000000     # High limit for small farmers
        }
    },
    {
        "id": "caste_validity",
        "name": "Caste Validity Certificate (BARTI)",
        "category": "Documents",
        "benefit": "Official verification for Education/Jobs",
        "link": "https://barti.maharashtra.gov.in/",
        "rules": {
            "caste_category": ["SC", "ST", "OBC", "VJNT", "SBC"]
        }
    },
    {
        "id": "sanjay_gandhi_pension",
        "name": "Sanjay Gandhi Niradhar Yojana",
        "category": "Pension",
        "benefit": "₹1,000/month for destitute persons",
        "link": "https://sjsa.maharashtra.gov.in/",
        "rules": {
            "max_income": 21000,
            "special_status": ["Widow", "Disabled", "Orphan", "Senior Citizen"]
        }
    },
    {
        "id": "pik_vima",
        "name": "Pradhan Mantri Fasal Bima Yojana (Pik Vima)",
        "category": "Insurance",
        "benefit": "Crop loss coverage due to natural calamity",
        "link": "https://pmfby.gov.in/",
        "rules": {
            "occupation": ["Farmer"],
            "has_crop_insurance": False # Helps if they don't have it yet
        }
    }
]