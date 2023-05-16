from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory

conversational_memory = ConversationBufferMemory(memory_key="chat_history")
readonlymemory = ReadOnlySharedMemory(memory=conversational_memory)
