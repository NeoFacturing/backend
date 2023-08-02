from langchain.agents import initialize_agent
from langchain.agents import AgentType
from app.core.llm import chatgpt
from app.core.tools import tools
from app.core.memory import memory, agent_kwargs

open_ai_agent = initialize_agent(
    tools,
    chatgpt,
    agent=AgentType.OPENAI_FUNCTIONS,
    memory=memory,
    agent_kwargs=agent_kwargs,
    verbose=True,
)
