import datetime
from adapters.mysql_adapter import fetch_data

def get_questions():
    now = datetime.datetime.now()
    one_day_ago = now - datetime.timedelta(days=1)
    one_day_ago_str = one_day_ago.strftime('%Y-%m-%d %H:%M:%S')

    # Prepare SQL query string
    sql_query = f"""
    SELECT id, question
    FROM question
    WHERE parent_question_id = 0 AND
    (status = 'answered' OR status = 'new') AND
    created_at > '{one_day_ago_str}';
    """
    
    sql_results = fetch_data(sql_query)

    questions_from_past_day = [(row[0], row[1]) for row in sql_results]
    
    return questions_from_past_day
