import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="Flat Design Extractor", layout="wide")
st.title("👕 Mockup to Flat Design Extractor")

file = st.file_uploader("Upload Pic 1 (Mockup)", type=["jpg", "png", "jpeg"])

if file:
    # Image loading
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    h, w, _ = img.shape

    # --- FLAT EXTRACTION LOGIC ---
    # Hum shirt ke 4 corners ko pakad kar unhein flat square sheet par "stretch" karenge
    # Is se zoom nahi hoga, balkay poora design flat ho kar bahir aayega
    src_pts = np.float32([
        [w*0.2, h*0.1], [w*0.8, h*0.1], 
        [w*0.1, h*0.9], [w*0.9, h*0.9]
    ])
    
    dst_pts = np.float32([
        [0, 0], [1000, 0], 
        [0, 1000], [1000, 1000]
    ])

    # Perspective transformation (Design ko flat karna)
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    flat_design = cv2.warpPerspective(img, matrix, (1000, 1000))
    
    # Color correction
    flat_design_rgb = cv2.cvtColor(flat_design, cv2.COLOR_BGR2RGB)

    # Display Results
    col1, col2 = st.columns(2)
    with col1:
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Pic 1: Original Mockup")
    with col2:
        st.image(flat_design_rgb, caption="Pic 2: Extracted Flat Design (Full)")

    # Download
    _, buffer = cv2.imencode('.png', flat_design)
    st.divider()
    st.download_button(
        label="📥 Download Flat Design PNG",
        data=buffer.tobytes(),
        file_name="flat_texture.png",
        mime="image/png"
    )
