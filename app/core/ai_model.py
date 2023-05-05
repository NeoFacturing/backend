from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

gpt3 = OpenAI(
    model_name="gpt-3.5-turbo",
)

template = """Question: {question}

Answer: """
prompt = PromptTemplate(template=template, input_variables=["question"])

llm_chain = LLMChain(prompt=prompt, llm=gpt3)
