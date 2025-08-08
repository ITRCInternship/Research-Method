import json
import requests
import time
import re
from .config import VLLM_SERVER_URL, VLLM_MODEL_NAME
class Llm:
    def __init__(self):
        self.vllm_url = VLLM_SERVER_URL
        self.model = VLLM_MODEL_NAME

    
        
        
    def vllm_inference(self, user_message,system_message):
        start_time = time.time()
        prompt = [{"role": "user", "content": user_message},
                            {"role": "system", "content": system_message}]

        payload = {
            "model": self.model,
            "messages": prompt,  
            "temperature": 0.5,      
        }

        try:
            # Send a POST request to VLLM server
            response = requests.post(
                self.vllm_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )
     
            if response.status_code == 200:
                response_data = response.json()
                # print("status code is 200")
                end_time = time.time()  
        
                print(f"Time taken for inference: {end_time - start_time} seconds")
                return response_data
            else:
                print(f"Error in response data: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error : {e}")
            return None
                 
    def clean_text(self, content):
        cleaned_content = content.strip()                          # Remove leading/trailing spaces
        cleaned_content = re.sub(r'\n+', '\n', cleaned_content)    # Collapse multiple newlines
        cleaned_content = re.sub(r'\s+', ' ', cleaned_content)     # Optional: collapse all excessive spaces to single space
        cleaned_content = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned_content)  # Optional: remove Markdown bold **text**
        return cleaned_content