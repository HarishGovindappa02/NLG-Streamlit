import os
from src.qna_bot import QnABot
from flask import *

app = Flask(__name__)

template = """
        understand the following context:
        CONTEXT: {context}
        ---------------------------
        here is the input query:
        INPUT QUERY: {query}, {suffix}
        for the above INPUT QUERY and the CONTEXT provide the answer in the following format: {response_type}
        also format your answers as a markdown text
    """
# """
#         if an only if you don't find answer in the context just say "Following response is not from the given documents:"
#         followed by your answer formatted in markdown
# """

@app.route('/v1', methods=['GET', 'POST'])
def response():
    data = request.get_json()
    dbpath1 = os.path.join(os.getcwd(), data['query_index']+'_v1')
    input_variable_names = ['query', 'suffix', 'context', 'response_type']
    input_variables = {
        'query': data['query'],
        'suffix': data['query_suffix'],
        'context': '',
        'response_type': data['response_type']
    }
    bot1 = QnABot(
        template=template,
        input_variable_names=input_variable_names,
        input_variables=input_variables,
        dbpath=dbpath1
    )

    response = {'response': bot1.get_response()}

    return json.dumps(response)

@app.route('/v2', methods=['GET', 'POST'])
def alternate_response():
    data = request.get_json()
    dbpath2 = os.path.join(os.getcwd(), data['query_index']+'_v2')
    input_variable_names = ['query', 'suffix', 'context', 'response_type']
    input_variables = {
        'query': data['query'],
        'suffix': data['query_suffix'],
        'context': '',
        'response_type': data['response_type']
    }
    bot2 = QnABot(
        template=template,
        input_variable_names=input_variable_names,
        input_variables=input_variables,
        dbpath=dbpath2
    )

    response = {'response': bot2.get_response()}

    return json.dumps(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(port=5000, debug=True)
