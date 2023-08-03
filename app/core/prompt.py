from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent

simple_template = """Hallo, du bist ein Konstrukteur und beantwortest Fragen zur Konstruktion von Bauteilen. Frage: {input}"""

simple_prompt_template = PromptTemplate(
    template=simple_template, input_variables=["input"]
)

german_system_message = SystemMessage(
    content="Du bist ein hilfreicher KI-Assistent für Bauingenieure."
)
agent_prompt = OpenAIFunctionsAgent.create_prompt(system_message=german_system_message)
