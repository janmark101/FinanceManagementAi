import streamlit as st
import pandas as pd 
import aisuite as ai


def assistant_page(table : str, conn):
    
    col1, col2 = st.columns([9,1])
    
    with col1:
        st.title("🤖 Assistant")    
    
    with col2:
        if st.button("🗑 Clear"):
            st.session_state.messages = [
                {"role": "system", "content": "You are an experienced data analytics professional..."}
            ]
    
    for i in range(2):
        st.write(" ")
    
    client = ai.Client()
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are an experienced data analytics professional..."}
        ]
        
    containter = st.container()
        

    if prompt := st.chat_input("Say something"):
        st.session_state.messages.append({"role" : "user", "content" : prompt})
        
        response = ai_resposne(client)
        st.session_state.messages.append({"role" : "assistant", "content" : response})
    
        
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            containter.chat_message("user").write(msg['content'])
        elif msg['role'] == 'assistant':
            containter.chat_message("assistant").write(msg['content'])
        


def ai_resposne(client) -> str:
    # messages = [
    #     {"role" : "user", "content" : prompt}
    # ]

    response = client.chat.completions.create(model='ollama:llama3.2', messages=st.session_state.messages,temperature=0.75)
    
    return response.choices[0].message.content