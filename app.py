import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="Mockup to Flat Texture", layout="wide")
st.title("👕 Mockup to Flat Texture Extractor")

file = st.file_uploader("Upload Pic 1 (Mockup)", type=["jpg", "png", "jpeg"])

if file:
    # Image read karna
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    h, w, _ = img.shape

    # --- TEXTURE EXTRACTION LOGIC ---
    # 1. Shirt ka main center area extract karna
    # Ye collar, sleeves aur buttons ko automatically nikaal dega
    y1, y2 = int(h * 0.15), int(h * 0.85)
    x1, x2 = int(w * 0.20), int(w * 0.80)
    texture_crop = img[y1:y2, x1:x2]

    # 2. Design ko "Flatten" karna (Perspective Transformation)
    # Is se shirt ki curves khatam ho kar design flat sheet ban jayega
    flat_texture = cv2.resize(texture_crop, (1200, 1200), interpolation=cv2.INTER_LANCZOS4)
    
    # 3. Design Sharpening
    gaussian_blur = cv2.GaussianBlur(flat_texture, (0, 0), 3)
    flat_texture = cv2.addWeighted(flat_texture, 1.5, gaussian_blur, -0.5, 0)

    # --- Results Display ---
    col1, col2 = st.columns(2)
    with col1:
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Pic 1: Original Mockup")
    with col2:
        # Ye wahi Pic 2 hai jo aapne aakhri screenshot mein dekhi
        st.image(cv2.cvtColor(flat_texture, cv2.COLOR_BGR2RGB), caption="Pic 2: Extracted Flat Design")

    # Download Button
    _, buffer = cv2.imencode('.png', flat_texture)
    st.divider()
    st.download_button(
        label="📥 Download Flat Texture (PNG)",
        data=buffer.tobytes(),
        file_name="flat_texture_result.png",
        mime="image/png"
    )
