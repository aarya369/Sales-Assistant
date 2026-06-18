# test_schema_retriever.py

from schema_retriever import load_schema_docs


tables = load_schema_docs("schema_docs.txt")

print(len(tables))

print(tables[0])