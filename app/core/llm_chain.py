from langchain import LLMChain
from langchain.chains import RetrievalQA

from app.utils.vector_store import make_retriever
from app.core.llm import chatgpt
from app.core.prompt import simple_prompt_template

simple_llm_chain = LLMChain(llm=chatgpt, prompt=simple_prompt_template)
