import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="Texture Extractor", layout="wide")
st.title("👕 AI Sportswear Texture Extractor")

file = st.file_uploader("Upload Pic 1 (Mockup)", type=["jpg", "png", "jpeg"])

if file:
    # Image loading
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    with st.spinner('Extracting Flat Design...'):
        # 1. Background Masking (Shirt isolate karna)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY_INV)
        
        # 2. Extracting only the design pattern
        # Ye shadows hatayega taake design flat dikhe
        design_only = cv2.bitwise_and(img, img, mask=mask)
        design_rgb = cv2.cvtColor(design_only, cv2.COLOR_BGR2RGB)
        
        # 3. GUI Layout
        col1, col2 = st.columns(2)
        with col1:
            st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Pic 1: Original")
        with col2:
            st.image(design_rgb, caption="Pic 2: Flat Texture Result")

        # 4. Download
        final_img = Image.fromarray(design_rgb)
        buf = io.BytesIO()
        final_img.save(buf, format="PNG")
        
        st.divider()
        st.download_button("📥 Download Flat Texture (PNG)", buf.getvalue(), "flat_design.png", "image/png")
