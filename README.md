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
