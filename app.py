import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="Pro Vector Extractor", layout="wide")
st.title("⚡ Pro Vectorizer (Flat Design)")

file = st.file_uploader("Upload Mockup (Pic 1)", type=["jpg", "png", "jpeg"])

if file:
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    h, w, _ = img.shape

    with st.spinner('Processing Vector Design...'):
        # 1. Perspective Flattening (Shirt se design bahir nikalna)
        src_pts = np.float32([[w*0.2, h*0.1], [w*0.8, h*0.1], [w*0.15, h*0.9], [w*0.85, h*0.9]])
        dst_pts = np.float32([[0, 0], [1500, 0], [0, 1500], [1500, 1500]])
        matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
        flat = cv2.warpPerspective(img, matrix, (1500, 1500))
        
        # 2. Vectorization Cleanup (Vectorizer.ai jaisa look dene ke liye)
        # Shading aur shadows hatana
        gray = cv2.cvtColor(flat, cv2.COLOR_BGR2GRAY)
        smooth = cv2.bilateralFilter(gray, 9, 75, 75) # Edges ko smooth rakhta hai
        
        # Adaptive thresholding (Har corner ka design pakadne ke liye)
        thresh = cv2.adaptiveThreshold(smooth, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        
        # 3. SVG Generation (High Resolution Paths)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
        
        svg_paths = []
        for cnt in contours:
            if cv2.contourArea(cnt) > 20: # Chota kachra hatane ke liye
                path = "M " + " L ".join([f"{p[0][0]},{p[0][1]}" for p in cnt]) + " Z"
                svg_paths.append(f'<path d="{path}" fill="black" />')
        
        svg_data = f'<svg width="1500" height="1500" viewBox="0 0 1500 1500" xmlns="http://www.w3.org/2000/svg" style="background:white">' + "".join(svg_paths) + '</svg>'

        # Results Display
        col1, col2 = st.columns(2)
        with col1:
            st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Pic 1: Original")
        with col2:
            st.image(cv2.cvtColor(flat, cv2.COLOR_BGR2RGB), caption="Pic 2: Flat Design (High Res)")

        # 4. Download Section
        st.divider()
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            _, img_buf = cv2.imencode('.png', flat)
            st.download_button("📥 Download PNG Design", img_buf.tobytes(), "design_flat.png", "image/png")
        with col_dl2:
            st.download_button("📐 Download SVG Vector (Corel/AI)", svg_data, "design_vector.svg", "image/svg+xml")

st.info("Tip: SVG file ko CorelDraw mein 'Import' karein, ye bilkul vectorizer jaisa saaf result degi.")
