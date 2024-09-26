import pandas as pd
from PIL import Image
import io
import base64
import json
from langchain_anthropic import ChatAnthropic

def process_lieferschein_response(response):
    result = response.content.strip()
    try:
        # Assuming the model returns a JSON string with table data
        table_data = json.loads(result)
        return table_data
    except json.JSONDecodeError:
        print(f"Failed to parse JSON: {result}")
        return {"error": "Failed to parse JSON", "raw_response": result}

def process_lieferschein_image(image_bytes, anthropic_api_key):
    image = Image.open(io.BytesIO(image_bytes))
    image = image.resize((1024, 1024)).convert("RGB")  # Resize the image to 1024x1024 pixels and convert to RGB
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

    llm = ChatAnthropic(anthropic_api_key=anthropic_api_key, model="claude-3-opus-20240229")
    
    system_message = {
        "role": "system", 
        "content": """You are an expert in extracting information from Lieferschein (delivery note) images. 
        Your task is to analyze the image of a Lieferschein and extract the relevant information into a structured table format. 
        Focus on details such as item descriptions, quantities, prices, dates, and any other relevant information typically found on a Lieferschein. 
        Return the extracted data as a JSON object representing a table, where each key is a column name and its value is a list of entries for that column Do not add any comments just return the json without any further information."""
    }
    
    user_message = {
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": base64_image,
                },
            },
            {
                "type": "text",
                "text": "Please extract the table data from this Lieferschein image and return it as a JSON object."
            }
        ],
    }
    
    response = llm.invoke(input=[system_message, user_message])
    return process_lieferschein_response(response)
