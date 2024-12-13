import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

def render():
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

                def generate_histogram(col_data):
                    if pd.api.types.is_numeric_dtype(col_data):
                        counts, bin_edges = np.histogram(col_data.dropna(), bins=20)
                        return counts.tolist()
                    return []

                data_editor_df = pd.DataFrame({
                    "Column Name": df.columns,
                    "Use": [True] * len(df.columns),
                    "Role": "",
                    "Min": [calculate_statistics(df[col])["Min"] for col in df.columns],
                    "Avg": [calculate_statistics(df[col])["Avg"] for col in df.columns],
                    "Max": [calculate_statistics(df[col])["Max"] for col in df.columns],
                    "Null Values": [calculate_statistics(df[col])["Nulls"] for col in df.columns],
                    "Distinct Values": [calculate_statistics(df[col])["Distinct"] for col in df.columns],
                    "Sample Data": [
                        ", ".join(map(str, df[col].head(3).tolist())) for col in df.columns
                    ],
                    "Histogram": [
                        generate_histogram(df[col]) for col in df.columns
                    ],
                    "Notes": ""
                })

                st.data_editor(
                    data_editor_df,
                    column_config={
                        "Use": st.column_config.CheckboxColumn(
                            default=True,
                            help="Use this column for analysis"
                        ),
                        "Role": st.column_config.SelectboxColumn(
                            default=None, 
                            options=["primary key", "feature", "timepoint", "metadata", "patient metadata", "gene expression"]
                        ),
                        "Sample Data": st.column_config.ListColumn(),
                        "Null Values": st.column_config.ProgressColumn(width="small", min_value=0, max_value=len(df), format="%d"),
                        "Distinct Values": st.column_config.ProgressColumn(width="small", min_value=0, max_value=len(df), format="%d"),
                        "Histogram": st.column_config.BarChartColumn(
                            "Histogram",
                            help="Data distribution for numeric columns (20 bins)",
                            y_min=0,
                            y_max=max([
                                max(generate_histogram(df[col])) if pd.api.types.is_numeric_dtype(df[col]) and len(generate_histogram(df[col])) > 0 else 0 for col in df.columns
                            ])
                        )
                    },
                    disabled=["Column Name", "Min", "Avg", "Max", "Null Values", "Distinct Values", "Sample Data", "Histogram"],
                    key=f"data_editor_{csv_file.name}",
                    num_rows="dynamic"
                )

            except Exception as e:
                st.error(f"Error reading {csv_file.name}: {e}")

        if st.button("Next"):
            st.session_state.page = "cleaning"