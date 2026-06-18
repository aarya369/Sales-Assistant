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

def get_tables(conn):
    cur = conn.cursor()
    cur.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    ORDER BY table_name;
    """)
    tables = [row[0] for row in cur.fetchall()]
    cur.close
    return tables

def get_row_count(conn):
    cur = conn.cursor()
    tables = get_tables(conn)
    row_counts = {}
    for table in tables:
        cur.execute(f"""
        SELECT COUNT(*)
        FROM {table};
        """)
        row_counts[table] = cur.fetchone()[0]
    cur.close()
    return row_counts

def get_columns(conn):
    cur = conn.cursor()
    cur.execute("""
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position;
    """)
    rows = cur.fetchall();
    columns = {}
    for table, column, dtype in rows:
        if table not in columns:
            columns[table] = []
        columns[table].append(
            {
                "column_name": column,
                "data_type": dtype
            }
        )
    cur.close()
    return columns

def get_lov(conn, table, column, limit = 5):
    cur = conn.cursor()
    query = f"""
    SELECT DISTINCT {column}
    FROM {table}
    WHERE {column} IS NOT NULL
    ORDER BY {column}
    LIMIT {limit};
    """
    cur.execute(query)
    values = [row[0] for row in cur.fetchall()]
    cur.close()
    return values

def build_metadata(conn):
    metadata = {
        "tables": {}
    }
    tables = get_tables(conn)
    row_counts = get_row_count(conn)
    columns = get_columns(conn)
    for table in tables:
        metadata["tables"][table] = {
            "row_count": row_counts[table],
            "columns": columns[table],
            "lov": {
                "country": get_lov(conn, table, "country")
            } if table == "customers" else {}
        }
    return metadata

def get_foreign_keys(conn):

    cur = conn.cursor()

    cur.execute("""

    SELECT

        tc.table_name,

        kcu.column_name,

        ccu.table_name AS foreign_table_name,

        ccu.column_name AS foreign_column_name

    FROM information_schema.table_constraints tc

    JOIN information_schema.key_column_usage kcu

    ON tc.constraint_name = kcu.constraint_name

    JOIN information_schema.constraint_column_usage ccu

    ON ccu.constraint_name = tc.constraint_name

    WHERE tc.constraint_type = 'FOREIGN KEY'

    ORDER BY tc.table_name;

    """)

    rows = cur.fetchall()

    fks = []

    for table, column, foreign_table, foreign_column in rows:

        fks.append(

            {

                "table": table,

                "column": column,

                "foreign_table": foreign_table,

                "foreign_column": foreign_column

            }

        )

    cur.close()

    return fks

def generate_schema_docs(metadata):

    docs = ""

    for table_name, table_info in metadata["tables"].items():

        docs += f"\nTable: {table_name}\n"

        docs += f"Rows: {table_info['row_count']}\n\n"

        docs += "Columns:\n"

        for col in table_info["columns"]:

            docs += (

                f"- "

                f"{col['column_name']} "

                f"({col['data_type']})\n"

            )

        if table_info["lov"]:

            docs += "\nSample values:\n"

            for column, values in table_info["lov"].items():

                docs += f"\n{column}:\n"

                docs += ", ".join(

                    str(v)

                    for v in values

                )

                docs += "\n"

        docs += "\n"

        docs += "-"*40

        docs += "\n"

    return docs

if __name__ == "__main__":

    conn = get_connection()

    print("Connection successful!")
    metadata = build_metadata(conn)
    docs = generate_schema_docs(metadata)
    with open(
        "schema_docs.txt", "w",encoding = "utf-8"
    ) as f:
        f.write(docs)
    
    conn.close()