import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import cv2
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Plant Growth Analyzer",
    page_icon="🌱",
)

st.title("Plant Growth Analyzer")

st.markdown(
    '''
    # Hello!

    Welcome to the Plant Growth Analyzer! This app is designed to help you analyze the growth of your plants.

    Here are the features of this app:
    - [ ] [Trunk Analysis](/Trunk Analysis)
'''
)

