import streamlit as st
import os
import pandas as pd
from pathlib import Path

# Define a function to save uploaded files
def save_uploaded_file(uploaded_file, project_folder):
    file_path = Path(project_folder) / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Set up the Streamlit application
st.set_page_config(page_title="CSV File Manager", layout="centered")

# Define the main page
if "page" not in st.session_state:
    st.session_state.page = "classification"

# Landing page: File upload
if st.session_state.page == "landing":
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

    if st.button("Go to Data Classification"):
        st.session_state.page = "classification"

# Data classification page
elif st.session_state.page == "classification":
    st.title("Data Classification")

    # Fetch all uploaded files
    project_folder = Path("uploaded_files")
    csv_files = list(project_folder.glob("*.csv"))

    if not csv_files:
        st.warning("No files uploaded yet. Please go back to upload CSV files.")
        if st.button("Back to Upload"):
            st.session_state.page = "landing"
    else:
        st.write("Classify the columns in your uploaded files.")

        for csv_file in csv_files:
            st.subheader(f"File: {csv_file.name}")
            try:
                df = pd.read_csv(csv_file)

                # Prepare data for the data editor
                def calculate_statistics(col_data):
                    if pd.api.types.is_numeric_dtype(col_data):
                        return {
                            "Min": col_data.min(),
                            "Avg": col_data.mean(),
                            "Max": col_data.max(),
                            "Nulls": col_data.isnull().sum(),
                            "Distinct": col_data.nunique()
                        }
                    elif pd.api.types.is_string_dtype(col_data):
                        return {
                            "Min": "-",
                            "Avg": "-",
                            "Max": "-",
                            "Nulls": col_data.isnull().sum(),
                            "Distinct": col_data.nunique()
                        }
                    else:
                        return {"Min": "-", "Avg": "-", "Max": "-", "Nulls": "-", "Distinct": "-"}

                data_editor_df = pd.DataFrame({
                    "Column Name": df.columns,
                    "Role": "",
                    "Min": [calculate_statistics(df[col])["Min"] for col in df.columns],
                    "Avg": [calculate_statistics(df[col])["Avg"] for col in df.columns],
                    "Max": [calculate_statistics(df[col])["Max"] for col in df.columns],
                    "Null Values": [calculate_statistics(df[col])["Nulls"] for col in df.columns],
                    "Distinct Values": [calculate_statistics(df[col])["Distinct"] for col in df.columns],
                    "Sample Data": [
                        ", ".join(map(str, df[col].head(3).tolist())) for col in df.columns
                    ],
                    "Notes": ""
                })

                st.data_editor(
                    data_editor_df,
                    column_config={
                        "Role": st.column_config.SelectboxColumn(
                            default=None, 
                            options=["primary key", "feature", "timepoint", "metadata", "patient metadata", "gene expression"]
                        ),
                        "Sample Data": st.column_config.ListColumn(),
                        "Null Values": st.column_config.ProgressColumn(width="small", min_value=0, max_value=len(df), format="%d"),
                        "Distinct Values": st.column_config.ProgressColumn(width="small", min_value=0, max_value=len(df), format="%d")
                    },
                    key=f"data_editor_{csv_file.name}",
                    num_rows="dynamic"
                )

            except Exception as e:
                st.error(f"Error reading {csv_file.name}: {e}")

        if st.button("Finish"):
            st.success("Data classification completed.")
