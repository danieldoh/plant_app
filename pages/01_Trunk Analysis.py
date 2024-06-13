import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import io
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
        'cum_height': [],
        'height': [],
    }

if 'coordinates' not in st.session_state:
    st.session_state['coordinates'] = (0, 0)

# Image path
uploadted_file = st.file_uploader("Choose an image file to be analyzed", type=["jpg", "jpeg", "png"])


if uploadted_file is not None:
    img_pil = Image.open(io.BytesIO(uploadted_file.read()))

    value = streamlit_image_coordinates(
        img_pil,
        use_column_width="always",
        key="pil",
    )

    mode = st.selectbox("Select the category", ["Width", "Cumulative Height", "Height"], index = None, placeholder="Select an option")

    with st.sidebar:
        st.write(st.session_state['pixel_value']['width'])

    if mode == "Width":
        st.session_state['pixel_value']['height'] = []
        st.session_state['pixel_value']['cum_length'] = []
        cum_height_reset = False
        height_reset = False

        st.write("🖐️ Click on the image to select the two points for the trunk.")
        width_reset = st.button("Reset")
        message_width_reset = st.empty()

        if width_reset:
            st.session_state['pixel_value']['width'] = []
            message_width_reset.write("Resetting")

            time.sleep(2)

            message_width_reset.empty()
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
        st.session_state['pixel_value']['height'] = []
        width_reset = False
        height_reset = False

        st.write("🖐️ Click on the image to select the side of the trunk for the cumulative height.")

        cum_height_reset = st.button("Reset")
        cum_height_start = st.button("Start")

        message_cum_height_reset = st.empty()

        if cum_height_reset:
            st.session_state['pixel_value']['cum_height'] = []
            message_cum_height_reset.write("Resetting")

            time.sleep(2)

            message_cum_height_reset.empty()
            width_reset = False

        if value and not cum_height_reset:

            if len(st.session_state['pixel_value']['cum_height']) < 3:
                st.session_state['pixel_value']['width'].append([value['x'], value['y']])

            if len(st.session_state['pixel_value']['cum_height']) > 1:
                st.write("Number of Pixel Clicked: ", len(st.session_state['pixel_value']['width'])-1)
                st.write("Points Selected: ", st.session_state['pixel_value']['width'][1:])

            if len(st.session_state['pixel_value']['cum_height']) == 3:
                pix_1 = st.session_state['pixel_value']['cum_height'][-2]
                pix_2 = st.session_state['pixel_value']['cum_height'][-1]
                distance = two_points_distance(pix_1, pix_2)
                st.write("Trunk Width: ", f"{distance * 0.00057} m")
                st.write("Two points are already selected. Please reset the width to select new points.")

    elif mode == "Height":
        st.session_state['pixel_value']['width'] = []
        st.session_state['pixel_value']['cum_height'] = []
        width_reset = False
        cum_height_reset = False

        st.write("🖐️ Click on the image to select one bottom point and one top point for the height.")

        height_reset = st.button("Reset")
        message_height_reset = st.empty()

        if height_reset:
            st.session_state['pixel_value']['height'] = []
            message_height_reset.write("Resetting")

            time.sleep(2)

            message_height_reset.empty()
            height_reset = False

        if value and not height_reset:

            if len(st.session_state['pixel_value']['height']) < 3:
                st.session_state['pixel_value']['height'].append([value['x'], value['y']])

            if len(st.session_state['pixel_value']['height']) > 1:
                st.write("Number of Pixel Clicked: ", len(st.session_state['pixel_value']['height'])-1)
                st.write("Points Selected: ", st.session_state['pixel_value']['height'][1:])

            if len(st.session_state['pixel_value']['height']) == 3:
                pix_1 = st.session_state['pixel_value']['height'][-2]
                pix_2 = st.session_state['pixel_value']['height'][-1]
                distance = two_points_distance(pix_1, pix_2)
                st.write("Trunk Height: ", f"{distance * 0.00057} m")
                st.write("Two points are already selected. Please reset the height to select new points.")







