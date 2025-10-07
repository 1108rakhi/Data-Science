# import openai
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json, re
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# for model in genai.list_models():
#     print(model.name)
def generate_descriptions(table_name : str, description : list[dict]):
    command = f"""
        As a description generator, generate business-friendly names and descriptions with around 300 char length for the 
        table name: {table_name} and return output as a JSON list like:
        [
          {{"column": "column_name", "business_name": "business name" ,"business_description": "business meaning"}}
        ]
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(command)
    cleaned_text = re.sub(r"^```json\s*|```$", "", response.text, flags=re.DOTALL)
    output_text = cleaned_text.strip()
    try:
        result = json.loads(output_text)
    except json.JSONDecodeError:
        result = json.loads(output_text.replace("'", '"'))

    return result       
    