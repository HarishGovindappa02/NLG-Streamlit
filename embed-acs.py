import os, json, logging
import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import AzureSearch



# Load environment variables from a .env file using load_dotenv():


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
model: str = "gpt-4"

vector_store_address: str = "nMepdQ0hZVw4bhQAjGcnGasSBFcYVJz3BV70grqVRTAzSeCjeOP6"
vector_store_password: str = "https://cognitive-search-genai.search.windows.net"
index_name: str = "index-nlg"


embeddings = OpenAIEmbeddings(model=model, chunk_size=1, openai_api_key = oai_key)
vector_store = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=vector_store_password,
    index_name=index_name,
    embedding_function=embeddings.embed_query,
)


from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredPowerPointLoader,DirectoryLoader

# path = 'PPT'
path = 'Job Description'
print("started ===>")


loader = DirectoryLoader(f'./{path}/',glob = "./*.p*")

documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
print("docs:", docs)
vector_store.add_documents(documents=docs)