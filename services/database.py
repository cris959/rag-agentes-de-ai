import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
DB_FAISS_PATH = "vectorstore/db_faiss"
DOCS_DIR = "documentos"

def inicializar_base_conocimiento():
    """Carga el índice FAISS desde el disco o lo crea procesando los PDFs."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    if os.path.exists(DB_FAISS_PATH):
        print("💾 [SERVICES - DATABASE] Cargando índice FAISS existente desde el disco...")
        db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
        return db.as_retriever(search_kwargs={"k": 2})
    
    print("✨ [SERVICES - DATABASE] Creando base vectorial desde los PDFs...")
    if not os.path.exists(DOCS_DIR) or len(os.listdir(DOCS_DIR)) == 0:
        os.makedirs(DOCS_DIR, exist_ok=True)
        raise FileNotFoundError(f"❌ Meté tus archivos PDF en la carpeta '{DOCS_DIR}' antes de iniciar.")
        
    loader = PyPDFDirectoryLoader(DOCS_DIR)
    documentos = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    fragmentos = text_splitter.split_documents(documentos)
    
    db = FAISS.from_documents(fragmentos, embeddings)
    db.save_local(DB_FAISS_PATH)
    print(f"✅ [SERVICES - DATABASE] Índice persistido en '{DB_FAISS_PATH}'.")
    
    return db.as_retriever(search_kwargs={"k": 2})

# Exponemos el retriever listo para usar
retriever = inicializar_base_conocimiento()