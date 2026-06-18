from security_judge import llm_security_check, off_topic_check
import re
PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "forget previous instructions",
    "forget the schema",
    "ignore the schema",
    "reveal system prompt",
    "show system prompt",
    "return all customer emails",
    "act as a dba",
    "bypass restrictions"
]
def detect_prompt_injection(question):
    q = question.lower()
    for pattern in PROMPT_INJECTION_PATTERNS:
        if pattern in q:
            raise ValueError(
                "Prompt injection attempt detected."
            )
    return True

JAILBREAK_PATTERNS = [
    "you are dan",
    "developer mode",
    "no restrictions",
    "unrestricted ai",
    "pretend to be",
    "ignore safety",
    "act without limitations"
]

def detect_jailbreak(question):
    q = question.lower()
    for pattern in JAILBREAK_PATTERNS:
        if pattern in q:
            raise ValueError(
                "Jailbreak attempt detected."
            )
    return True
EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
def detect_email(text):
    return re.findall(
        EMAIL_PATTERN,
        text
    )
PHONE_PATTERN = r'\b(?:\+?\d{1,3}[- ]?)?\d{10}\b'
def detect_phone(text):
    return re.findall(
        PHONE_PATTERN,
        text
    )
def redact_pii(text):
    text = re.sub(
        EMAIL_PATTERN,
        "[REDACTED_EMAIL]",
        text
    )


    text = re.sub(
        PHONE_PATTERN,
        "[REDACTED_PHONE]",
        text
    )
    return text

def safe_log_question(question):
    return redact_pii(question)

def validate_input(question):
    detect_prompt_injection(question)
    detect_jailbreak(question)
    off_topic_check(question)
    llm_security_check(question)
    return True