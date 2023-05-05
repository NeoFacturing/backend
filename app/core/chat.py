from langchain import LLMChain
from app.core.ai_model import llm_chain


def get_response(input: str, llm_chain: LLMChain = llm_chain) -> str:
    """
    Get a response from the AI model based on the user input.

    Args:
        input (str): Input text to get a response from the AI model
        llm_chain (LLMChain, optional): An instance of LLMChain to use for generating responses.

    Returns:
        str: AI model's response
    """
    response = llm_chain.run(input)
    print(response)
    return response
