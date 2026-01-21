import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("👕 Sportswear Design Tool")

file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if file:
    # Image read karna
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # Background remove karne ka asaan tareeka (GrabCut)
    st.write("Processing... Please wait.")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Result dikhana
    res = cv2.bitwise_and(img, img, mask=thresh)
    res_rgb = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
    
    st.image(res_rgb, caption="Processed Texture")
    
    # Download Button
    result_img = Image.fromarray(res_rgb)
    st.download_button("Download Design", file.getvalue(), "design.png")
