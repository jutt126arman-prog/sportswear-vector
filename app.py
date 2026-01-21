import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="Vector Extractor", layout="wide")
st.title("⚡ AI Vector & Flat Texture Extractor")

# File Upload
file = st.file_uploader("Upload Pic 1 (Mockup)", type=["jpg", "png", "jpeg"])

if file:
    # 1. Image Processing
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    h, w, _ = img.shape

    # 2. Flattening Logic (Design Stretch)
    src_pts = np.float32([[w*0.2, h*0.1], [w*0.8, h*0.1], [w*0.15, h*0.9], [w*0.85, h*0.9]])
    dst_pts = np.float32([[0, 0], [1500, 0], [0, 1500], [1500, 1500]])
    matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
    flat = cv2.warpPerspective(img, matrix, (1500, 1500))
    
    # 3. Display Images
    col1, col2 = st.columns(2)
    with col1:
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original Mockup")
    with col2:
        st.image(cv2.cvtColor(flat, cv2.COLOR_BGR2RGB), caption="Extracted Flat Design")

    # 4. DOWNLOAD BUTTONS (Ye lazmi nazar aayenge)
    st.markdown("### 📥 Download Results")
    
    # PNG Download
    _, img_encoded = cv2.imencode('.png', flat)
    st.download_button(
        label="🖼️ Download PNG (High Quality)",
        data=img_encoded.tobytes(),
        file_name="flat_design.png",
        mime="image/png",
        key="png_btn"
    )

    # SVG Vector Download (For CorelDraw)
    gray = cv2.cvtColor(flat, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    svg_data = f'<svg width="1500" height="1500" xmlns="http://www.w3.org/2000/svg">'
    for cnt in contours:
        path = "M " + " L ".join([f"{p[0][0]},{p[0][1]}" for p in cnt]) + " Z"
        svg_data += f'<path d="{path}" fill="black" />'
    svg_data += '</svg>'
    
    st.download_button(
        label="📐 Download SVG Vector (CorelDraw)",
        data=svg_data,
        file_name="vector_design.svg",
        mime="image/svg+xml",
        key="svg_btn"
    )
