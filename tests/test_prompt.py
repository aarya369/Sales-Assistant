from prompts import NL_TO_SQL_PROMPT


schema_context = """

payments(
payment_id,
order_id,
payment_amount,
payment_date,
payment_status
)

orders(
order_id,
customer_id,
order_date
)

"""


relationship_context = """
payments.order_id -> orders.order_id
"""


lov_context = """
payments.payment_status:
Success
Failed
Pending
"""

user_question = """
Show monthly revenue from successful payments.
"""


prompt = NL_TO_SQL_PROMPT.format(

    schema_context=schema_context,
    relationship_context=relationship_context,
    lov_context=lov_context,
    user_question=user_question

)

print(prompt)
