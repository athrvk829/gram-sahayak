import streamlit as st
import os
import time
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# 1. SETUP & CONFIGURATION
# ------------------------
st.set_page_config(page_title="Gram-Sahayak", page_icon="🚜", layout="wide")
load_dotenv()  # Loads keys from .env file

# API Keys (Safely loaded)
VISION_KEY = os.getenv("VISION_KEY")
VISION_ENDPOINT = os.getenv("VISION_ENDPOINT")

# Initialize Session State (To remember data between clicks)
if 'farmer_name' not in st.session_state:
    st.session_state['farmer_name'] = ""
if 'land_area' not in st.session_state:
    st.session_state['land_area'] = ""
if 'loan_amount' not in st.session_state:
    st.session_state['loan_amount'] = ""

# 2. HELPER FUNCTIONS
# -------------------
def generate_pdf(name, area, amount):
    """Creates a simple PDF application form in memory"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 750, "GRAM-SAHAYAK: Loan Application")
    c.line(100, 740, 500, 740)
    
    # Content
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Date: {time.strftime('%d/%m/%Y')}")
    c.drawString(100, 670, f"Applicant Name: {name}")
    c.drawString(100, 650, f"Land Area (7/12): {area} Guntha")
    c.drawString(100, 630, f"Requested Loan Amount: ₹ {amount}")
    
    c.drawString(100, 580, "Declaration:")
    c.drawString(100, 565, "I hereby declare that the information provided is true.")
    
    # Signature Placeholder
    c.line(100, 500, 300, 500)
    c.drawString(100, 485, "Farmer Signature")
    
    c.save()
    buffer.seek(0)
    return buffer

# 3. SIDEBAR (CONTROLS)
# ---------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
st.sidebar.title("🚜 Gram-Sahayak")
st.sidebar.markdown("---")
mode = st.sidebar.radio("App Mode:", ["🟢 Demo (Simulation)", "🔴 Live (Azure AI)"])
st.sidebar.info("Use 'Demo' if API keys are missing or internet is slow.")

# 4. MAIN APP INTERFACE
# ---------------------
st.title("🌾 Smart Farmer Assistant")
st.markdown("Automating Farm Loans using **Voice** and **Vision**.")

# --- SECTION 1: VOICE INPUT ---
st.header("1️⃣  Speak Your Request")
col1, col2 = st.columns([1, 2])

with col1:
    if st.button("🎤 Tap to Speak"):
        with st.spinner("Listening..."):
            time.sleep(2)  # Simulate processing time
            
            if mode == "🟢 Demo (Simulation)":
                recognized_text = "Mala tractor sathi 5 lakh loan hava ahe. Maze nav Atharva ahe."
                st.success("✅ Voice Recognized!")
            else:
                # PLACEHOLDER: Insert Real Azure Speech Code Here
                recognized_text = "Live Speech Not Connected (Check Keys)"
                st.warning("⚠️ Live Speech requires Azure Key setup.")
            
            st.code(f"🗣️ You said: '{recognized_text}'")
            
            # Simple keyword extraction (Mock Logic)
            if "Atharva" in recognized_text:
                st.session_state['farmer_name'] = "Atharva Kassa"
            if "5 lakh" in recognized_text:
                st.session_state['loan_amount'] = "5,00,000"

with col2:
    st.text_input("📝 Farmer Name (Auto-filled)", value=st.session_state['farmer_name'])
    st.text_input("💰 Loan Amount (Auto-filled)", value=st.session_state['loan_amount'])

st.markdown("---")

# --- SECTION 2: DOCUMENT SCANNING ---
st.header("2️⃣  Upload 7/12 Extract")
uploaded_file = st.file_uploader("Upload Image of 7/12 Document", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Scanned Document", width=300)
    
    if st.button("🔍 Analyze Document"):
        with st.spinner("Analyzing Land Records..."):
            time.sleep(2) # UI effect
            
            if mode == "🟢 Demo (Simulation)":
                st.session_state['land_area'] = "45"
                st.success("✅ Land Verified: 45 Guntha")
                st.json({
                    "Owner": "Atharva Kassa",
                    "Survey No": "142/B",
                    "Land Type": "Irrigated",
                    "Area": "45 Guntha"
                })
            else:
                st.error("⚠️ Connect Azure Computer Vision Key to use Live Mode.")

st.markdown("---")

# --- SECTION 3: GENERATE APPLICATION ---
st.header("3️⃣  Final Step")

if st.session_state['farmer_name'] and st.session_state['land_area']:
    st.success("All details collected. Ready to generate form.")
    
    if st.button("📄 Generate Loan Application PDF"):
        pdf_file = generate_pdf(
            st.session_state['farmer_name'],
            st.session_state['land_area'],
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
    st.info("Complete Step 1 and Step 2 to unlock the Application Form.")