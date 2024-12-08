import streamlit as st
from utils.utils import add_to_db, extract_json
from ollama import chat
from ollama import ChatResponse
from typing import Dict


def preprocess_page(table : str, cursor, conn) -> None:
    st.title("📤 Wgraj plik i dodaj dane")
    
    uploaded_file = st.file_uploader(label=" ", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
    
        col1, col2 = st.columns(2)
    
        with col1:
            st.image(uploaded_file, width=600)

            colu1, colu2 = st.columns([1,4])
            
            for i in range(3):
                st.write(" ")
            
            with colu1:
                if st.button("Extract data 🛠"):
                    with st.spinner('Processing...'):
                        try:
                            # response: ChatResponse = chat(model='llama3.2-vision', messages=[{
                            #         'role': 'user',
                            #         'content': """
                            #                 From the given image, return the information in JSON format WITHOUT ADDITIONAL TEXT, including {price, date, company, company_category}. 
                            #                 If any of these elements are not found in the image, record them as NULL. If the company_category cannot be found by the company name, determine it based on the shopping list.
                            #         """,
                            #         'images' : [uploaded_file.getvalue()]
                            #     }])

                            st.session_state['response'] = '{"price" : 50.0, "date" : null, "company" : "Alelgro"}'
                            # st.session_state['response'] = response.message.content
                        except Exception as e:
                            st.error("Error occured while processing image. Try again!")
            
            with colu2:
                if st.button("Clear 🗑"):
                    if 'response' in st.session_state:
                        del st.session_state['response']
            
        if 'response' in st.session_state:
            with col2:
                data = extract_json(st.session_state['response'])
                if data is not None:                   
                    show_extracted_data(data, table, cursor, conn)
 
         
        
def show_extracted_data(data : Dict[str,str | int], table, cursor, conn) -> None :
    st.title("Extracted data :")
    data['price'] = st.number_input("Price", min_value=0.00, value=data.get("price",None))
    data['date'] = st.date_input("Date", value=data['date'] if data['date'] else "default_value_today")
    data['company'] = st.text_input("Company", value=data.get('company', None))
    data['company_category'] = st.text_input("Category", value=data.get('company_category', None))
    
    if st.button("Add to database"):
        if add_to_db(data, table, cursor, conn):
            st.success("Added to database! 🎈")