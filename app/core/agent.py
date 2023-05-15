from langchain.agents import Tool, initialize_agent
import langchain.chains.conversation as conversational_memory
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA, LLMChain
from langchain.llms import OpenAI

from app.core.ai_model import chatgpt
from app.core.prompt import prompt_template
from app.utils.vector_store import make_retriever



retriever = make_retriever()

#llm_chain = LLMChain(llm=chatgpt, prompt=chat_prompt)

qa_chain = RetrievalQA.from_chain_type(
            llm=chatgpt,
            chain_type="stuff",
            retriever=retriever,
        )

conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)

tools = [
    Tool(
        name='Knowledge Base',
        func=qa_chain.run,
        description=(
            'Benutze die Knowledge Base um Antworten auf Fragen zu finden.'
        )
    )
]

prompt_with_history = CustomPromptTemplate(
    template=template,
    tools=tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    input_variables=["input", "intermediate_steps", "history"]
)

agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=tools,
    llm=chatgpt,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=conversational_memory
)

print(agent.agent.llm_chain.prompt)