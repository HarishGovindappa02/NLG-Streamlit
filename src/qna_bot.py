import os
import re
import json
import pickle
import pandas as pd
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from chunk_1 import mainToResponse


from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import messages_from_dict, messages_to_dict
from langchain.memory import ChatMessageHistory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT

from langchain.llms import OpenAI
import openai


import json, logging, os
from langchain import PromptTemplate

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

memory_file='memory.txt'
vectorstore='db1'
class QnABot:
    def __init__(self, template, input_variable_names, input_variables, dbpath="docs_index_v1") -> None:
        self.embeddings = OpenAIEmbeddings(openai_api_key = oai_key,engine = 'text-embedding-ada-002' )
        self._db = FAISS.load_local(dbpath, self.embeddings)
        self._input_variables = input_variables
        

    def get_response(self):
        input_query = self._input_variables['query']
        results = self._db.similarity_search_with_score(input_query)
        #message = results[2:].metadata["source"]# Top1 change to pick up 2
        last_two_metadata = [item[0].metadata["source"] for item in results[-2:]]
        message = last_two_metadata
        print("result===>>>",results)
        
        print("PFD SELECTED:-", message)
        pdf_message = [path.replace('\\\\', '/') for path in message]
        print("FINAL PFD SELECTED2:-", pdf_message)
        #else:
            #message = "I could not find the answer to the question in the reference."

        SendSource = mainToResponse(pdf_message, input_query)
        return SendSource, pdf_message

