from logger import logger

logger.critical(

    "",

    extra={

        "trace_id":"123",

        "component":"test",

        "event_type":"critical_test",

        "payload":{

            "msg":"hello"

        }

    }

)