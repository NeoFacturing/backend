import os
from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
chatgpt = ChatOpenAI(
    openai_api_key=openai_api_key,
    model_name="gpt-3.5-turbo",
    temperature=0.0,
)

template = """Frage: {question}

Antwort: """
prompt = PromptTemplate(template=template, input_variables=["question"])