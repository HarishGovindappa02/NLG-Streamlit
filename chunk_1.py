import openai
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize
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
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize

def extract_text_from_pdf(pdf_paths):
    texts = []
    for pdf_path in pdf_paths:
        try:
            pdf_file = open(pdf_path, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()

            pdf_file.close()
            texts.append(text)
        except Exception as e:
            print(f"Error while extracting text from {pdf_path}: {e}")
    #print("TEXTS:", text)
    return texts

def chunk_text_into_sentences(texts):
    # Download and update the Punkt tokenizer models
    nltk.download('punkt')

    # Tokenize the texts into sentences
    all_sentences = []
    for text in texts:
        sentences = sent_tokenize(text)
        all_sentences.extend(sentences)
    #print("ALL SENTENCE:", all_sentences)
    return all_sentences


import openai

def generate_sections_with_gpt4(sentences, query):
    chunk_size = 1500
    chunked_text = [sentences[i:i + chunk_size] for i in range(0, len(sentences), chunk_size)]

    # Generate responses for each chunk
    responses = []
    for chunk in chunked_text:
        context = "\n".join(chunk)
        role = query

        #print("role:", role)

        # Prepare the message list for the Chat API
        content1 = f"""
        You are an AI assistant that helps people to create job descriptions 
        for given role in triple single quotes based on multiple job descriptions 
        delimited using triple backticks.Format Job Description as html markdown using small blue headers and bullet points and donot change the role{role}.    
        Multiple Job Descriptions: ```{context}```       
        Role: '''{role}'''     
        Think through each section of all the multiple job descriptions 
        and prepare each section for given role by using relevant information.
        Final job descripion should have all the sections in both descriptions exactly once in the response.
        There should not be any duplicate sections.      
        Add About Unilever, About Uniops headers after Location and keep the same pattern.        
        Job Description for {role}
        """
       

        messages = [{"role": "assistant", "content": content1}]
                # Make the API call with the Chat API
        response = openai.ChatCompletion.create(
            engine="gpt-4-32k",
            messages=messages,
            temperature=0,
            max_tokens=4500,
            top_p=0,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

        responses.append(response['choices'][0]['message']['content'])

    #Join the responses back into a single string
    full_response = "\n".join(responses)
    # messages = [
    #                 {"role": "assistant", "content": f"Job Description: {full_response}"},
    #                 {"role": "assistant", "content": "Format the output as HTML markdown with small blue headers."}
    #             ]
    #     # Make the API call with the Chat API
    # response = openai.ChatCompletion.create(
    #     engine="gpt-4",
    #     messages=messages,
    #     temperature=0,
    #     max_tokens=7000,
    #     top_p=0,
    #     frequency_penalty=0,
    #     presence_penalty=0,
    #     stop=None
    # )

    # return response['choices'][0]['message']['content']
    
    return full_response




def mainToResponse(pdf_path, query):
    text = extract_text_from_pdf(pdf_path)
    sentences = chunk_text_into_sentences(text)
    sections = generate_sections_with_gpt4(sentences, query)
    return sections
    

    print("sections:", sections)

if __name__ == "__main__":
    pdf_path = ""
    query = ''
    mainToResponse(pdf_path, query)
