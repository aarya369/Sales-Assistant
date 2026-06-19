import uuid


def create_trace_id():

    return str(uuid.uuid4())


class Trace:

    def __init__(self, trace_id):

        self.trace = {

            "trace_id": trace_id,

            "user_question": None,

            "retrieved_context": None,

            "llm_prompt": None,

            "generated_sql": None,

            "guardrail": None,

            "db_result": None,

            "final_response": None

        }

    def update(self, key, value):

        self.trace[key] = value


    def save(self):
        import os
        import json

        os.makedirs("traces", exist_ok=True)

        filename = f"traces/{self.trace['trace_id']}.json"

        with open(filename, "w") as f:

            json.dump(
                self.trace,
                f,
                indent=4,
                default=str
        )