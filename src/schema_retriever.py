#Reads schema_docs.txt and splits it table-wise
def load_schema_docs(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    tables = content.split("----------------------------------------")
    return tables
TABLE_KEYWORDS = {
   "customers": [
        "customer",
        "customers"
    ],
    "orders": [
        "order",
        "orders"
    ],
    "products": [
        "product",
        "products"
    ],
    "order_details": [
        "order detail",
        "quantity",
        "discount"
    ],
    "employees": [
        "employee",
        "employees",
        "salesperson",
        "person"
    ],
    "categories": [
        "category",
        "categories",
        "genre",
        "section"
    ],
    "suppliers": [
        "supplier",
        "suppliers"
    ]
}

def get_relevant_tables(question):
    question = question.lower()
    relevant = []
    for table, keywords in TABLE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in question:
                relevant.append(table)
                break
    return relevant
TABLE_DEPENDENCIES = {
    "products":["order_details"],
    "order_details":["orders"],
    "orders":["customers"]
}

def add_dependencies(tables):
    expanded = set(tables)
    changed = True
    while changed:
        changed = False
        for table in list(expanded):
            if table in TABLE_DEPENDENCIES:
                for dep in TABLE_DEPENDENCIES[table]:
                    if dep not in expanded:
                        expanded.add(dep)
                        changed = True
    return list(expanded)

def get_schema_context(
        filepath,
        relevant_tables
):
    tables = load_schema_docs(filepath)
    context = ""
    for table_text in tables:
        for table_name in relevant_tables:
            if f"Table: {table_name}" in table_text:
                context += table_text
                context += "\n"
    return context
question = "Top selling products"
tables = get_relevant_tables(question)
tables = add_dependencies(tables)
schema_context = get_schema_context(
    "schema_docs.txt",
    tables
)
