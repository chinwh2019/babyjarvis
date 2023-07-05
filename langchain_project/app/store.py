import os 

from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
import pickle


# create the vectorstore and save it to a pickle file
def create_store():
    loader = DirectoryLoader(
        './FAQ', glob='**/*.txt', loader_cls=TextLoader, show_progress=True
    )
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
    )

    documents = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY'))
    
    vectorstore = FAISS.from_documents(documents, embeddings)

    with open('vectorstore.pickle', 'wb') as f:
        pickle.dump(vectorstore, f)



# load the vectorstore from the pickle file
def get_vectorstore():
    with open('vectorstore.pickle', 'rb') as f:
        vectorstore = pickle.load(f)
    return vectorstore