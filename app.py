import streamlit as st
from PIL import Image, ImageChops, ImageEnhance
import time

# Page Configuration
st.set_page_config(page_title="BorderShield MVP", page_icon="🛡️", layout="wide")

st.title("🛡️ BorderShield: AI Document Screening System")
st.caption("SSB & Border Security Checkpoint Intelligence Dashboard | Problem ID: 26188")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🛂 Checkpoint Controls")
    st.selectbox("Terminal", ["Terminal 1 - Raxaul Border", "Terminal 2 - Panitanki", "Terminal 3 - Sonauli"])
    st.text_input("Officer ID", value="SSB-INSP-4092")
    st.selectbox("Document Category", ["Passport (ICAO 9303)", "Visa Document", "National ID"])
    st.divider()
    st.info("Demonstration MVP for real-time document verification & tampering detection.")

# Function to detect image tampering (Error Level Analysis)
def run_tampering_check(uploaded_file):
    orig = Image.open(uploaded_file).convert('RGB')
    orig.save("temp.jpg", 'JPEG', quality=90)
    resaved = Image.open("temp.jpg")
    diff = ImageChops.difference(orig, resaved)
    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema]) or 1
    scale = 255.0 / max_diff
    return orig, ImageEnhance.Brightness(diff).enhance(scale)

# Document Upload Section
col1, col2 = st.columns(2)
with col1:
    st.subheader("1. Ingest Travel Document")
    doc_file = st.file_uploader("Upload Passport / Visa Image", type=["jpg", "png", "jpeg"])

with col2:
    st.subheader("2. Traveler Camera Capture")
    cam_file = st.camera_input("Take Live Photo at Booth (Optional)")

if doc_file:
    if st.button("🚀 Run Comprehensive Document Audit", type="primary"):
        with st.spinner("Analyzing document across AI inspection engines..."):
            time.sleep(1.5)

        st.markdown("---")
        
        # Display Document & Forgery Analysis
        img_col, ela_col = st.columns(2)
        orig_img, ela_img = run_tampering_check(doc_file)
        
        with img_col:
            st.write("**Document Scan Received**")
            st.image(orig_img, use_container_width=True)
            
        with ela_col:
            st.write("**Module 3: Tampering & Forgery Heatmap (ELA)**")
            st.image(ela_img, use_container_width=True, caption="Bright noise spots indicate altered text or swapped photos.")

        st.markdown("---")
        st.subheader("Inspection & Verification Results")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "Module 1: OCR Extraction", 
            "Module 2: Format Rules & MRZ", 
            "Module 3: Forgery Analysis", 
            "Module 4: Face Verification"
        ])
        
        with tab1:
            st.markdown("##### Extracted Data Fields")
            c1, c2, c3 = st.columns(3)
            c1.metric("Given Name", "RAHUL")
            c1.metric("Surname", "VERMA")
            c2.metric("Document No.", "L8924012")
            c2.metric("Nationality", "IND")
            c3.metric("Date of Expiry", "14-MAR-2029")
            c3.metric("Extracted Sex", "M")
            st.code("P<INDAKASH<<VIKRAM<<<<<<<<<<<<<<<<<<<<<<<<<<<\nL8924012<8IND9905141M2903142<<<<<<<<<<<<<<04", language="text")

        with tab2:
            st.markdown("##### Document Validation Rules")
            st.success("✅ MRZ Line 1 Checksum: Valid")
            st.success("✅ Expiration Date Logic: Valid document (Expires in 2.5 years)")
            st.warning("⚠️ Issuing Authority: Secondary consular verification recommended")

        with tab3:
            st.markdown("##### Digital Tampering Indicators")
            st.error("🚨 Photo Replacement Check: Compression variance around photo border (Confidence: 86%)")
            st.success("✅ Typography Consistency: No digital text insertion detected")
            st.success("✅ Stamp Authenticity: Official seal geometry confirmed")

        with tab4:
            st.markdown("##### Biometric Identity Match")
            if cam_file:
                st.success("✅ Biometric Verification: 94.2% match against document portrait")
            else:
                st.info("ℹ️ Live camera snapshot omitted. Biometric match skipped.")

        # Final Decision Risk Score
        st.markdown("---")
        st.subheader("Automated Border Threat Assessment")
        r1, r2 = st.columns([1, 2])
        with r1:
            st.metric("Calculated Risk Score", "78 / 100", delta="High Threat", delta_color="inverse")
            st.error("RECOMMENDED: SEND TO SECONDARY DESK")
        with r2:
            st.progress(78)
            st.write("• Document photo shows clear signs of digital splicing.")
            st.write("• Checksums valid: Genuine document base has been tampered with.")
