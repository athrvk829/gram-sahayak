# test_logic.py
from logic import check_eligibility, parse_ocr_text

# --- TEST CASE 1: Manual Profile (Sita) ---
print("--- TEST 1: Manual Input (Sita) ---")
sita_profile = {
    "name": "Sita Devi",
    "gender": "Female",
    "age": 25,
    "income": 150000,
    "occupation": "Tailor",
    "residence": "Maharashtra"
}

results = check_eligibility(sita_profile)
print(f"User: {sita_profile['name']}")
print(f"Eligible for {len(results)} schemes:")
for s in results:
    print(f"✅ {s['name']}")
print("\n")


# --- TEST CASE 2: Azure AI Simulation (Ramesh) ---
print("--- TEST 2: AI Scanned Document ---")
# Simulate messy text that Member 1's AI might find on a document
fake_ocr_text = """
GOVERNMENT OF MAHARASHTRA
7/12 EXTRACT
Name: Ramesh Patil
Age: 42 years
Income Certificate: Rs. 1,80,000
Land Holding: 1.2 Hectare
"""

# Step 1: Clean the text
extracted_data = parse_ocr_text(fake_ocr_text)
print(f"AI Extracted Data: {extracted_data}")

# Step 2: Check Eligibility
ocr_results = check_eligibility(extracted_data)
print(f"Eligible for {len(ocr_results)} schemes:")
for s in ocr_results:
    print(f"✅ {s['name']}")