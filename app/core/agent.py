from langchain.agents import AgentExecutor, ConversationalChatAgent, ZeroShotAgent
import langchain.chains.conversation as conversational_memory
from langchain import LLMChain

# from app.core.prompt import prompt
from app.core.llm import chatgpt
from app.core.memory import conversational_memory
from app.core.tools import tools
from app.core.prompt import zero_shot_prompt

# LLM chain needs to be instantiated with the LLM model and the right prompt for the agent
llm_chain = LLMChain(llm=chatgpt, prompt=zero_shot_prompt)
zero_shot_agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)

# Agent below is not working
conversational_chat_agent = ConversationalChatAgent(
    tools=tools,
    llm_chain=llm_chain,
    verbose=True,
)

agent_chain = AgentExecutor.from_agent_and_tools(
    agent=zero_shot_agent, tools=tools, verbose=True, memory=conversational_memory
)
