import os, logging, openai, json
from llama_index import SimpleDirectoryReader
from langchain.document_loaders import UnstructuredPowerPointLoader,DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
logging.info('Code running from: {}'.format(ROOT_DIR))

with open(os.path.join(ROOT_DIR, 'config.json'), 'r') as jsonfile:
    config = json.load(jsonfile)
oai_base = config['openai']['base']
oai_key = config['openai']['key']
oai_ver = config['openai']['version']
oai_type = config['openai']['type']

openai.api_type = oai_type
openai.api_key = oai_key
openai.api_base = oai_base
openai.api_version = oai_ver




path = 'Job Description'


print("started ===>")
# loader = DirectoryLoader(path, glob="**/*.pdf")
loader = DirectoryLoader(f'./{path}/',glob = "./*.p*")

# loader = DirectoryLoader(f'./{path}/',glob = "./*.pptx",loader_cls=UnstructuredPowerPointLoader)

documents = loader.load()

# print("documents=>>>",documents[0].metadata)
# text_splitter1 = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
text_splitter1 = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=100)
docs1 = text_splitter1.split_documents(documents)
print("docs1===>", docs1)

# text_splitter2 = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
# docs2 = text_splitter2.split_documents(documents)


# docs_index_v1 chunksize 500 overlap 100
# docs_index_v2 chunksize 800 overlap 100
embeddings = OpenAIEmbeddings(openai_api_key = oai_key, engine = 'text-embedding-ada-003')

# docsearch1 = Chroma.from_texts(docs1, embeddings, metadatas=[{"source": str(i)} for i in range(len(docs1))])
# docsearch2 = Chroma.from_texts(docs2, embeddings, metadatas=[{"source": str(i)} for i in range(len(docs2))])

# metadatas=[{"source": str(i)} for i in docs1]
# print("metadatas",metadatas)

db1 = FAISS.from_documents(docs1, embeddings  )
db1.save_local(path+"_v1")

# db2 = FAISS.from_documents(docs2, embeddings )
# db2.save_local(path+"_v2")

print("completed ===>")


