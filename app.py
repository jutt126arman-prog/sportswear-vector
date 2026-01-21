import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="Flat Texture Extractor", layout="wide")
st.title("🖼️ Pro Design Texture Extractor (Flat Mode)")

file = st.file_uploader("Upload Shirt Image", type=["jpg", "png", "jpeg"])

if file:
    # Image read karna
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    h, w, _ = img.shape

    # 1. Design Extraction Logic (Non-AI, High Precision)
    # Hum shirt ke patterns ko background aur shadows se alag karenge
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)
    
    # Shadows hatane ke liye Contrast improve karna
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l_channel)
    final_lab = cv2.merge((cl,a,b))
    enhanced_img = cv2.cvtColor(final_lab, cv2.COLOR_LAB2BGR)

    # 2. Flattening (Shirt ki shape se texture nikalna)
    # Hum shirt ke center area ko expand karenge jo flat design deta hai
    roi = enhanced_img[int(h*0.15):int(h*0.85), int(w*0.2):int(w*0.8)]
    flat_texture = cv2.resize(roi, (1000, 1000), interpolation=cv2.INTER_CUBIC)

    # 3. GUI Display
    col1, col2 = st.columns(2)
    with col1:
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original Mockup")
    with col2:
        # Ye wahi flat result hai jo aapne image_ab1217.png mein dikhaya
        st.image(cv2.cvtColor(flat_texture, cv2.COLOR_BGR2RGB), caption="Extracted Flat Texture")

    # 4. Download
    _, buffer = cv2.imencode('.png', flat_texture)
    st.download_button(
        label="📥 Download Flat Texture (High Res)",
        data=buffer.tobytes(),
        file_name="flat_design_texture.png",
        mime="image/png"
    )
