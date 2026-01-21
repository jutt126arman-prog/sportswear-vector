import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="Texture Extractor", layout="wide")
st.title("👕 AI Texture Design Extractor")

file = st.file_uploader("Upload Shirt Image", type=["jpg", "png", "jpeg"])

if file:
    # Image loading
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    h, w, _ = img.shape

    # --- Texture Extraction Logic ---
    # Hum shirt ke center se texture ka 50% hissa nikalenge jo flat hota hai
    start_row, start_col = int(h * 0.25), int(w * 0.25)
    end_row, end_col = int(h * 0.75), int(w * 0.75)
    texture_crop = img[start_row:end_row, start_col:end_col]

    # Texture ko saaf karna (Noise removal)
    texture_clean = cv2.detailEnhance(texture_crop, sigma_s=10, sigma_r=0.15)
    texture_rgb = cv2.cvtColor(texture_clean, cv2.COLOR_BGR2RGB)

    col1, col2 = st.columns(2)
    with col1:
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original Image", use_container_width=True)
    with col2:
        # Ye aapko flat texture dikhayega bina shirt ki shape ke
        st.image(texture_rgb, caption="Extracted Flat Texture", use_container_width=True)

    # --- Download ---
    result_img = Image.fromarray(texture_rgb)
    buf = io.BytesIO()
    result_img.save(buf, format="PNG")
    
    st.divider()
    st.download_button(
        label="📥 Download Flat Texture Design",
        data=buf.getvalue(),
        file_name="flat_texture.png",
        mime="image/png"
    )
