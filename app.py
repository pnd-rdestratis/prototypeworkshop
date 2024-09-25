import streamlit as st
import pandas as pd
from query_iptc import process_lieferschein_image
import os

st.set_page_config(page_title="Prototyp: Lieferschein zu Tabelle Konverter")
st.sidebar.title("How To")
st.sidebar.write("""
1. Lieferschein hochladen
2. Konvertieren
3. Tabelle runterladen
""")
st.image("logo.png", width=150)
st.title('Prototyp: Lieferschein zu Tabelle Konverter')

uploaded_image = st.file_uploader("Upload Lieferschein:", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    if st.button('Konvertieren'):
        anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]
        if not anthropic_api_key:
            st.error("ANTHROPIC_API_KEY is not set. Please set the environment variable and restart the app.")
        else:
            with st.spinner('Konvertiere Lieferschein zu Tabelle...'):
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
                    
                    st.success('Erledigt')
                    
                    # Display the table
                    st.subheader("Tabelle")
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
