import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="Texture Extractor")
st.title("👕 AI Texture Extractor")

file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if file:
    # Image process karna
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # Background Removal (Grayscale + Thresholding)
    # Ye tareeka foran chalta hai bina kisi error ke
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Texture extract karna
    res = cv2.bitwise_and(img, img, mask=mask)
    res_rgb = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
    
    st.image(res_rgb, caption="Extracted Texture")
    
    # Download Button
    result_img = Image.fromarray(res_rgb)
    buf = io.BytesIO()
    result_img.save(buf, format="PNG")
    st.download_button("Download PNG", buf.getvalue(), "texture.png", "image/png")
