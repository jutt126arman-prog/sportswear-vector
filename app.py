import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="Sportswear Texture Extractor")
st.title("👕 AI Texture Design Extractor")
st.write("Upload your shirt image to extract only the design texture.")

file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if file:
    # Processing
    with st.spinner('Extracting design... please wait...'):
        input_image = Image.open(file)
        
        # AI Background Removal (Sirf design bachega)
        output_image = remove(input_image)
        
        # Display Results
        col1, col2 = st.columns(2)
        with col1:
            st.image(input_image, caption="Original Image", use_container_width=True)
        with col2:
            st.image(output_image, caption="Extracted Texture", use_container_width=True)
        
        # Download Button
        buf = io.BytesIO()
        output_image.save(buf, format="PNG")
        st.download_button("📥 Download Texture PNG", buf.getvalue(), "extracted_design.png", "image/png")
