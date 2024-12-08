import streamlit as st
from PIL import Image
import torch
import psycopg2
from ollama import chat
from ollama import ChatResponse
import os 
from dotenv import load_dotenv
from utils.utils import add_to_db, extract_json
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
import aisuite as ai
from utils.process_receipt import preprocess_page
from utils.analytics import analytics_page
from utils.ai_assistant import assistant_page
import aisuite as ai

load_dotenv()

connection_params = {
    "dbname": os.getenv("DBNAME"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),        
}



try:
    conn = psycopg2.connect(**connection_params)  
    cursor = conn.cursor()
    
    st.set_page_config(
    page_title="FinanceAI",
    page_icon="💸",
    layout="wide",
)

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose page : ", ["📤 Read receipt", "📋 Database", "🤖 AI Assistant"])
    
    if page == "📤 Read receipt":
        preprocess_page(table=os.getenv("TABLE"), cursor=cursor, conn=conn)

    if page == "📋 Database":
        analytics_page(table=os.getenv("TABLE"),conn=conn)
        
    if page == "🤖 AI Assistant":
        assistant_page(table=os.getenv("TABLE"),conn=conn)

except psycopg2.Error as e:
    st.title("Error connecting to the database:", e)



