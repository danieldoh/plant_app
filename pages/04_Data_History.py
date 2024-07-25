import streamlit as st
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
    worksheet="ratio",
    ttl="0m",
)
trunk_df = conn.read(
    worksheet="trunk",
    ttl="0m",
)
leaf_df = conn.read(
    worksheet="leaf",
    ttl="0m",
)

st.subheader("Ratio Data")
st.write(ratio_df)

st.subheader("Trunk Data")
st.write(trunk_df)

st.subheader("Leaf Data")
st.write(leaf_df)