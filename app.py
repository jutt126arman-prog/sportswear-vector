import streamlit as st
import cv2
import numpy as np
import svgwrite
import io
import base64

st.set_page_config(page_title="AI Sportswear Texture Extractor", layout="wide")
st.title("👕 AI Automatic Texture Extractor & Vectorizer")
st.write("Upload your image to extract the camouflage texture and get a Vector file.")

uploaded_file = st.file_uploader("Choose your design image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Image loading
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    h, w = img.shape[:2]

    col1, col2 = st.columns(2)

    with col1:
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original Image", use_container_width=True)

    # --- Processing: Texture Extraction ---
    with st.spinner('Extracting Texture and Generating Vector...'):
        # Convert to grayscale and threshold to isolate the pattern
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Finding contours (the "shapes" of the camouflage)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # --- Vector Generation (SVG) ---
        svg_output = io.StringIO()
        dwg = svgwrite.Drawing(size=(w, h))
        
        for contour in contours:
            points = []
            for point in contour:
                points.append((float(point[0][0]), float(point[0][1])))
            
            if len(points) > 2:
                # Adding paths to SVG
                dwg.add(dwg.polygon(points=points, fill='black', stroke='none'))
        
        dwg.write(svg_output)
        svg_str = svg_output.getvalue()

    with col2:
        st.image(thresh, caption="Extracted Texture (Preview)", use_container_width=True)

    st.divider()

    # --- Download Options ---
    st.subheader("📥 Download Vector Files")
    
    # SVG Download
    st.download_button(
        label="Download SVG (Best for CorelDraw/AI)",
        data=svg_str,
        file_name="extracted_texture.svg",
        mime="image/svg+xml"
    )
    
    st.success("Tip: CorelDraw mein 'Import' karein aur shapes ko apni marzi ka color dein.")
