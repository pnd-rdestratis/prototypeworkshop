import streamlit as st
import pandas as pd
from query_iptc import process_lieferschein_image
import os

st.set_page_config(page_title="Lieferschein to Table Converter")
st.sidebar.title("How to Use")
st.sidebar.write("""
1. Upload an image of a Lieferschein (delivery note) using the file uploader.
2. Click the 'Convert to Table' button to extract the table from the Lieferschein.
3. The extracted table will be displayed.
4. Click the 'Download CSV' button to download the table as a CSV file.
""")
st.image("logo.png", width=150)
st.title('Lieferschein to Table Converter')

uploaded_image = st.file_uploader("Upload Lieferschein image:", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    if st.button('Convert to Table'):
        anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]
        if not anthropic_api_key:
            st.error("ANTHROPIC_API_KEY is not set. Please set the environment variable and restart the app.")
        else:
            with st.spinner('Converting Lieferschein to table...'):
                image_bytes = uploaded_image.getvalue()
                try:
                    table_data = process_lieferschein_image(image_bytes, anthropic_api_key)
                    
                    st.write("Extracted data:", table_data)  # Debug: Print extracted data
                    
                    # Handle potential inconsistencies in data
                    if isinstance(table_data, list):
                        # If table_data is a list of lists (rows)
                        max_length = max(len(row) for row in table_data)
                        padded_data = [row + [None] * (max_length - len(row)) for row in table_data]
                        df = pd.DataFrame(padded_data)
                    elif isinstance(table_data, dict):
                        # If table_data is a dictionary (columns)
                        df = pd.DataFrame({col: pd.Series(data) for col, data in table_data.items()})
                    else:
                        raise ValueError("Unexpected data format")
                    
                    st.success('Conversion complete!')
                    
                    # Display the table
                    st.subheader("Extracted Table")
                    st.dataframe(df)
                    
                    # Add download button
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="lieferschein_table.csv",
                        mime="text/csv",
                    )
                except Exception as e:
                    st.error(f"An error occurred during processing: {str(e)}")
                    st.write("Data causing the error:", table_data)  # Debug: Print problematic data
else:
    st.info("Please upload a Lieferschein image to convert to a table.")
