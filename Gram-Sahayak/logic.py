# logic.py
import re
from schemes_data import SCHEMES_DB

def check_eligibility(user_profile):
    """
    Input: Dictionary containing user details (age, income, gender, etc.)
    Output: List of schemes they qualify for.
    """
    eligible_schemes = []
    
    # 1. Loop through every scheme in our database
    for scheme in SCHEMES_DB:
        rules = scheme["rules"]
        is_eligible = True
        
        # --- RULE ENGINE ---
        
        # Check Gender
        if "gender" in rules and user_profile.get("gender") != rules["gender"]:
            is_eligible = False
            
        # Check Age Limits
        user_age = user_profile.get("age", 30) # Default to 30 if unknown
        if "min_age" in rules and user_age < rules["min_age"]:
            is_eligible = False
        if "max_age" in rules and user_age > rules["max_age"]:
            is_eligible = False
            
        # Check Income Cap
        if "max_income" in rules and user_profile.get("income", 0) > rules["max_income"]:
            is_eligible = False
            
        # Check Occupation
        if "occupation" in rules and user_profile.get("occupation") not in rules["occupation"]:
            is_eligible = False

        # Check Caste Category
        if "caste_category" in rules:
            if user_profile.get("caste") not in rules["caste_category"]:
                is_eligible = False

        # Check Special Status (Widow/Disabled)
        if "special_status" in rules:
            # Check if user's status matches ANY of the allowed statuses
            if user_profile.get("special_status") not in rules["special_status"]:
                is_eligible = False

        # --- FINAL VERDICT ---
        if is_eligible:
            eligible_schemes.append(scheme)
            
    return eligible_schemes


def parse_ocr_text(raw_text):
    """
    Input: Messy text string from Azure Vision AI.
    Output: Clean dictionary of extracted data.
    """
    data = {}
    
    # Regex to find Age (e.g., "Age: 45" or "45 years")
    age_match = re.search(r"(\d{2})\s?(years|yrs|age)", raw_text, re.IGNORECASE)
    if age_match:
        data["age"] = int(age_match.group(1))
        
    # Regex to find Income (e.g., "Income 50000" or "Rs. 1,00,000")
    # Looks for digits following 'Income' or 'Rs'
    income_match = re.search(r"(Income|Rs\.?|Salary)[:\-\s]+([\d,]+)", raw_text, re.IGNORECASE)
    if income_match:
        clean_income = income_match.group(2).replace(",", "")
        data["income"] = int(clean_income)
        
    # Regex to find Gender
    if re.search(r"\b(Female|Woman|Mrs|Smt)\b", raw_text, re.IGNORECASE):
        data["gender"] = "Female"
    elif re.search(r"\b(Male|Man|Mr)\b", raw_text, re.IGNORECASE):
        data["gender"] = "Male"
        
    # Regex to detect Land (e.g., "2.4 Ha" or "Hectare")
    if re.search(r"Hectare|Ha|7\/12", raw_text, re.IGNORECASE):
        data["occupation"] = "Farmer"
        
    return data