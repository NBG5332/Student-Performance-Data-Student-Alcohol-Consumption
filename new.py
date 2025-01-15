import pandas as pd
import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv
import time
import sys
import subprocess
import random
import io
import traceback

load_dotenv()

# Check for openpyxl
try:
    import openpyxl
except ImportError:
    st.error("The 'openpyxl' package is required but not installed. Please install it manually using the command: pip install openpyxl")
    st.stop()

# Predefined list of titles
target_titles = [
    "Doctor", "Nurse", "Psychiatrist", "Psychologist", "Surgeon", "Dentist",
    "Dental Assistant", "Veterinarian", "Veterinarian Assistant",
    "Non Medical Professional", "Other Medical Professional", "Chiropractor"
]

def shorten_titles(titles, model):
    titles = [str(title) if pd.notna(title) else "" for title in titles]
    prompt = (
        "Shorten each of the following job titles to match one of these target titles: \n"
        f"{', '.join(target_titles)}\n"
        "Provide the closest matching title from the target list based on the input titles. \n"
        "Provide only the shortened titles, one per line, in the same order as the input.\n"
        "Shorten each of the following job titles to match one of these target titles:\n"
        f"{chr(10).join(titles)}"
    )
    
    response = model.generate_content(prompt)
    
    # Assuming response contains candidates with content parts
    try:
        shortened_titles = response.candidates[0].content.parts[0].text.strip().split('\n')
    except (IndexError, AttributeError):
        st.error("Unexpected response format from the API.")
        return ["Unknown"] * len(titles)
    
    return shortened_titles


def process_excel(df, start_row, end_row, batch_size, input_column, model):
    if 'shortened_title' not in df.columns:
        df['shortened_title'] = ""

    total_rows = min(end_row, len(df)) - start_row
    progress_bar = st.progress(0)
    status_text = st.empty()
    batches_processed = []

    if total_rows <= 0:
        st.error("Invalid range of rows specified.")
        return df, batches_processed

    for i in range(start_row, min(end_row, len(df)), batch_size):
        batch_start_time = time.time()
        batch_end = min(i + batch_size, end_row)
        original_titles = df.loc[i:batch_end-1, input_column].tolist()

        st.write(f"Processing rows {i} to {batch_end-1} (batch size: {batch_size})")

        shortened_titles = shorten_titles(original_titles, model)

        for j, shortened_title in enumerate(shortened_titles):
            df.loc[i+j, 'shortened_title'] = shortened_title

        batch_end_time = time.time()
        batch_duration = batch_end_time - batch_start_time

        processed_rows = batch_end - start_row
        progress = processed_rows / total_rows
        progress_bar.progress(min(progress, 1.0))
        status_text.text(f"Processed {processed_rows} out of {total_rows} rows in {batch_duration:.2f} seconds")

        batches_processed.append((i, batch_end-1))

        delay = random.uniform(0, 0.5)
        st.write(f"Waiting for {delay:.2f} seconds before the next batch...")
        time.sleep(delay)

    st.write("All specified rows have been processed.")
    return df, batches_processed


st.title("Job Title Shortener")

# API Key input
os.getenv("GOOGLE_API_KEY")
api_key=os.getenv("GOOGLE_API_KEY")
if len(api_key)>0:
    try:
        os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.success("API key configured successfully!")
    except Exception as e:
        st.error(f"Error configuring API key: {str(e)}")
        st.stop()

    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.write(f"Total rows in the file: {len(df)}")

        columns = df.columns.tolist()
        input_column = st.selectbox("Select the column containing job titles", columns)

        start_row = st.number_input("Enter the starting row number (0-based index)", min_value=0, max_value=len(df)-1, value=0, step=1)
        end_row = st.number_input("Enter the ending row number (0-based index)", min_value=start_row+1, max_value=len(df), value=min(start_row+6312, len(df)), step=1)
        batch_size = st.number_input("Enter the number of rows to process in each batch", min_value=1, max_value=500, value=300, step=1)

        total_rows = min(end_row, len(df)) - start_row
        st.write(f"Processing {total_rows} rows in batches of {batch_size} rows...")

        if st.button("Process Titles"):
            result_df, batches_processed = process_excel(df, start_row, end_row, batch_size, input_column, model)
            st.write("Processing complete!")
            
            st.write("Processed batches:")
            for start, end in batches_processed:
                st.write(f"Rows {start} to {end}")
            
            st.write("Preview of processed data:")
            st.dataframe(result_df.head())

            # Save the result to a new Excel file
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                result_df.to_excel(writer, index=False)
            
            # Offer the new Excel file for download
            st.download_button(
                label="Download processed data as Excel",
                data=buffer.getvalue(),
                file_name="processed_titles.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Also offer CSV download
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download processed data as CSV",
                data=csv,
                file_name="processed_titles.csv",
                mime="text/csv",
            )
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Full error traceback:")
        st.error(traceback.format_exc())
else:
    st.warning("Please enter your Gemini API key to proceed.")