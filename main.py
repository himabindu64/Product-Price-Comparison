import streamlit as st
import cv2
import pytesseract
import easyocr
import numpy as np
from PIL import Image
import pandas as pd

from utils.price_fetcher import fetch_all_sites

# ---------------- STREAMLIT PAGE CONFIG ----------------
st.set_page_config(page_title=" 🛍️ Price Compare App - Free OCR", page_icon="🛒", layout="wide")

st.title(" 🛍️ Price Compare App - Free OCR")

# ---------------- OCR ENGINE SELECTION ----------------
ocr_engine = st.radio("Choose OCR Engine:", ["Tesseract (Local)", "EasyOCR (CPU)"])

if ocr_engine == "Tesseract (Local)":
    st.success(f"✅ Tesseract {pytesseract.get_tesseract_version()} is installed")
else:
    st.info("ℹ EasyOCR will run on CPU")

# ---------------- IMAGE UPLOAD ----------------
uploaded_file = st.file_uploader("📸 Choose product image", type=["jpg", "jpeg", "png"])

product_name = None

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 Uploaded Image", use_container_width=True)

    img_array = np.array(image)

    # OCR processing
    if ocr_engine == "Tesseract (Local)":
        text = pytesseract.image_to_string(img_array)
    else:
        reader = easyocr.Reader(["en"])
        results = reader.readtext(img_array)
        text = " ".join([res[1] for res in results])

    product_name = text.strip()
    st.write("### 🔍 OCR Analysis")
    if product_name:
        st.success(f"✅ Product Identified: {product_name}")
    else:
        st.error("❌ Could not detect product name. Try another image.")

# ---------------- FETCH PRICES ----------------
if product_name and st.button("🔍 Search Prices"):
    with st.spinner("Fetching best prices..."):
        results = fetch_all_sites(product_name)

    if results and len(results) > 0:
        st.write("### 💰 Price Comparison (in ₹)")

        df = pd.DataFrame(results)

        if not df.empty:
            # Add "Link" column with clickable links
            if "url" in df.columns:
                df["URL"] = df["url"].apply(lambda x: f'<a href="{x}" target="_blank">Link</a>')
                df = df.drop(columns=["url"])  # Remove raw URL column

            # Rename columns for clarity
            df = df.rename(columns={
                "store": "Website",
                "title": "Title",
                "price": "Price (₹)"
            })

            # Show table with clickable links (HTML rendering)
            st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

        else:
            st.warning("No results found from Amazon, Flipkart, or eBay.")
    else:
        st.warning("No results found from Amazon, Flipkart, or eBay.")