
import streamlit as st
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Define a function to save uploaded files
def save_uploaded_file(uploaded_file, project_folder):
    file_path = Path(project_folder) / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def render():
    st.title("CSV File Manager")
    
    # Define a project folder
    project_folder = Path("uploaded_files")
    project_folder.mkdir(exist_ok=True)

    st.subheader("Step 1: Upload CSV Files")
    uploaded_files = st.file_uploader(
        "Drag and drop CSV files here or click to upload", 
        type="csv", 
        accept_multiple_files=True
    )

    if uploaded_files:
        st.write("Uploaded Files:")
        for uploaded_file in uploaded_files:
            file_path = save_uploaded_file(uploaded_file, project_folder)
            st.write(f"- {uploaded_file.name} saved to {file_path}")

    if st.button("Next"):
        st.session_state.page = "classification"