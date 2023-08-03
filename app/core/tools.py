from typing import Optional, Type
import requests
import os
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

# from app.core.llm_chain import simple_llm_chain


def draft_analysis(filepath: str) -> str:
    """Schickt eine Anfrage an den Server mit dem Pfad zur .step Datei, um eine Formschrägenanalyse durchzuführen."""
    print(filepath)
    params = {"filepath": filepath}
    url = os.environ["NGROK_URL"] + "/api/SolidWorks/run"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("Request was successful!")
        return "Request was successful!"
    else:
        print(f"Failed to send request! Status code: {response.status_code}")
        return f"Failed to send request! Status code: {response.status_code}"


class DraftAnalysisInput(BaseModel):
    """Eingabeparameter für die Formschrägenanalyse."""

    filepath: str = Field(
        ...,
        title="Pfad zur Datei",
        description="Pfad zur .step Datei, die analysiert werden soll.",
    )


class DraftAnalysisTool(BaseTool):
    name = "draft_analysis"
    description = "Formschrägenanalyse für .step Dateien."

    def _run(self, filepath: DraftAnalysisInput) -> str:
        sanitizedInput = filepath.strip().replace("\n", " ")
        return draft_analysis(filepath=sanitizedInput)

    def _arun(self, input: DraftAnalysisInput) -> str:
        raise NotImplementedError("This tool does not support asynchronous execution.")

    args_schema: Optional[Type[BaseModel]] = DraftAnalysisInput


tools = [DraftAnalysisTool()]
