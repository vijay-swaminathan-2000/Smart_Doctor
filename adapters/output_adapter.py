from adapters.mysql_adapter import insert_data

def persist_generated_responses(smart_doctor_responses):
    sql_query: str = "INSERT into smart_doctor_answer (qid, answer) VALUES (%s, %s)"
    insert_data(sql_query, smart_doctor_responses)