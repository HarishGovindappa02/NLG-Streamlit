import os
import streamlit as st
from src.qna_bot import QnABot

template = """
    You are an AI assistant whose job is to help call center agents help resolve customer queries
    you'll be provided with customer query, context, instructions and response length to create response.

    example of instructions are:
    - step by step: provide all the steps of the procedure queried upon in bullet points
    - tabular: generate output in tabular format
    
    example of response length:
    - details: generate response in 50 or more words
    - summary: generate respose in less than 50 words

    Please provide response relevant to the query if you find it in the context provided, otherwise just say
    "I didn't find response in the context, please ask relevant question or be specific about what you want"

    Here is the query, context, instruction and response length:
    QUERY: {query}, {suffix}
    CONTEXT: {context}
    INSTRUCTION: {instruction}
    RESPONSE LENGTH: {response_length}

    YOUR RESPONSE:
"""

introduction = """
Hi, I am a question answering bot, my job is to assist you in resolving customer queries.
Just put the user query in the box below and i'll find the relevant response and give it 
to you. Be specific with what you put in query box to help me find the best answer for you.

for example, if customer has a query regarding cancelling the insurance policy. you can ask:
\n`what are the steps of cancelling insurance policy?`
"""

os.environ['OPENAI_API_KEY'] = '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'


def get_query():
    input_text = st.text_area(label="Input Query", label_visibility='collapsed', placeholder="Your Query...", key="query")
    return input_text


st.set_page_config(page_title="QnA Bot", page_icon=":robot:")
st.header("QnA Bot")
st.markdown(introduction)

col1, col2, col3 = st.columns(3)
with col1:
    instructions = st.selectbox(
        'Select type of response',
        ('step by step', 'tabular'))
    
with col2:
    response_length = st.selectbox(
        'Select response length',
        ('Summary', 'Deatailed'))
    
with col3:
    query_suffix = st.selectbox(
        'Select query suffix',
        ('', 'Answer', 'Summarize')
    )

st.markdown('### Enter your Query here:')
query = get_query()

if query:
    dbpath1 = os.path.join(os.getcwd(), 'docs_index_v1')
    dbpath2 = os.path.join(os.getcwd(), 'docs_index_v2')
    input_variable_names = ['query', 'suffix', 'context', 'instruction', 'response_length']
    input_variables = {
        'query': query,
        'suffix': query_suffix,
        'context': '',
        'instruction': instructions,
        'response_length': response_length
    }
    bot1 = QnABot(
        template=template,
        input_variable_names=input_variable_names,
        input_variables=input_variables,
        dbpath=dbpath1
    )
    bot2 = QnABot(
        template=template,
        input_variable_names=input_variable_names,
        input_variables=input_variables,
        dbpath=dbpath2
    )

    response1, response2 = st.columns(2)

    with response1:
        st.markdown('### Response 1')
        st.write(bot1.get_response())

    with response2:
        st.markdown('### Response 2')
        st.write(bot2.get_response())