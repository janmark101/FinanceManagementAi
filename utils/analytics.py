import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd



def analytics_page(table : str, conn):
    st.title("📋 Database")
    # colored_header("📋 Database",color_name="green-70")

    df = pd.read_sql_query(f"SELECT * FROM {table}", conn, index_col='id', parse_dates=['date'])
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    if not df.empty:
        st.dataframe(df, use_container_width=True)

        record_id = st.selectbox("Wybierz rekord do edycji/usunięcia", df.index)
        
        
        st.subheader("📊 Analiza danych")
        col1, col2 = st.columns(2)
        
        month, year = datetime.today().month, datetime.today().year
        

        with col1:
            st.subheader(f"Expenses in {datetime.today().strftime('%B')}")
            fig, ax = plt.subplots()
            filtered_df = df[(df['date'].dt.year==year) & (df['date'].dt.month==month)]
            filtered_df = filtered_df.groupby('date')['price'].sum()
            filtered_df.plot(kind='line', color='skyblue', marker='o', linestyle='-', linewidth=2)
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            st.pyplot(fig)

        with col2:
            df_filtered = df[df['date'] >= (datetime.today()-timedelta(days=150))]
            df_filtered['month'] = df_filtered['date'].dt.to_period('M')
            df_filtered = df_filtered.groupby('month')['price'].sum().reset_index()
            df_filtered['month'] = pd.to_datetime(df_filtered['month'], format='%Y-%m')
            print(df_filtered)
            st.subheader("Pole 1 - Liczność")
            fig, ax = plt.subplots()
            plt.bar(df_filtered['month'], df_filtered['price'], color='skyblue')
            ax.set_ylabel("")
            st.pyplot(fig)
    else:
        st.warning("Brak danych w bazie. Dodaj nowe rekordy na stronie '📤 Wgraj plik'.")