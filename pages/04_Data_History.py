import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

### Page Configurations ###
st.set_page_config(
    page_title="Data History",
    page_icon="💾",
    layout='wide',
)

st.title("💾 Data History")

conn = st.connection("gsheets", type=GSheetsConnection)

ratio_df = conn.read(
    worksheet="ratio"
)
trunk_df = conn.read(
    worksheet="trunk"
)
leaf_df = conn.read(
    worksheet="leaf"
)

st.subheader("Ratio Data")

'''new_row = {"date": "2024/7/25", "no_aerosol_top_ratio": 0.00057, "aerosol_top_ratio": 0.00057, "no_aerosol_side_ratio": 0.00057, "aerosol_side_ratio": 0.00057}
ratio_df = ratio_df.append(new_row, ignore_index=True)

conn.update(
    worksheet="ratio",
    data=ratio_df
)'''

st.write(ratio_df)

st.subheader("Trunk Data")
st.write(trunk_df)

st.subheader("Leaf Data")
st.write(leaf_df)