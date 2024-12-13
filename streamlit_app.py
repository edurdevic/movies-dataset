import streamlit as st
import os
import pandas as pd
import numpy as np
from pathlib import Path
from app import landing, classification


# Set up the Streamlit application
st.set_page_config(page_title="CSV File Manager", layout="centered")

# Define the main page
if "page" not in st.session_state:
    st.session_state.page = "classification"

# Landing page: File upload
if st.session_state.page == "landing":
    landing.render()

# Data classification page
elif st.session_state.page == "classification":
    classification.render()

elif st.session_state.page == "cleaning":
    st.title("Data cleaning")