import os
import re
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import openai
import gradio as gr
import pandas as pd

os.environ['OPENAI_API_KEY'] = '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'

class QnABot:
    def __init__(self, dbpath="ppt_index") -> None:
        self.embeddings = OpenAIEmbeddings()
        self.db = FAISS.load_local(dbpath, self.embeddings)

    def _get_summary_String(self, input_text):
        response_length_pattern = r'Brief|Short'
        if len(re.findall(response_length_pattern, input_text, re.IGNORECASE)) > 0:
            response_length = "in less than 50 words"
        else:
            response_length = "in 50 or more words"

        summary_pattern = r'Summar'
        if len(re.findall(summary_pattern, input_text, re.IGNORECASE)) > 0:
            summary_string = "genrating a summary {}".format(response_length)
        else:
            summary_string = "answering the questions {}".format(response_length)

        return summary_string

    def qnabot(self, input_text):
        summary_string = self._get_summary_String(input_text)
        results = self.db.similarity_search(input_text)
        context = ' '.join([doc.page_content for doc in results])
        system_prompt = "for the following context start {}: ".format(summary_string)
        
        response = openai.ChatCompletion.create(
                 model="gpt-3.5-turbo",
                messages=[
                {"role": "system", "content": system_prompt + context},
                {"role": "user", "content": input_text},
            ])
        
        message = response.choices[0].message.content
        bot_data = pd.DataFrame({'query':[input_text], 'context': [context], 'output': [message]})
        bot_data.to_csv('qna-bot-output.csv', mode='a', header=False, index=False)
        return message

bot = QnABot("faiss_index")
iface = gr.Interface(fn=bot.qnabot,
                     inputs=gr.inputs.Textbox(lines=7, label="Enter your text"),
                     outputs="text",
                     title="Custom-trained AI Chatbot")

iface.launch(share=True)