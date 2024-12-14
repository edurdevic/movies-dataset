import streamlit as st
import os
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

    # Handle file uploads
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path = Path(project_folder) / uploaded_file.name

            # Check if file already exists
            if file_path.exists():
                st.write(f"Replacing existing file: {uploaded_file.name}")

            # Save or replace the file
            save_uploaded_file(uploaded_file, project_folder)
            st.write(f"- {uploaded_file.name} saved to {file_path}")

    # st.subheader("Step 2: Manage Uploaded Files")

    # # Display list of files in the project folder
    # files = list(project_folder.glob("*.csv"))

    # if files:
    #     st.write("Files in the project folder:")
    #     for file in files:
    #         col1, col2 = st.columns([3, 1])

    #         with col1:
    #             st.write(file.name)

    #         with col2:
    #             # Delete button for each file
    #             if st.button("Delete", key=f"delete_{file.name}"):
    #                 file.unlink()  # Delete the file
    #                 st.rerun()
    # else:
    #     st.write("No files uploaded yet.")

    if st.button("Next"):
        st.session_state.page = "classification"
        st.rerun()

if __name__ == "__main__":
    render()
