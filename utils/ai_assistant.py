import streamlit as st
import pandas as pd 
import aisuite as ai
import datetime
from typing import Tuple

def assistant_page(table : str, conn):
    """
    Function to load assistant page with UI and functions
    """
    df = load_csv(table,conn)
    acc_month, sum_monthly, mean_monthly = prepare_statistics(df)
    
    col1, col2 = st.columns([9,1])
    
    with col1:
        st.title("🤖 Assistant")    
    
    with col2:
        if st.button("🗑 Clear"):
            st.session_state.messages = [
                {"role": "system", "content": f"""You are an experienced data analytics professional, 
                 you have 3 basic statistics from the database: the current month : {acc_month} - the sum of money spent, data from the last 6 months grouped by month with the sum of money spent : {sum_monthly} and 
                 data from the last 6 months grouped by month with the average of money spent : {mean_monthly}. Based on these statistics, answer questions, predict and analyze other statistics """}
            ]
    
    for i in range(2):
        st.write(" ")
    
    client = ai.Client()
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": f"""You are an experienced data analytics professional, 
                 you have 3 basic statistics from the database: the current month : {acc_month} - the sum of money spent, data from the last 6 months grouped by month with the sum of money spent : {sum_monthly} and 
                 data from the last 6 months grouped by month with the average of money spent : {mean_monthly}. Based on these statistics, answer questions,  predict and analyze other statistics """}
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
    """
    Function to generate Llama resposne 
    
    # Args: 
        client : connection with llama model
        
    # Return: 
        str : llama response
    """
    response = client.chat.completions.create(model='ollama:llama3.2', messages=st.session_state.messages,temperature=0.75)
    
    return response.choices[0].message.content


def load_csv(table : str, conn) -> pd.DataFrame:
    """
    Funtion to get all data from given table to pandas Dataframe object
    
    # Args:
        table: str -> name of the table 
        conn -> connection with db
    
    # Return:
        Dataframe object
    """
    
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn, index_col='id', parse_dates=['date'])
    return df
    
    
def prepare_statistics(df : pd.DataFrame) -> Tuple[float,pd.Series,pd.Series]:
    """
    Function to get 3 basics statiscics from user's database
    Containts : 
    Calculating sum and mean of money spent in last 6 month
    Sum of money spent in current month
    
    # Args:
        df : pd.DataFrame -> loaded db into dataframe
        
    # Return:
        Tuple containing calculated statistics
    """
    start_date = datetime.datetime.now() - datetime.timedelta(days=180)

    df = df[df['date'] > pd.to_datetime(start_date)].sort_values(by=['date'])
    df['Month'] = df['date'].dt.month_name()
    sum_monthly = df.groupby('Month')['price'].sum()
    mean_monthly = df.groupby('Month')['price'].mean()
    acc_month = df[df['Month'] == datetime.datetime.now().strftime('%B')]['price'].sum()

    return acc_month, sum_monthly, mean_monthly