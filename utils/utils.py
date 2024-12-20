from typing import Dict
import re
import json
import pandas as pd



def add_to_db(data : Dict[str,str | float], table : str, cursor, conn) -> bool:
    """
    Function to add record to db
    
    # Args:
        data : Dict[str,str | float] ->Dictionary contains data to add to db
        table : str -> Name of table in db
        cursor -> DB object to execute SQL Query
        conn -> connection with db
        
    # Return:
    bool 
        'True' if data was succesfully addded in db
        'False' is error occured
    """
    query = f"""
    INSERT INTO {table} (date,price,company,category)
    VALUES ('{data['date']}',{data['price']},'{data['company']}','{data['company_category']}');
    """
    try:
        cursor.execute(query)
        conn.commit()
        return True
    except Exception as e:
        print(str(e))
        return False


def extract_json(response : str) -> Dict[str,str|float] | None:
    """"
    Function to extract json from llama response
    
    # Args:
        response : str -> whole llama resposne
    
    # Return:
        Dict[str,str|float] if data was succesfully extracted, otherwise None
    """
    
    json_pattern = r'(\{.*\})'
    match = re.search(json_pattern, response, re.DOTALL)

    if match:
        json_str = match.group(0)
        
        try:
            data = json.loads(json_str)
            return data

        except json.JSONDecodeError as e:
            return None
    else:
        return None
    
    
def load_db_to_df(table: str, conn) -> pd.DataFrame:
    """
    Function to load db table to pandas dataframe
    
    # Args:
        table :str -> name of table in db
    
    # Return:
        DataFrame object
    """
    
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn, index_col='id', parse_dates=['date'])
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    return df
        

def delete_record(record_id : str, table: str, conn, cursor) -> bool:
    """
    Function to validate record_id if is a number 
    if valid calling a function to delete record from database
    
    # Args:
        record_id : str -> user input
        table : str -> Name of table in db
        cursor -> DB object to execute SQL Query
        conn -> connection with db
        
    # Return:
    bool 
        'True' if record was succesfully deleted
        'False' is error occured
    """
    
    try : 
        record_id = int(record_id)
        delete_record_from_db(record_id, table, conn, cursor)
        return True
    except (ValueError, IndexError):
        print('error')
        return False
    
    
def delete_record_from_db(record_id : int, table : str ,conn, cursor) -> None:
    """
    Function to execute query to delete record from database 
    
    # Params :
    record_id :int -> id number of a record to delete
    table :str -> name of a table in db
    conn -> connection with db
    cursor -> DB object to execute SQL Query
    """
    
    query = f"""
    DELETE FROM {table} WHERE id = {record_id}
    """
    
    cursor.execute(query)
    conn.commit()
