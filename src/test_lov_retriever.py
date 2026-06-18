# test_lov_retriever.py

from lov_retriever import get_lov_context


relevant_tables = [

    "customers"

]

lov_context = get_lov_context(

    "schema_docs.txt",

    relevant_tables

)

print(lov_context)