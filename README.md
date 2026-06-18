# Sales-Assistant
sudo apt update

sudo apt install postgresql postgresql-contrib

psql -U postgres
CREATE DATABASE northwind;
wget https://raw.githubusercontent.com/pthom/northwind_psql/master/northwind.sql

sudo cp northwind.sql /tmp/

sudo -u postgres psql -d northwind -f /tmp/northwind.sql

**Decision:** Metadata is extracted programmatically using PostgreSQL's `information_schema` instead of hardcoding schema details.

**Reasoning:** Hardcoding tables and columns would make the system brittle to schema changes. Programmatic extraction ensures that the LLM always receives an up-to-date view of the database schema, including table names, columns, data types, row counts, foreign keys, and representative categorical values.

**Tradeoff:** Metadata extraction introduces a small startup cost but greatly improves maintainability and NL→SQL accuracy.

Day3: 
Prompt final version: 
You are an expert PostgreSQL SQL assistant.

Generate ONLY read-only SQL.

Allowed:
- SELECT
- WITH (CTEs)

Forbidden:
- INSERT
- UPDATE
- DELETE
- DROP
- ALTER
- TRUNCATE
- CREATE
- MERGE

Use ONLY the tables, columns and LOVs provided.

Do not invent tables, columns or values.

Always use explicit JOIN syntax.

If no limit is specified, use LIMIT 100.

Return ONLY SQL.
No explanations.
No markdown.

Schema:
{schema_context}

Relationships:
{relationship_context}

Allowed Values:
{lov_context}

Question:
{user_question}

# Task 2.2 #
pip install langchain langchain-openai python-dotenv
pip install langchain-google-genai python-dotenv