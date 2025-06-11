from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import uuid
from langchain_pinecone import PineconeVectorStore

#Extract data from the PDF
def load_pdf(data):
    loader = DirectoryLoader(data,
                    glob="*.pdf",
                    loader_cls=PyPDFLoader)
    
    documents = loader.load()

    return documents


#Split the text into smaller chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 20)
    text_chunks = text_splitter.split_documents(extracted_data)

    return text_chunks

#download the model from the HuggingFace hub
def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings

def from_texts(texts, embedding, index_name, batch_size=32, text_key="text"):
    index = pc.Index(index_name)  # connect to the index

    for i in range(0, len(text_chunks), batch_size):
        i_end = min(i + batch_size, len(text_chunks))
        lines_batch = [text.page_content for text in text_chunks[i:i_end]]

        ids_batch = [str(uuid.uuid4()) for _ in range(i, i_end)]

        embeds = embedding.embed_documents([doc for doc in lines_batch])


        metadata = [{} for _ in range(i, i_end)]

        for j, line in enumerate(lines_batch):
            metadata[j][text_key] = line

        to_upsert = zip(ids_batch, embeds, metadata)

        index.upsert(vectors=list(to_upsert))
    return PineconeVectorStore(pc.Index(index_name), embeddings, text_key, namespace=None)