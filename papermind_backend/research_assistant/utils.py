import fitz  
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from django.conf import settings

def get_embedding_from_text(text: str) -> list[float]:
    embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=settings.GENAI_API_KEY)
    return embedder.embed_query(text)


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text
