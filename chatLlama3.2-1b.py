import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate, ChatPromptTemplate

st.title("Chatbot using OllamaLlama 3.2:1b 💬")
st.write("Github Repository: https://github.com/kderrylo/Chatbot-with-Olama-Llama-3.2-1b")

model = ChatOllama(model="llama3.2:1b", base_url="http://localhost:11434") # load model dari ollama

# spesifikasi interaksi dengan AI assistant
system_message = SystemMessagePromptTemplate.from_template("You are AI assistant, explain things in 1 sentence")

# atur state untuk history chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
def history():
    chat_history = [system_message]
    for chat in st.session_state.chat_history:
        chat_history.append(HumanMessagePromptTemplate.from_template(chat['user']))
        chat_history.append(AIMessagePromptTemplate.from_template(chat["assistant"]))
    return chat_history

# buat form
with st.form("form"):
    input = st.text_area("Input your text/prompt here 👇👇 !", key="user_input")
    button = st.form_submit_button("Enter")

# AI response generation
def response_generate(chat_history):
    chat_template = ChatPromptTemplate.from_messages(chat_history)
    # model_response = model.invoke(chat_template)
    model_response = chat_template|model|StrOutputParser()
    return model_response.invoke({})
    # chain = chat_template | model | StrOutputParser()
    # return chain.invoke({})

if input and button:
    with st.spinner("Thinking . . . 🤔💭"):
        chat_history = history()
        
        chat_history.append(HumanMessagePromptTemplate.from_template(input))

        response = response_generate(chat_history)
        if response:
            st.session_state.chat_history.append({
                "user":input,
                "assistant":response
            })

st.write("---")
st.write("### Chat History ⏳")
for chat in reversed(st.session_state["chat_history"]):
    st.write(f"😃 You : {chat['user']}")
    st.write(f"🤖  AI : {chat['assistant']}")
    st.write("---")



