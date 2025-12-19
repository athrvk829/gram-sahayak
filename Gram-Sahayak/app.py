import streamlit as st
import os
import time
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# --- FIX 1: Import Logic ---
import logic 
# --------------------------------------

# Try importing the Azure module
try:
    import azure_vision 
except ImportError:
    azure_vision = None

# 1. SETUP & CONFIGURATION
st.set_page_config(page_title="Gram-Sahayak", page_icon="🚜", layout="wide")
load_dotenv() 

# Initialize Session State
if 'farmer_name' not in st.session_state:
    st.session_state['farmer_name'] = ""
if 'land_area' not in st.session_state:
    st.session_state['land_area'] = ""
if 'loan_amount' not in st.session_state:
    st.session_state['loan_amount'] = ""

# 2. HELPER FUNCTIONS
def generate_pdf(name, area, amount):
    """Creates a simple PDF application form in memory"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 750, "GRAM-SAHAYAK: Loan Application")
    c.line(100, 740, 500, 740)
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Date: {time.strftime('%d/%m/%Y')}")
    c.drawString(100, 670, f"Applicant Name: {name}")
    c.drawString(100, 650, f"Land Area (7/12): {area} Guntha")
    c.drawString(100, 630, f"Requested Loan Amount: ₹ {amount}")
    c.drawString(100, 580, "Declaration:")
    c.drawString(100, 565, "I hereby declare that the information provided is true.")
    c.line(100, 500, 300, 500)
    c.drawString(100, 485, "Farmer Signature")
    c.save()
    buffer.seek(0)
    return buffer

# 3. SIDEBAR (CONTROLS)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
st.sidebar.title("🚜 Gram-Sahayak")
st.sidebar.markdown("---")
mode = st.sidebar.radio("App Mode:", ["🟢 Demo (Simulation)", "🔴 Live (Azure AI)"])
st.sidebar.info("Use 'Demo' if API keys are missing or internet is slow.")

# 4. MAIN APP INTERFACE
st.title("🌾 Smart Farmer Assistant")
st.markdown("Automating Farm Loans using **Voice** and **Vision**.")

# --- SECTION 1: VOICE INPUT ---
st.header("1️⃣  Speak Your Request")
col1, col2 = st.columns([1, 2])

with col1:
    if st.button("🎤 Tap to Speak"):
        with st.spinner("Listening..."):
            time.sleep(2) 
            if mode == "🟢 Demo (Simulation)":
                recognized_text = "Mala tractor sathi 5 lakh loan hava ahe. Maze nav Atharva ahe."
                st.success("✅ Voice Recognized!")
            else:
                recognized_text = "Live Speech Not Connected (Check Keys)"
                st.warning("⚠️ Live Speech requires Azure Key setup.")
            
            st.code(f"🗣️ You said: '{recognized_text}'")
            if "Atharva" in recognized_text:
                st.session_state['farmer_name'] = "Atharva Kassa"
            if "5 lakh" in recognized_text:
                st.session_state['loan_amount'] = "5,00,000"

with col2:
    st.text_input("📝 Farmer Name (Auto-filled)", value=st.session_state['farmer_name'])
    st.text_input("💰 Loan Amount (Auto-filled)", value=st.session_state['loan_amount'])

st.markdown("---")

# --- SECTION 2: DOCUMENT SCANNING (INTEGRATED) ---
st.header("2️⃣  Upload 7/12 Extract")
uploaded_file = st.file_uploader("Upload Image of 7/12 Document", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Scanned Document", width=300)
    
    if st.button("🔍 Analyze Document"):
        
        # --- PATH A: DEMO MODE ---
        if mode == "🟢 Demo (Simulation)":
            with st.spinner("Analyzing Land Records..."):
                time.sleep(2) 
                st.session_state['land_area'] = "45"
                st.success("✅ Land Verified: 45 Guntha")
                st.json({
                    "Owner": "Atharva Kassa",
                    "Survey No": "142/B",
                    "Land Type": "Irrigated",
                    "Area": "45 Guntha"
                })

        # --- PATH B: LIVE AZURE MODE ---
        else:
            if azure_vision is None:
                st.error("❌ azure_vision.py file is missing! Please create it to use Live Mode.")
            else:
                with st.spinner("Connecting to Azure Computer Vision..."):
                    raw_text = azure_vision.get_text_from_image(uploaded_file)
                    if "Error" in raw_text:
                        st.error(raw_text)
                    else:
                        st.success("✅ Azure Scan Successful!")
                        with st.expander("See Raw Extracted Text"):
                            st.text(raw_text)
                        
                        st.info("Parsing Data...")
                        import re
                        match = re.search(r"(\d+\.\d+)\s*(Hectare|R|Guntha)", raw_text, re.IGNORECASE)
                        if match:
                            found_area = match.group(1)
                            st.session_state['land_area'] = found_area
                            st.success(f"✅ Extracted Land Area: {found_area} units")
                        else:
                            st.warning("Could not automatically find 'Land Area' in text. Please enter manually.")

    # --- FIX 2: MOVED LOGIC CHECK OUTSIDE THE IF/ELSE BLOCK ---
    st.markdown("---")
    st.header("2️⃣.5️⃣  Check Scheme Eligibility")
    
    # We create a button so the user can choose when to run the logic
    if st.button("🧠 Check Eligibility with Logic.py"):
        st.info("Analyzing Profile...")
        
        # Create a profile using whatever data we have (Demo or Live)
        current_profile = {
            "name": st.session_state.get('farmer_name', 'Unknown'),
            "occupation": "Farmer", 
            "land_holding": float(st.session_state.get('land_area', 0)) if st.session_state.get('land_area') else 0.0,
            "income": 120000, 
            "residence": "Maharashtra"
        }

        # CALL THE FUNCTION FROM logic.py
        eligible_schemes = logic.check_eligibility(current_profile)

        if eligible_schemes:
            st.success(f"🎉 You are eligible for {len(eligible_schemes)} Schemes!")
            for scheme in eligible_schemes:
                with st.expander(f"✅ {scheme['name']}"):
                    st.write(f"**Benefit:** {scheme['benefit']}")
                    st.write(f"**Link:** {scheme['link']}")
        else:
            st.warning("No schemes found for this profile.")
    # ----------------------------------------------------------

st.markdown("---")

# --- SECTION 3: GENERATE APPLICATION ---
st.header("3️⃣  Final Step")

if st.session_state['farmer_name']:
    st.success("Ready to generate form.")
    
    if st.button("📄 Generate Loan Application PDF"):
        pdf_file = generate_pdf(
            st.session_state['farmer_name'],
            st.session_state['land_area'] if st.session_state['land_area'] else "N/A",
            st.session_state['loan_amount']
        )
        
        st.balloons()
        st.download_button(
            label="⬇️ Download Official Application",
            data=pdf_file,
            file_name="Gram_Sahayak_Application.pdf",
            mime="application/pdf"
        )
else:
    st.info("Please provide Farmer Name to generate the application.")