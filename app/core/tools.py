from langchain.agents import Tool
from app.core.llm_chain import simple_llm_chain

tools = [
    Tool(
        name="Knowledge Base",
        func=simple_llm_chain.run,
        description=("Benutze die Knowledge Base um Antworten auf Fragen zu finden."),
    )
]
