from langchain.chains import RetrievalQA
from app.utils.vector_store import make_retriever
from app.core.llm import chatgpt

retriever = make_retriever()

qa_chain = RetrievalQA.from_chain_type(
    llm=chatgpt,
    chain_type="stuff",
    retriever=retriever,
)
