from langchain.prompts import PromptTemplate

simple_template = """Hallo, du bist ein Konstrukteur und beantwortest Fragen zur Konstruktion von Bauteilen. Frage: {input}"""

simple_prompt_template = PromptTemplate(
    template=simple_template, input_variables=["input"]
)
