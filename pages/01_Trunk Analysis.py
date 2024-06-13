import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import cv2
import time
import numpy as np
from PIL import Image
from src.utils import two_points_distance
from datetime import datetime

st.set_page_config(
    page_title="Trunk Analysis",
    page_icon="🌱",
    layout='wide',
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
    st.session_state['pixel_value'] = {
        'width': [[0,0]],
        'cum_length': [],
        'height': [],
    }

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
    
    mode = st.selectbox("Select the category", ["Width", "Cumulative Height", "Height"], index = None, placeholder="Select an option")

    with st.sidebar:
        st.write(st.session_state['pixel_value']['width'])

    if mode == "Width":

        st.write("Instruction: Click on the image to select the two points.")
        width_reset = st.button("Reset")
        message_reset = st.empty()
        
        if width_reset:
            st.session_state['pixel_value']['width'] = []
            message_reset.write("Resetting")

            time.sleep(2)

            message_reset.empty()
            width_reset = False

        if value and not width_reset:

            if len(st.session_state['pixel_value']['width']) < 3:
                st.session_state['pixel_value']['width'].append([value['x'], value['y']])

            if len(st.session_state['pixel_value']['width']) > 1:
                st.write("Number of Pixel Clicked: ", len(st.session_state['pixel_value']['width'])-1)
                st.write("Points Selected: ", st.session_state['pixel_value']['width'][1:])

            if len(st.session_state['pixel_value']['width']) == 3:
                pix_1 = st.session_state['pixel_value']['width'][-2]
                pix_2 = st.session_state['pixel_value']['width'][-1]
                distance = two_points_distance(pix_1, pix_2)
                st.write("Trunk Width: ", f"{distance * 0.00057} m")
                st.write("Two points are already selected. Please reset the width to select new points.")

    
    elif mode == "Cumulative Height":
        st.session_state['pixel_value']['width'] = []
        width_reset = False

        st.write("Click on the image to select the base of the trunk.")
    






            


