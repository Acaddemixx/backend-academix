import os
from dotenv import load_dotenv
import google.generativeai as gemini_embedder

load_dotenv()
GOOGLE_API_KEY = os.getenv('GEMNI_API_KEY') 


#this is a method that makes embeddings/the vectors 
def embed(object):
    result = (gemini_embedder.embed_content(
        model="models/embedding-001",
        content= object,
        task_type="retrieval_document",))
    
    return result['embedding']