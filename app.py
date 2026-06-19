import streamlit as st
import pandas as pd
from src.nl_to_sql import ask_sales_assistant
st.set_page_config(
    page_title="Sales Insights Assistant",
    page_icon="📊",
    layout="wide"
)
st.title("📊 Sales Insights Assistant")
st.caption(
    "Ask questions about the Northwind sales database"
)
if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
question = st.chat_input("Ask a sales question...")
if question:
    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner(
            "Thinking..."
        ):
            response = ask_sales_assistant(
                question
            )
        if response["error"]:
            st.error(
                response["error"]
            )
        else:
            st.success(
                "Query executed successfully"
            )
            with st.expander(
                "Generated SQL"
            ):
                st.code(
                    response["sql"],
                    language="sql"
                )
            if len(response["rows"]) > 0:
                df = pd.DataFrame(response["rows"],columns=response["columns"])
                st.dataframe(df,use_container_width=True)
            else:
                st.info("No rows returned")
            if response["confidence"]=="High":
                st.success("High confidence")
            elif response["confidence"]=="Medium":
                st.warning("Medium confidence")
            else:
                st.warning("Low confidence. Verify results.")
            st.caption(
                f"Trace ID: "
                f"{response['trace_id']}"
            )
        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":
                f"Trace ID: "
                f"{response['trace_id']}"
            }
        )
with st.sidebar:

    st.header(

        "Database Overview"

    )


    st.markdown(

"""
### Main Tables

**customers**

Customer information

---

**orders**

Order headers

---

**order_details**

Products inside each order

---

**products**

Product catalog

---

**categories**

Product categories

---

**employees**

Sales employees

"""
)
st.header(

    "Example Questions"

)


st.markdown(

"""

- Top 5 customers by sales

- Sales by category

- Highest selling product in Germany

- Monthly sales trend

- Employee with highest revenue

- Top suppliers by sales

"""

)