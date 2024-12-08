from typing import Dict
import re
import json




def add_to_db(data : Dict[str,str], table : str, cursor, conn) -> bool:
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
            
    
