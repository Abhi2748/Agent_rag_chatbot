import faiss
import os
import pickle
from dotenv import load_dotenv
load_dotenv()

VECTORSTORE_PATH = 'vectorstore/faiss.index'
META_PATH = 'vectorstore/meta.pkl'

def save_faiss_index(index, metadata):
    faiss.write_index(index, VECTORSTORE_PATH)
    with open(META_PATH, 'wb') as f:
        pickle.dump(metadata, f)

def load_faiss_index():
    if not os.path.exists(VECTORSTORE_PATH):
        return None, None
    index = faiss.read_index(VECTORSTORE_PATH)
    with open(META_PATH, 'rb') as f:
        metadata = pickle.load(f)
    return index, metadata 