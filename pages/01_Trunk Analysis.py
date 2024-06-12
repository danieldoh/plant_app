import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import cv2
import numpy as np
from PIL import Image
from src.utils import two_points_distance

st.set_page_config(
    page_title="Trunk Analysis",
    page_icon="🌱",
)

st.title("Trunk Analysis")

aerosol_selection = st.selectbox("Select aerosol condition", ["Aerosol", "No Aerosol"], index = None, placeholder="Select an option")

if aerosol_selection == "Aerosol":
    st.write("Aerosol is selected.")
elif aerosol_selection == "No Aerosol":
    st.write("No Aerosol is selected.")

# session state
if 'aerosol_selection' not in st.session_state:
    st.session_state['aerosol_selection'] = aerosol_selection

if 'pixel_value' not in st.session_state:
    st.session_state['pixel_value'] = []

if 'coordinates' not in st.session_state:
    st.session_state['coordinates'] = (0, 0)

# Image path
uploadted_file = st.file_uploader("Choose an image file to be analyzed", type=["jpg", "jpeg", "png"])


if uploadted_file is not None:
    file_bytes = np.asarray(bytearray(uploadted_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)


    value = streamlit_image_coordinates(
        img_pil,
        use_column_width="always",
        key="pil",
    )

    if value:

        st.session_state['pixel_value'].append([value['x'], value['y']])

        st.write(st.session_state['pixel_value'])


