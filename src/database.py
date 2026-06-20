import psycopg2
from src.sql_validator import clean_sql
import sqlite3

def get_connection():

    conn = sqlite3.connect(

        "northwind.db"

    )

    return conn

def execute_sql(sql):

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return columns, rows
def execute_with_retry(question, sql, retry_chain, max_retries=2):

    retries = 0

    while retries <= max_retries:

        try:

            print("\nTrying SQL:\n")
            print(sql)

            columns, rows = execute_sql(sql)

            return sql, columns, rows

        except Exception as e:

            print("\nDatabase Error:\n")
            print(e)

            if retries == max_retries:

                raise ValueError(
                    "Unable to generate a valid query after multiple attempts."
                )

            error_message = str(e)

            sql = retry_chain.invoke({
                "question": question,
                "failed_sql": sql,
                "error_message": error_message
            })
            sql = clean_sql(sql)

            print("\nLLM Corrected SQL:\n")
            print(sql)

            retries += 1

from src.result_sanitizer import sanitize_results, handle_empty_results
if __name__ == "__main__":

    sql = """
    SELECT *
    FROM products
    WHERE product_name = 'XYZ'
    LIMIT 5;
    """

    columns, rows = execute_sql(sql)
    if len(rows) == 0:
        print(handle_empty_results())
    else:
        columns, rows = sanitize_results(columns, rows)
        print(columns)
        for row in rows:
            print(row)