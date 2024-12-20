import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from .utils import delete_record, load_db_to_df


plot_helper = {
    "Year" : 'Y',
    "Month" : "M",
    "Day" : "D"
}


def analytics_page(table : str, conn, cursor):
    """
    Function to load analytics page with functions to load db 
    """
    df = load_db_to_df(table=table, conn=conn)
    
    col1, col2 = st.columns([2,1])
    with col1:
        st.title("📋 Database")
    
    with col2:
        del_col1, del_col2, del_col3  = st.columns([2,1,2])
        with del_col1:
            record_id = st.text_input(label=" ", placeholder="Insert ID to delete")
        with del_col2:
            st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
            if st.button("Delete"):
                with del_col3:
                    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
                    if delete_record(record_id=record_id, table=table, conn=conn, cursor=cursor):
                        df = load_db_to_df(table=table, conn=conn)
                        st.success("Success 🎈")
                    else:
                        st.error("Try again! 😕")


    if not df.empty:
        st.dataframe(df, use_container_width=True)
       
        
        st.subheader("📊 Data analysis")
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
                if st.button("Generate Plot 📊", use_container_width=True):
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
        st.warning("Database is empty.")
        
        
        
