# Lieferschein to Table Converter

This Streamlit app converts images of Lieferschein (delivery notes) into tabular data that can be viewed and downloaded as CSV files.

## Setup

1. Ensure you have Python installed on your system.

2. Clone this repository or download the source code.

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your Anthropic API key as an environment variable. You can do this in one of two ways:

   a. Set it temporarily in your terminal:
      ```
      export ANTHROPIC_API_KEY="your_api_key_here"
      ```
      Replace "your_api_key_here" with your actual Anthropic API key.

   b. Add it to your shell configuration file (e.g., .bashrc, .zshrc):
      ```
      echo 'export ANTHROPIC_API_KEY="your_api_key_here"' >> ~/.bashrc
      ```
      Replace "your_api_key_here" with your actual Anthropic API key and ~/.bashrc with the path to your shell configuration file if different.

## Running the App

1. Navigate to the project directory in your terminal.

2. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

3. Open a web browser and go to the URL provided by Streamlit (usually http://localhost:8501).

## Using the App

1. Upload a Lieferschein image using the file uploader on the app's interface.

2. Click the "Convert to Table" button to process the image and extract the table data.

3. Review the extracted table displayed on the page.

4. Use the "Download CSV" button to download the extracted data as a CSV file.

## Troubleshooting

- If you encounter an error message about the ANTHROPIC_API_KEY not being set, make sure you've correctly set up the environment variable as described in the Setup section.

- If you face any issues with image processing or data extraction, ensure that the uploaded image is clear and contains a typical Lieferschein layout.

For any other issues or questions, please refer to the Streamlit and Anthropic API documentation or contact the app maintainer.