import os
from PIL import Image
import streamlit as st
import json, logging, os, openai
from langchain import PromptTemplate
from src.qna_bot import QnABot

template = """



"""


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

def get_query():
    input_text = st.text_area(label="Input Query", height = 200, label_visibility='collapsed', placeholder="Your Query...", key="query")
    return input_text.strip()

#
def main():
    st.set_page_config(page_title="Unilever", page_icon="logo/1.png")
    
    col1,col2 = st.columns([1,10])

    with col1:
        # Load and display the image
        image = Image.open('logo/2.png')
        st.image(image, width=60)

    with col2:
        # Custom header with different font style and size
        header_text = "Next-Gen Recruitment: Unilever's Job Description Generating AI Tool Based on Custom Indexed data in Chat-GPT4"

        st.markdown(f"<h1 style='font-family: Arial, sans-serif; font-size: 13px;'>{header_text}</h1>", unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)

    # with col3:
    #     query_index = st.selectbox(
    #         'Select reference documents',
    #         ('Job Description','Legal Documents','UL_Docs', 'All', 'MSD','PPT','Multi')
    #     )
    
    st.markdown('### Enter your Query here:')
    
    query = get_query()
    submit_button = st.button("Submit")
    query_index = 'Job Description'
    print("query_index:", query_index)
    if query and submit_button:
        dbpath1 = os.path.join(os.getcwd(), query_index+'_v1')
        input_variable_names = ['query', 'context']
        input_variables = {
            'query': query,
            'context': '',
        }

        bot1 = QnABot(
            template=template,
            input_variable_names=input_variable_names,
            input_variables=input_variables,
            dbpath=dbpath1
        )

    
        
        responses = bot1.get_response()
        response = responses[0]
        message = responses[1]

        # Remove "Job Description" from each file path
        pdf_reference = [path.replace('Legal Documents\\', '') for path in message]

        if isinstance(response,str):
            #st.markdown(f''' :red[{response}]''')
            #st.write(response)
            st.markdown (response, unsafe_allow_html=True)
            st.markdown("""  """)
            st.markdown(f''' :red[References: ] :blue[{pdf_reference}] ''')
            st.markdown("""  """)
            st.markdown(f'''  :blue[Legal Documents generated by this tool may require further manual tuning from Buisness Perspective]''')
            
        elif isinstance(response,list):
            if len(response)>1:
                st.markdown(f''':red[Multiple sources of information are present. Please be more specific.]''')
                st.markdown("""---""")
            for items in response:
                file_name = items["source"].split('\\')[-1]
                st.markdown(f''' :red[Citation:] :blue[{file_name}] ''')
                st.markdown(items["answer"][0])
                st.markdown("""---""")
        else:
            st.markdown(f''':red["Internal error, try running query again"]''')
        
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
    main()
