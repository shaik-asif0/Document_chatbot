from google import genai
import docx
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

load_dotenv()  
API_KEY = os.getenv("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# --- Function to read uploaded documents ---
def read_document(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        pdf = PdfReader(uploaded_file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])
    elif uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")
    else:
        return ""

def get_answer_from_doc(uploaded_file, question):
    doc_text = read_document(uploaded_file)
    prompt = f"Document:\n{doc_text}\n\nQuestion: {question}\nAnswer:"
    
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )
    return response.text
