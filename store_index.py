from src.helper import load_pdf, text_split, download_hugging_face_embeddings, from_texts
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os


load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

extracted_data = load_pdf("data/")
text_chunks = text_split(extracted_data)
embeddings= download_hugging_face_embeddings()

pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "medical-chatbot"
# Create an index if it doesn't exist (example for serverless spec)
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name='medical-chatbot',
        dimension=384,
        metric='euclidean'
    )

docsearch= from_texts(text_chunks, embeddings, index_name=index_name)
