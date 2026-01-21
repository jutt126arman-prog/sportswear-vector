import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Page Config
st.set_page_config(page_title="Design Extractor", layout="wide")
st.title("👕 AI Sportswear Texture Extractor")

# File Uploader
file = st.file_uploader("Upload Pic 1 (Mockup)", type=["jpg", "png", "jpeg"])

if file:
    # Image loading
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    h, w, _ = img.shape

    # --- TEXTURE EXTRACTION LOGIC ---
    # Shirt ke main body area ko capture karna (Sleeves aur collar ignore karke)
    # Ye shirt ke design ko extract karke flat kar deta hai
    roi = img[int(h*0.15):int(h*0.85), int(w*0.2):int(w*0.8)]
    
    # Texture ko Pic 2 ki tarah square aur flat banana
    flat_texture = cv2.resize(roi, (1000, 1000), interpolation=cv2.INTER_LANCZOS4)
    
    # Display Results
    col1, col2 = st.columns(2)
    with col1:
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Pic 1: Original Mockup", use_container_width=True)
    with col2:
        st.image(cv2.cvtColor(flat_texture, cv2.COLOR_BGR2RGB), caption="Pic 2: Extracted Flat Texture", use_container_width=True)

    # Download Button
    _, buffer = cv2.imencode('.png', flat_texture)
    st.divider()
    st.download_button(
        label="📥 Download Flat Texture (PNG)",
        data=buffer.tobytes(),
        file_name="flat_design_texture.png",
        mime="image/png"
    )
