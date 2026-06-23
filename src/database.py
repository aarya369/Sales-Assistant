import os
import psycopg2
import streamlit as st

from src.sql_validator import clean_sql
from src.result_sanitizer import (
    sanitize_results,
    handle_empty_results
)


import streamlit as st
import psycopg2


def get_connection():

    conn = psycopg2.connect(

        host=st.secrets["DB_HOST"],

        database=st.secrets["DB_NAME"],

        user=st.secrets["DB_USER"],

        password=st.secrets["DB_PASSWORD"],

        port=st.secrets["DB_PORT"],

        sslmode="require"

    )

    return conn


def execute_sql(sql):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(sql)

    rows = cur.fetchall()

    columns = [

        desc[0]

        for desc in cur.description

    ]

    cur.close()

    conn.close()

    return columns, rows


def execute_with_retry(

    question,

    sql,

    retry_chain,

    max_retries=2

):

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


if __name__ == "__main__":

    sql = """

    SELECT *

    FROM products

    LIMIT 5;

    """

    columns, rows = execute_sql(sql)

    columns, rows = sanitize_results(

        columns,

        rows

    )

    print(columns)

    for row in rows:

        print(row)