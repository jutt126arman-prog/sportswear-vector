import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="Pro Design Extractor", layout="wide")
st.title("⚡ Vectorizer Style Design Extractor")

file = st.file_uploader("Upload Mockup (Pic 1)", type=["jpg", "png", "jpeg"])

if file:
    # Image loading
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    h, w, _ = img.shape

    with st.spinner('Extracting Full Design...'):
        # --- FLAT EXTRACTION LOGIC ---
        # Shirt ke main area ko select karke poori screen par stretch karna
        src_pts = np.float32([
            [w*0.2, h*0.1], [w*0.8, h*0.1], 
            [w*0.15, h*0.9], [w*0.85, h*0.9]
        ])
        dst_pts = np.float32([
            [0, 0], [1500, 0], 
            [0, 1500], [1500, 1500]
        ])

        matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
        flat_design = cv2.warpPerspective(img, matrix, (1500, 1500))
        
        # Display Results
        col1, col2 = st.columns(2)
        with col1:
            st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Pic 1: Original")
        with col2:
            st.image(cv2.cvtColor(flat_design, cv2.COLOR_BGR2RGB), caption="Pic 2: Flat Design Result")

        # --- DOWNLOAD SECTION ---
        st.divider()
        st.subheader("📥 Download Files")
        
        # PNG Download
        _, img_buf = cv2.imencode('.png', flat_design)
        st.download_button(
            label="🖼️ Download High-Res PNG",
            data=img_buf.tobytes(),
            file_name="extracted_design.png",
            mime="image/png"
        )
        
        # SVG (Vector) Download - CorelDraw ke liye
        gray = cv2.cvtColor(flat_design, cv2.COLOR_BGR2GRAY)
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
            file_name="design_vector.svg",
            mime="image/svg+xml"
        )
