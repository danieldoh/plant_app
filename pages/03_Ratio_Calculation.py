import streamlit as st
import pandas as pd
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Ratio Calculation",
    page_icon="📐",
    layout='wide',
)

st.title("📐 Ratio Calculation")

conn = st.connection("gsheets", type=GSheetsConnection)

ratio_df = conn.read(
    worksheet="ratio"
)

st.subheader("Ratio Data")

st.write(ratio_df)