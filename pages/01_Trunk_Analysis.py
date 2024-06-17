import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import io
import time
import numpy as np
from PIL import Image
from src.utils import two_points_distance, angle_calculation
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

if "calculated_values" not in st.session_state:
    st.session_state["calculated_values"] = {
        "width": 0.0,
        "cum_height": 0.0,
        "height": 0.0,
        "angle": 0.0,
        "leaf_angle": 0.0
    }

if 'width' not in st.session_state:
    st.session_state['width'] = [[0,0]]

if 'height' not in st.session_state:
    st.session_state['height'] = [[0,0]]

if 'cum_height' not in st.session_state:
    st.session_state['cum_height'] = [[0,0]]

if 'angle' not in st.session_state:
    st.session_state['angle'] = [[0,0]]

if 'leaf_angle' not in st.session_state:
    st.session_state['leaf_angle'] = [[0,0]]

# Image path
uploadted_file = st.file_uploader("Choose an image file to be analyzed", type=["jpg", "jpeg", "png"])


if uploadted_file is not None:
    img_pil = Image.open(io.BytesIO(uploadted_file.read()))

    value = streamlit_image_coordinates(
        img_pil,
        use_column_width="always",
        key="pil",
    )

    st.write(f"Width: {st.session_state['calculated_values']['width']} m")
    st.write(f"Cumulative Height: {st.session_state['calculated_values']['cum_height']} m")
    st.write(f"Height: {st.session_state['calculated_values']['height']} m")
    st.write(f"Tilt Angle: {st.session_state['calculated_values']['angle']} degrees")
    st.write(f"Leaf Tilt Angle: {st.session_state['calculated_values']['leaf_angle']} degrees")

    mode = st.selectbox("Select the category", ["Width", "Cumulative Height", "Height", "Tilt Angle", "Leaf Tilt Angle"], index = None, placeholder="Select an option")

    with st.sidebar:
        st.write(st.session_state['width'])
    

    if mode == "Width":
        st.session_state['angle'] = []
        st.session_state['height'] = []
        st.session_state['cum_height'] = []
        st.session_state['leaf_angle'] = []

        st.write("🖐️ Click on the image to select the two points for the trunk.")
        width_reset = st.button("RESET")
        message_width_reset = st.empty()

        if width_reset:
            st.session_state['width'] = []
            message_width_reset.write("Resetting")

            time.sleep(2)

            message_width_reset.empty()
            width_reset = False

        if value and not width_reset:

            if len(st.session_state['width']) < 3:
                st.session_state['width'].append([value['x'], value['y']])

            if len(st.session_state['width']) == 3:
                pix_1 = st.session_state['width'][-2]
                pix_2 = st.session_state['width'][-1]
                st.session_state['calculated_values']['width'] = two_points_distance(pix_1, pix_2)
                st.write("Trunk Width: ", f"{st.session_state['calculated_values']['width'] * 0.00057} m")
                st.write("Width calculation is finished. Please press the RESET button to select new points.")

            if len(st.session_state['width']) > 1:
                st.write("Number of Pixel Clicked: ", len(st.session_state['width'])-1)
                st.write("Points Selected: ", st.session_state['width'][1:])


    elif mode == "Cumulative Height":
        st.session_state['angle'] = []
        st.session_state['width'] = []
        st.session_state['height'] = []
        st.session_state['leaf_angle'] = []

        st.write("🖐️ Click on the image to select the side of the trunk for the cumulative height.")
        st.write("🖐️ Press START button and click the points. When you finish, press END button")

        cum_height_reset = st.button("RESET")
        cum_height_start = st.button("START")
        cum_height_end = st.button("END")

        message_cum_height_reset = st.empty()

        if cum_height_start:
            st.session_state['cum_height'] = []

        if cum_height_reset:
            st.session_state['cum_height'] = []
            message_cum_height_reset.write("Resetting")

            time.sleep(2)

            message_cum_height_reset.empty()
            cum_height_reset = False
            cum_height_start = False
            cum_height_end = False

        if value and not cum_height_reset:

            if not cum_height_end:
                st.session_state['cum_height'].append([value['x'], value['y']])

            if cum_height_end:
                for i in range(1, len(st.session_state['cum_height'])-1):
                    pix_1 = st.session_state['cum_height'][i]
                    pix_2 = st.session_state['cum_height'][i+1]
                    st.session_state['calculated_values']['cum_height'] += two_points_distance(pix_1, pix_2)
                st.write("Trunk Cumulative Height: ", f"{st.session_state['calculated_values']['cum_height'] * 0.00057} m")
                st.write("Cumulative height calcuation is finished. Please press the RESET button to select new points.")

            if len(st.session_state['cum_height']) > 1:
                st.write("Number of Pixel Clicked: ", len(st.session_state['cum_height'])-1)
                st.write("Points Selected: ", st.session_state['cum_height'][1:])

    elif mode == "Height":
        st.session_state['angle'] = []
        st.session_state['width'] = []
        st.session_state['cum_height'] = []
        st.session_state['leaf_angle'] = []

        st.write("🖐️ Click on the image to select one bottom point and one top point for the height.")

        height_reset = st.button("RESET")
        message_height_reset = st.empty()

        if height_reset:
            st.session_state['height'] = []
            message_height_reset.write("Resetting")

            time.sleep(2)

            message_height_reset.empty()
            height_reset = False

        if value and not height_reset:

            if len(st.session_state['height']) < 3:
                st.session_state['height'].append([value['x'], value['y']])

            if len(st.session_state['height']) == 3:
                pix_1 = st.session_state['height'][-2]
                pix_2 = st.session_state['height'][-1]
                st.session_state['calculated_values']['height'] = two_points_distance(pix_1, pix_2)
                st.write("Trunk Height: ", f"{st.session_state['calculated_values']['height'] * 0.00057} m")
                st.write("Height calcuation is finished. Please press the RESET button to select new points.")

            if len(st.session_state['height']) > 1:
                st.write("Number of Pixel Clicked: ", len(st.session_state['height'])-1)
                st.write("Points Selected: ", st.session_state['height'][1:])


    elif mode == "Tilt Angle":
        st.session_state['width'] = []
        st.session_state['cum_height'] = []
        st.session_state['height'] = []
        st.session_state['leaf_angle'] = []

        st.write("🖐️ Click on the image to select three points for the angle.")
        st.write("🖐️ Click Order: BOTTOM - STRAIGHT TOP - TILTED TOP")

        angle_reset = st.button("RESET")
        message_angle_reset = st.empty()

        if angle_reset:
            st.session_state['angle'] = []
            message_angle_reset.write("Resetting")

            time.sleep(2)

            message_angle_reset.empty()
            angle_reset = False

        if value and not angle_reset:

            if len(st.session_state['angle']) < 4:
                st.session_state['angle'].append([value['x'], value['y']])

            if len(st.session_state['angle']) == 4:
                pix_1 = st.session_state['angle'][-3]
                pix_2 = st.session_state['angle'][-2]
                pix_3 = st.session_state['angle'][-1]
                st.session_state['calculated_values']['angle'] = angle_calculation(pix_1, pix_2, pix_3)
                st.write("Trunk Tilt Angle: ", f"{st.session_state['calculated_values']['angle']} degrees")
                st.write("Angle calcuation is finished. Please press the RESET button to select new points.")

            if len(st.session_state['angle']) > 1:
                st.write("Number of Pixel Clicked: ", len(st.session_state['angle'])-1)
                st.write("Points Selected: ", st.session_state['angle'][1:])
    
    elif mode == "Leaf Tilt Angle":
        st.session_state['width'] = []
        st.session_state['cum_height'] = []
        st.session_state['height'] = []
        st.session_state['angle'] = []

        st.write("🖐️ Click on the image to select three points for the leaf angle.")
        st.write("🖐️ Click Order: BOTTOM - STRAIGHT TOP - TILTED TOP")

        leaf_angle_reset = st.button("RESET")
        message_leaf_angle_reset = st.empty()

        if leaf_angle_reset:
            st.session_state['leaf_angle'] = []
            message_leaf_angle_reset.write("Resetting")

            time.sleep(2)

            message_leaf_angle_reset.empty()
            angle_reset = False

        if value and not leaf_angle_reset:

            if len(st.session_state['leaf_angle']) < 4:
                st.session_state['leaf_angle'].append([value['x'], value['y']])

            if len(st.session_state['leaf_angle']) == 4:
                pix_1 = st.session_state['leaf_angle'][-3]
                pix_2 = st.session_state['leaf_angle'][-2]
                pix_3 = st.session_state['leaf_angle'][-1]
                st.session_state['calculated_values']['leaf_angle'] = angle_calculation(pix_1, pix_2, pix_3)
                st.write("Leaf Tilt Angle: ", f"{st.session_state['calculated_values']['leaf_angle']} degrees")
                st.write("Leaf Angle calcuation is finished. Please press the RESET button to select new points.")

            if len(st.session_state['leaf_angle']) > 1:
                st.write("Number of Pixel Clicked: ", len(st.session_state['leaf_angle'])-1)
                st.write("Points Selected: ", st.session_state['leaf_angle'][1:])


