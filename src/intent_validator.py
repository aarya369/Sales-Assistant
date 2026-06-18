FORBIDDEN_INTENTS = [

    "delete",

    "drop",

    "update",

    "alter",

    "truncate",

    "insert",

    "create"

]
def validate_question(question):

    question_lower = question.lower()

    for keyword in FORBIDDEN_INTENTS:

        if keyword in question_lower:

            raise ValueError(

                f"Operation '{keyword}' is not allowed. Only read-only queries are supported."

            )

    return True