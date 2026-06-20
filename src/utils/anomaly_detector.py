from src.utils.logger import logger
from collections import deque
from collections import defaultdict
import os
import json

from datetime import datetime
from datetime import timedelta


def check_sql_length(sql, trace_id):
    if len(sql) > 500:
        logger.warning(
            "",
            extra={
                "trace_id":
                trace_id,
                "component":
                "anomaly_detector",
                "event_type":
                "long_sql",
                "payload":{

                    "sql_length":
                    len(sql)
                }
            }
        )

from datetime import datetime, timedelta
from src.utils.logger import logger

def record_validation(

    success,

    trace_id

):

    state = load_state()


    now = datetime.utcnow()


    now_str = now.isoformat()


    state["validation_history"].append(

        [success, now_str]

    )


    cutoff = now - timedelta(

        minutes=10

    )


    filtered = []


    for success, t in state["validation_history"]:

        t_obj = datetime.fromisoformat(t)

        if t_obj >= cutoff:

            filtered.append(

                [

                    success,

                    t

                ]

            )


    state["validation_history"] = filtered


    save_state(

        state

    )


    total = len(

        filtered

    )


    failed = sum(

        1

        for success, _

        in filtered

        if not success

    )


    if total > 0:

        failure_rate = failed / total


        if failure_rate > 0.30:


            logger.warning(

                "",

                extra={

                    "trace_id":

                    trace_id,

                    "component":

                    "anomaly_detector",

                    "event_type":

                    "high_validation_failure",

                    "payload":{

                        "failure_rate":

                        round(

                            failure_rate,

                            2

                        ),

                        "window":

                        "10min"

                    }

                }

            )

def record_user_query(

    user_id,

    trace_id

):

    state = load_state()


    now = datetime.utcnow()


    now_str = now.isoformat()


    if user_id not in state["user_queries"]:

        state["user_queries"][user_id] = []


    state["user_queries"][user_id].append(

        now_str

    )


    cutoff = now - timedelta(

        minutes=5

    )


    filtered = []


    for t in state["user_queries"][user_id]:

        t = datetime.fromisoformat(t)

        if t >= cutoff:

            filtered.append(

                t.isoformat()

            )


    state["user_queries"][user_id] = filtered


    save_state(

        state

    )


    query_count = len(

        filtered

    )


    if query_count > 20:

        logger.critical(

            "",

            extra={

                "trace_id":

                trace_id,

                "component":

                "anomaly_detector",

                "event_type":

                "high_query_volume",

                "payload":{

                    "user":

                    user_id,

                    "queries_last_5min":

                    query_count

                }

            }

        )
STATE_FILE = "logs/anomaly_state.json"
def load_state():

    if not os.path.exists(

        STATE_FILE

    ):

        return {

            "validation_history":[],

            "user_queries":{}

        }


    with open(

        STATE_FILE,

        "r"

    ) as f:

        return json.load(f)
def save_state(state):

    with open(

        STATE_FILE,

        "w"

    ) as f:

        json.dump(

            state,

            f,

            indent=4

        )