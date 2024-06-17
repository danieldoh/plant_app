import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import io
import time
import numpy as np
from PIL import Image
from src.utils import two_points_distance
from datetime import datetime

st.set_page_config(
    page_title="Leaf Analysis",
    page_icon="🍃",
    layout='wide',
)

st.title("Leaf Analysis")

aerosol_selection = st.selectbox("Select aerosol condition", ["Aerosol", "No Aerosol"], index = None, placeholder="Select an option")

if aerosol_selection == "Aerosol":
    st.write("Aerosol is selected.")
elif aerosol_selection == "No Aerosol":
    st.write("No Aerosol is selected.")

uploadted_file = st.file_uploader("Choose an image file to be analyzed", type=["jpg", "jpeg", "png"])

if uploadted_file is not None:
    img_pil = Image.open(io.BytesIO(uploadted_file.read()))

    value = streamlit_image_coordinates(
        img_pil,
        use_column_width="always",
        key="pil",
    )


