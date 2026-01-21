import streamlit as st
import cv2
import numpy as np
import base64

st.set_page_config(page_title="Pro Vector & Texture Extractor", layout="wide")
st.title("⚡ AI Vector & Texture Tool")

file = st.file_uploader("Upload Mockup (Pic 1)", type=["jpg", "png", "jpeg"])

if file:
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    h, w, _ = img.shape

    with st.spinner('Vectorizing Design...'):
        # 1. Texture Flattening (Shirt se design nikalna)
        roi = img[int(h*0.15):int(h*0.85), int(w*0.2):int(w*0.8)]
        flat = cv2.resize(roi, (1200, 1200), interpolation=cv2.INTER_LANCZOS4)
        
        # 2. Vectorization (SVG Generation Logic)
        gray = cv2.cvtColor(flat, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # SVG File banana
        svg_data = f'<svg width="1200" height="1200" xmlns="http://www.w3.org/2000/svg">'
        for cnt in contours:
            path_data = "M " + " L ".join([f"{p[0][0]},{p[0][1]}" for p in cnt]) + " Z"
            svg_data += f'<path d="{path_data}" fill="black" />'
        svg_data += '</svg>'

        # 3. GUI Display
        col1, col2 = st.columns(2)
        with col1:
            st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original Mockup")
        with col2:
            st.image(cv2.cvtColor(flat, cv2.COLOR_BGR2RGB), caption="Extracted Design")

        # 4. Professional Download Buttons
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            _, img_buf = cv2.imencode('.png', cv2.cvtColor(flat, cv2.COLOR_RGB2BGR))
            st.download_button("📥 Download PNG Texture", img_buf.tobytes(), "design.png", "image/png")
        with c2:
            st.download_button("📐 Download SVG Vector", svg_data, "design_vector.svg", "image/svg+xml")

st.success("Tip: Vectorizer.ai jaisa result milne ke liye SVG file download karein!")
