import os
import time
from dotenv import load_dotenv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

# 1. Load Secrets immediately when this file is imported
load_dotenv()

def get_text_from_image(image_file):
    """
    Connects to Azure Computer Vision, sends the image, 
    and returns the extracted text string.
    """
    
    # --- A. Authentication ---
    API_KEY = os.getenv("AZURE_VISION_KEY")
    ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")

    if not API_KEY or not ENDPOINT:
        return "Error: Azure keys not found. Check .env file."

    # --- B. Client Setup ---
    client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

    try:
        # --- C. Send Image to Cloud ---
        # Azure needs a stream, and Streamlit provides a buffer. 
        # We pass 'raw=True' to get the operation ID.
        response = client.read_in_stream(image_file, raw=True)
        
        # Get the 'Operation-Location' from the response headers
        operation_location = response.headers["Operation-Location"]
        # Extract the ID from the URL (it's the last part)
        operation_id = operation_location.split("/")[-1]

        # --- D. Wait for Result (Async) ---
        # OCR takes a few seconds, so we must poll the server
        while True:
            result = client.get_read_result(operation_id)
            if result.status not in ['notStarted', 'running']:
                break
            time.sleep(1) # Wait 1 second before checking again

        # --- E. Extract Text ---
        if result.status == OperationStatusCodes.succeeded:
            extracted_text = []
            for text_result in result.analyze_result.read_results:
                for line in text_result.lines:
                    extracted_text.append(line.text)
            
            # Join all lines into one big string
            return "\n".join(extracted_text)
            
        else:
            return "Error: Azure failed to read the document."

    except Exception as e:
        return f"Error: {str(e)}"