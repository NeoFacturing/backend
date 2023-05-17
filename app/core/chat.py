from app.core.agent import agent_chain
from app.core.llm_chain import qa_chain


def get_response(input: str, ai: str) -> str:
    """
    Get a response from the AI model based on the user input.

    Args:
        input (str): Input text to get a response from the AI model
        llm_chain (LLMChain, optional): An instance of LLMChain to use for generating responses.

    Returns:
        str: AI model's response
    """
    try:
        # OpenAI recommends replacing newlines with spaces for best results
        sanitizedInput = input.strip().replace("\n", " ")
    except Exception as e:
        print(f"Error in sanitizing the input: {str(e)}")
        return None
    try:
        if ai == "agent":
            agent_response = agent_chain.run(input=sanitizedInput)
            return agent_response
        else:
            response = qa_chain.run(sanitizedInput)
            return response

    except Exception as e:
        print(f"Error in running the chain: {str(e)}")
        return None
