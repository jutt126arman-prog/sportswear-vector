import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="Flat Design Extractor", layout="wide")
st.title("👕 Mockup to Flat Texture Extractor")
st.write("Ye app shirt ki shape khatam karke andar ka poora design flat nikal degi.")

file = st.file_uploader("Upload Shirt Mockup (Pic 1)", type=["jpg", "png", "jpeg"])

if file:
    # Image read karna
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    h, w, _ = img.shape

    # --- TEXTURE EXTRACTION LOGIC ---
    # 1. Shirt ki body ka main area (Sleeves aur collar ke baghair)
    # Hum design ko stretch karke flat square banayenge
    src_pts = np.float32([
        [w*0.25, h*0.2], [w*0.75, h*0.2], 
        [w*0.2, h*0.85], [w*0.8, h*0.85]
    ])
    
    dst_pts = np.float32([
        [0, 0], [1000, 0], 
        [0, 1000], [1000, 1000]
    ])

    # 2. Warp Perspective (Design ko khinch kar flat karna)
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    flat_texture = cv2.warpPerspective(img, matrix, (1000, 1000))
    
    # 3. Clean and Sharpen
    flat_texture = cv2.cvtColor(flat_texture, cv2.COLOR_BGR2RGB)

    # Results Display
    col1, col2 = st.columns(2)
    with col1:
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Pic 1: Original Mockup")
    with col2:
        # Ye aapka final flat design hai (Pic 2)
        st.image(flat_texture, caption="Pic 2: Extracted Flat Design")

    # Download Button
    res_img = cv2.cvtColor(flat_texture, cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode('.png', res_img)
    st.divider()
    st.download_button(
        label="📥 Download Flat Texture (PNG)",
        data=buffer.tobytes(),
        file_name="flat_texture_design.png",
        mime="image/png"
    )
