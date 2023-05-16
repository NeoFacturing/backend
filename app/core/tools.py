from langchain.agents import Tool
from app.core.llm_chain import qa_chain

tools = [
    Tool(
        name="Knowledge Base",
        func=qa_chain.run,
        description=("Benutze die Knowledge Base um Antworten auf Fragen zu finden."),
    )
]
