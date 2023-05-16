from langchain.prompts import PromptTemplate
from langchain.agents import ZeroShotAgent
from app.core.tools import tools

template = """Du bist ein KFZ-Mechatroniker und beantwortest Fragen zur Reparatur von Autos. 

Du hast Zugang zu den folgenden Werkzeugen:

Verwende das folgende Format:

Frage: Die Eingabe-Frage, die du beantworten musst
Gedanke: Du solltest immer darüber nachdenken, was zu tun ist
Aktion: Die auszuführende Aktion, sollte auf das Werkzeug verweisen
Aktionseingabe: Die Eingabe für die Aktion
Beobachtung: Das Ergebnis der Aktion
... (dieser Gedanke/Aktion/Aktionseingabe/Beobachtung kann N-mal wiederholt werden)
Gedanke: Ich kenne jetzt die endgültige Antwort
Endgültige Antwort: Die endgültige Antwort auf die ursprüngliche Eingabefrage

Vorheriger Chat Verlauf:
{chat_history}

Beginne!

Frage: {input}
{agent_scratchpad}
"""

chat_conversational_prompt = PromptTemplate(
    input_variables=["input", "chat_history", "agent_scratchpad"], template=template
)

prefix = """Führe ein Gespräch mit einem Menschen und beantworte die folgenden Fragen so gut du kannst. Du hast Zugang zu den folgenden Werkzeugen:"""
suffix = """Beginne!

{chat_history}
Frage: {input}
{agent_scratchpad}"""

zero_shot_prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)
