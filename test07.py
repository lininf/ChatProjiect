import string
import streamlit as st
import random

import sys

from dotenv import load_dotenv
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI




# 使大模型具有记忆
def get_airesponse(user_propmt):
    load_dotenv()
    model = ChatOpenAI(
        model='gpt-4o-mini',
        api_key = st.session_state['API_KEY'],
        # api_key = st.secrets['API_KEY'],
        base_url='https://twapi.openai-hk.com/v1'
    )
    chain  =ConversationChain(llm=model,memory=st.session_state['memory'])
    return chain.invoke({'input':user_propmt})['response']


st.title('#我的ChatGPT')

with  st.sidebar:
    api_key = st.text_input('请输入你的key:',type='password')
    st.session_state['API_KEY'] = api_key


#session_state全局的字典
if 'messages' not in st.session_state:
    #创建会话对话列表
    st.session_state['messages'] =[{'role':'ai','content':'你好主人，我是你的AI助手，我叫小美'}]
    st.session_state['memory'] = ConversationBufferMemory(return_message=True)

#把所有内容显示在窗口上
for message in st.session_state['messages']:
    role , content = message['role'], message['content']
    st.chat_message(role).write(content)



user_input = st.chat_input()
if user_input:
    # if not api_key:
    #     st.info('请输入自己专属的key！！！')
    #     st.stop()
    st.chat_message('human').write(user_input)
    #追加human绘画列表
    st.session_state['messages'].append({'role':'human','content':user_input})
    with st.spinner('AI正在思考，请等待.....'):
        resp_from_ai = get_airesponse(user_input)
        st.session_state['history'] = resp_from_ai
        st.chat_message('ai').write(resp_from_ai)
        st.session_state['messages'].append({'role':'ai','content':resp_from_ai})

