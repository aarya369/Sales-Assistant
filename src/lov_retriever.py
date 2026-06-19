from src.schema_retriever import load_schema_docs
def get_lov_context(
        filepath,
        relevant_tables
):
    tables = load_schema_docs(filepath)
    lov_context = ""
    for table_text in tables:
        for table_name in relevant_tables:
            if f"Table: {table_name}" in table_text:
                if "Sample values:" in table_text:
                    sample_section = (
                        table_text
                        .split("Sample values:")[1]
                    )
                    lov_context += (
                        f"\nTable: {table_name}\n"
                    )
                    lov_context += sample_section
                    lov_context += "\n"
    return lov_context
LOV_KEYWORDS = {
    "country":[ "country","countries"],
    "city":["city", "cities"],
    "region":["region", "regions"],
    "category":["category","categories"]
}

def is_relevant_lov(
        column,
        question
):
    question = question.lower()
    if column not in LOV_KEYWORDS:
        return False
    for keyword in LOV_KEYWORDS[column]:
        if keyword in question:
            return True
    return False
