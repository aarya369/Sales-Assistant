FORBIDDEN_KEYWORDS = ["INSERT","UPDATE","DELETE","DROP","ALTER","TRUNCATE","CREATE","MERGE","GRANT","REVOKE"]
ALLOWED_TABLES = {"categories","customer_customer_demo","customer_demographics","customers","employee_territories","employees","order_details","orders","products","region","shippers","suppliers","territories","us_states"}
def check_forbidden_keywords(sql):
    sql_upper = sql.upper()
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in sql_upper:
            raise ValueError(
                f"Unsafe SQL detected: {keyword}"
            )
    return True
import re
def validate_tables(sql):
    sql_lower = sql.lower()
    found_tables = re.findall(
        r"(?:from|join)\s+(?:\w+\.)?([a-zA-Z_]+)",
        sql_lower
    )
    for table in found_tables:
        if table not in ALLOWED_TABLES:
            raise ValueError(
                f"Unknown table: {table}"
            )
    return True
def is_select_only(sql):
    sql = sql.strip().upper()
    return (
        sql.startswith("SELECT")
        or
        sql.startswith("WITH")
    )
def validate_sql(sql):

    sql_upper = sql.strip().upper()

    if sql_upper in [

        "OUT_OF_SCOPE",

        "CLARIFICATION_REQUIRED"

    ]:

        return True


    validate_syntax(sql)


    if not is_select_only(sql):

        raise ValueError(

            "Only SELECT queries are allowed."

        )


    check_forbidden_keywords(sql)

    validate_tables(sql)


    return True
import sqlglot
def validate_syntax(sql):
    try:
        sqlglot.parse_one(
            sql,
            dialect="postgres"
        )
        return True
    except Exception:
        raise ValueError(
            "Invalid SQL syntax"
        )
