import psycopg2

def get_connection():
    conn = psycopg2.connect(
        dbname="northwind",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
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

from result_sanitizer import sanitize_results, handle_empty_results
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