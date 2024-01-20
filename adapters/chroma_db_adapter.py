from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders.csv_loader import CSVLoader

print("Loading documents into Chroma...")
# load the document and split it into chunks
loader = CSVLoader("data/published_queries.csv")
published_queries_documents = loader.load()

# split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
split_documets = text_splitter.split_documents(published_queries_documents)

# create the open-source embedding function
embedding_function = HuggingFaceInstructEmbeddings(model_name="all-MiniLM-L6-v2")

print("Persisting documents into Chroma...")
# Persisting it into Chromadb
db = Chroma.from_documents(split_documets, embedding_function, persist_directory="./")
db.persist()