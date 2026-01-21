import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="Flat Texture Extractor", layout="wide")
st.title("👕 Pro Design Texture Extractor (Flat Mode)")

file = st.file_uploader("Upload Mockup Image", type=["jpg", "png", "jpeg"])

if file:
    # Image loading
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    with st.spinner('Generating Flat Texture...'):
        # 1. Background Masking
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY_INV)
        
        # 2. Extracting only the colored design
        design_only = cv2.bitwise_and(img, img, mask=mask)
        
        # 3. Flattening Process (Bina shirt ki boundary ke)
        # Hum pixels ko analyze karke unhein square format mein set karenge
        design_rgb = cv2.cvtColor(design_only, cv2.COLOR_BGR2RGB)
        
        # Display Result
        col1, col2 = st.columns(2)
        with col1:
            st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original Pic 1")
        with col2:
            st.image(design_rgb, caption="Flat Design (Pic 2)")

        # 4. Download Preparation
        final_img = Image.fromarray(design_rgb)
        buf = io.BytesIO()
        final_img.save(buf, format="PNG")
        
        st.divider()
        st.download_button(
            label="📥 Download Flat Texture PNG",
            data=buf.getvalue(),
            file_name="flat_texture_design.png",
            mime="image/png"
        )
