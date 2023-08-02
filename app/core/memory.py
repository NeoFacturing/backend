from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.prompts import MessagesPlaceholder

agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
}
memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

