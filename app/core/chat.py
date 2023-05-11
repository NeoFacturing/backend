from app.utils.make_chain import make_chain
from app.utils.vector_store import make_vectorstore
from langchain import LLMChain
from app.core.ai_model import llm_chain


def get_response(input: str, history: str) -> str:
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
        vectorstore = make_vectorstore()
    except Exception as e:
        print(f"Error in creating the vector store: {str(e)}")
        return None

    try:
        chain = make_chain(vectorstore)
    except Exception as e:
        print(f"Error in creating the chain: {str(e)}")
        return None

    try:
        response = chain({"question": sanitizedInput, "chat_history": history})
        answer = response["answer"].strip().replace("\n", " ")
        source = response["sources"]
        print(response)
        return {"answer": answer, "source": source}

    except Exception as e:
        print(f"Error in running the chain: {str(e)}")
        return None
