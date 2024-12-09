import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go


plot_helper = {
    "Year" : 'Y',
    "Month" : "M",
    "Day" : "D"
}


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
        
        result = pd.DataFrame([], columns=['Period','price'])
        
        with col1:
            date_col1, date_col2 = st.columns(2)
            with date_col1:
                start_date = st.date_input("Start date")
                group_by = st.selectbox("Group by : ",
                                        options = ['Year','Month','Day'])
            with date_col2:
                end_date = st.date_input("End date")
                
                agg_fun = st.selectbox("Aggregate function : ",
                                       options=['Mean', 'Sum'])
            
 
            with date_col1:
                if st.button("Generate Plot 📊"):
                    filtered_df = df[(df['date'] >= pd.Timestamp(start_date)) & (df['date'] <= pd.Timestamp(end_date))]
                    
                    filtered_df['Period'] = filtered_df['date'].dt.to_period(plot_helper[group_by])
                    
                    if agg_fun == 'Mean':
                        result = filtered_df.groupby("Period")['price'].mean().reset_index()
                        
                    if agg_fun == 'Sum':
                        result = filtered_df.groupby("Period")['price'].sum().reset_index()
                    
                    result['Period'] = result['Period'].dt.to_timestamp()
            with date_col2:
                if result is not None:
                    st.dataframe(result, use_container_width=True)
            
            
        with col2:
            if result is not None:
                fig = go.Figure()

                fig.add_trace(go.Bar(
                    x=result["Period"], 
                    y=result["price"], 
                    marker=dict(color="#7F0F30"),
                    name="Money"
                ))

                fig.update_layout(
                    plot_bgcolor="rgb(14, 17, 23)", 
                    paper_bgcolor="rgb(14, 17, 23)",  
                    font=dict(color="white"),  
                    xaxis=dict( gridcolor="gray"),
                    yaxis=dict(title="Money", gridcolor="gray")
                )

                st.plotly_chart(fig, use_container_width=True)


    else:
        st.warning("Brak danych w bazie. Dodaj nowe rekordy na stronie '📤 Wgraj plik'.")