import logging
import json
import os
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {"timestamp":datetime.fromtimestamp(record.created).isoformat(),"level": record.levelname, "trace_id": getattr(record,"trace_id",None),
            "component":getattr(record,"component",None),
            "event_type":getattr(record,"event_type",None),
            "payload":getattr(record,"payload",None)
        }
        return json.dumps(log_record)
os.makedirs("logs",exist_ok=True)

logger = logging.getLogger("sales_assistant")

logger.setLevel(logging.INFO)

handler = logging.FileHandler("logs/logs.jsonl")

handler.setFormatter(JsonFormatter())

logger.addHandler(handler)
console_handler = logging.StreamHandler()

console_handler.setFormatter(
    JsonFormatter()
)

logger.addHandler(
    console_handler
)