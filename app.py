import pandas as pd,streamlit as st
df=pd.read_csv("data/locations_master.csv")
st.title("Location Lifestyle AI V4 Sandbox")
st.write(f"Locations: {len(df)}")
current=st.selectbox("Current Location",df.name)
st.multiselect("Important Locations",df.name.tolist())
st.dataframe(df.head(20))