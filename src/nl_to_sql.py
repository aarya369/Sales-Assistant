from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.output_parsers import StrOutputParser

from prompts import NL_TO_SQL_PROMPT

from schema_retriever import (
    get_relevant_tables,
    add_dependencies,
    get_schema_context
)

from lov_retriever import get_lov_context
from sql_validator import validate_sql
from intent_validator import validate_question
load_dotenv()


llm = ChatGoogleGenerativeAI(

    model="gemini-2.5-flash",

    temperature=0

)

chain = (

    NL_TO_SQL_PROMPT

    |

    llm

    |

    StrOutputParser()

)

def generate_sql(question):
    validate_question(question)

    tables = get_relevant_tables(question)

    tables = add_dependencies(tables)


    schema_context = get_schema_context(

        "schema_docs.txt",

        tables

    )


    lov_context = get_lov_context(

        "schema_docs.txt",

        tables

    )


    relationship_context = """

orders.customer_id -> customers.customer_id

orders.employee_id -> employees.employee_id

order_details.order_id -> orders.order_id

order_details.product_id -> products.product_id

products.category_id -> categories.category_id

products.supplier_id -> suppliers.supplier_id

employee_territories.employee_id -> employees.employee_id

employee_territories.territory_id -> territories.territory_id

territories.region_id -> region.region_id

"""


    sql = chain.invoke(

        {

            "schema_context":

            schema_context,

            "relationship_context":

            relationship_context,

            "lov_context":

            lov_context,

            "user_question":

            question

        }

    )
    validate_sql(sql)

    return sql
if __name__ == "__main__":

    question = input(

        "\nEnter your question:\n"

    )

    try:

        sql = generate_sql(question)

        print(

            "\nGenerated SQL:\n"

        )

        print(sql)

    except Exception as e:

        print(

            "\nError:\n"

        )

        print(e)