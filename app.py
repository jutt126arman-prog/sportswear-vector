import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="Design Extractor", layout="wide")
st.title("👕 Pro Sportswear Texture Extractor")

uploaded_file = st.file_uploader("Upload Shirt Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Image ko load karna
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # 1. Background isolate karna (Is se design bahir nikal aayega)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # 2. Design extract karna
    texture = cv2.bitwise_and(img, img, mask=thresh)
    texture_rgb = cv2.cvtColor(texture, cv2.COLOR_BGR2RGB)
    
    # 3. GUI Layout
    col1, col2 = st.columns(2)
    with col1:
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original Image", use_container_width=True)
    with col2:
        st.image(texture_rgb, caption="Extracted Texture Design", use_container_width=True)
    
    # 4. Download Button
    result_img = Image.fromarray(texture_rgb)
    buf = io.BytesIO()
    result_img.save(buf, format="PNG")
    
    st.divider()
    st.download_button(
        label="📥 Download Texture (Transparent PNG)",
        data=buf.getvalue(),
        file_name="extracted_design.png",
        mime="image/png"
    )
