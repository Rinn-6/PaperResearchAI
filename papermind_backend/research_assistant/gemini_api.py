import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GENAI_API_KEY"))

def summarize_text(text):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(f"Summarize this research paper:\n{text}")
    return response.text

def extract_insights(text):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(f"Extract key insights from this research paper:\n{text}")
    return response.text

def generate_citation(text, format="APA"):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(f"Generate a {format} citation for this research paper:\n{text}")
    return response.text
