import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Plant Growth Analyzer",
    page_icon="🌱",
)

st.title("🪴 Plant Growth Analyzer")

st.markdown(
    '''
    ## 👋  Hello!

    ##### Welcome to the Plant Growth Analyzer!
    ######  This app is designed to help you analyze the growth of your plants.

    - ## 🌳 [Trunk Analysis](/Trunk_Analysis)
        - ##### Width 
        - ##### Cumulative Height
        - ##### Height
        - ##### Surface Area
        - ##### Tilt Angle
        - ##### Leaf Tilt Angle
    - ## 🌿 [Leaf Analysis](/Leaf_Analysis)
        - ##### Width
        - ##### Length
        - ##### Area
        - ##### Venation Analysis
    - ## 📐 [Ratio Calculation](/Ratio_Calculation)
    - ## 💾 [Data History](/Data_History)
'''
)

