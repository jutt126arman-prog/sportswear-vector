import streamlit as st
from transparent_background import Remover
from PIL import Image
import io

st.set_page_config(page_title="AI Texture Extractor")
st.title("👕 AI Sportswear Texture Extractor")

# AI Remover load ho raha hai
@st.cache_resource
def load_remover():
    return Remover()

remover = load_remover()

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file).convert('RGB')
    
    with st.spinner('Extracting texture... please wait...'):
        # AI Processing (Isme 1-2 minute lag sakte hain pehli baar)
        out = remover.process(img) 
        
        # Display Result
        st.image(out, caption="Extracted Texture", use_container_width=True)
        
        # Download as PNG (Transparent)
        buf = io.BytesIO()
        out.save(buf, format="PNG")
        st.download_button(
            label="Download PNG",
            data=buf.getvalue(),
            file_name="texture_extracted.png",
            mime="image/png"
        )
