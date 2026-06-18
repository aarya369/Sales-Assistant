from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from prompts import SECURITY_PROMPT, OFFTOPIC_PROMPT
load_dotenv()
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

security_chain = (
    SECURITY_PROMPT | llm | StrOutputParser()
)

def llm_security_check(question):
    response = security_chain.invoke(
        {
            "question":
            question
        }
    )
    response = response.strip().upper()
    if response == "UNSAFE":
        raise ValueError(
            "Unsafe input detected."
        )
    return True


offtopic_chain = OFFTOPIC_PROMPT | llm | StrOutputParser()
def off_topic_check(question):
    response = offtopic_chain.invoke({"question": question})
    response = response.strip().upper()

    if response == "OUT_OF_SCOPE":
        raise ValueError("Question is outside the scope of the Sales Insights Assistant.")

    return True