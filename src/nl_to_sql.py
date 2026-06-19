from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from src.prompts import NL_TO_SQL_PROMPT, RETRY_PROMPT
from src.schema_retriever import (get_relevant_tables, add_dependencies, get_schema_context)
from src.lov_retriever import get_lov_context
from src.sql_validator import validate_sql, ensure_limit
from src.intent_validator import validate_question
from src.input_guardrails import validate_input
from src.database import execute_sql, execute_with_retry
from src.result_sanitizer import sanitize_results, handle_empty_results
from src.utils.trace import Trace, create_trace_id
from src.utils.logger import logger
from src.utils.anomaly_detector import check_sql_length, record_validation, record_user_query

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

chain = (NL_TO_SQL_PROMPT|llm|StrOutputParser())
retry_chain = (RETRY_PROMPT| llm| StrOutputParser())

def generate_sql(question, trace):
    validate_input(question)
    validate_question(question)

    tables = get_relevant_tables(question)
    tables = add_dependencies(tables)
    trace.update("retrieved_context",{"tables": tables})
    logger.info("",
    extra={
        "trace_id":
        trace.trace["trace_id"],

        "component":
        "retriever",

        "event_type":
        "context_retrieved",

        "payload":{

            "tables":
            tables
        }
    }
)
    schema_context = get_schema_context("schema_docs.txt",tables)
    lov_context = get_lov_context("schema_docs.txt",tables)
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

    prompt_inputs = {"schema_context":schema_context,"relationship_context":relationship_context,"lov_context":lov_context,"user_question":question}
    trace.update("llm_prompt",prompt_inputs)

    sql = chain.invoke(prompt_inputs)
    trace.update("generated_sql",sql)
    check_sql_length(sql,trace.trace["trace_id"])
    logger.info("",extra={"trace_id":trace.trace["trace_id"],"component":"sql_generator","event_type":"sql_generated","payload":{"sql_length":len(sql)}})
    
    try:
        validate_sql(sql)
        trace.update("guardrail",{"status":"passed"})
        record_validation(True,trace.trace["trace_id"] )
        logger.info(
        "",
        extra={
            "trace_id":
            trace.trace["trace_id"],
            "component":
            "guardrail",
            "event_type":
            "guardrail_passed",
            "payload":{}
        }
    )
    except Exception as e:
        trace.update("guardrail",{"status":"blocked","reason":str(e)})
        record_validation(False,trace.trace["trace_id"])
        logger.warning(
        "",
        extra={
            "trace_id":
            trace.trace["trace_id"],
            "component":
            "guardrail",
            "event_type":
            "guardrail_triggered",
            "payload":{
                "reason":
                str(e)
            }
        }
    )
        raise
  
    sql = ensure_limit(sql)
    return sql

def ask_sales_assistant(question):
    trace_id = create_trace_id()
    trace = Trace(trace_id)
    record_user_query(user_id="default_user",trace_id=trace_id)
    trace.update("user_question", question)
    logger.info(
    "",
    extra={
        "trace_id": trace_id,
        "component":"main",
        "event_type":"input_received",
        "payload":{
            "question_length":
            len(question)
        }
    }
)
    try:
        sql = generate_sql(question, trace)
        sql, columns, rows = execute_with_retry(question, sql, retry_chain)
        trace.update("db_result",{"columns": columns,"rows": rows})
        logger.info(
        "",
        extra={
        "trace_id":
        trace_id,
        "component":
        "database",
        "event_type":
        "query_executed",
        "payload":{
            "rows_returned":
            len(rows)
        }
    }
)
        if len(rows) == 0:
            return {"trace_id":trace_id,"sql":sql,"columns":[],"rows":[],"confidence":"Low","message":handle_empty_results(),"error":None}        
        else:
            columns, rows = sanitize_results(columns, rows)
            #print("\nResults:\n")
            response = {
                "columns": columns,
                "rows": rows
            }
            trace.update("final_response", response)
            logger.info(

            "",

            extra={

            "trace_id":
            trace_id,

            "component":
            "main",

            "event_type":
            "response_returned",

            "payload":{
                "response_type":
                "table"

        }

    }

)
            return {"trace_id":trace_id,"sql":sql,"columns":columns,"rows":rows,"confidence":"High","error":None}
    except Exception as e:
        return {"trace_id":trace_id,"sql":None,"columns":None,"rows":None,"confidence":None,"error":str(e)}
    finally:
        trace.save()

if __name__ == "__main__":
    question = input(
        "\nEnter your question:\n"
    )
    response = ask_sales_assistant(question)

    if response["error"]:
        print("\nError:\n")
        print(response["error"])

    else:
        print("\nResult:\n")
        print(response["columns"])
        for row in response["rows"]:
            print(row)
    print(
        f"\nTrace ID: "
        f"{response['trace_id']}"
    )