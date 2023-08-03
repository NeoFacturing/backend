from app.core.azure_utils import generate_download_link, get_blob_service_client
from app.core.agent import open_ai_agent


def get_response(input: str, ai: str, input_file: str) -> str:
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
        folder_name = input_file.split("/")[0]
        input_file_path = folder_name + "/input.step"

        output_files = [
            "backView.bmp",
            "bottomView.bmp",
            "dimetricView.bmp",
            "frontView.bmp",
            "isometricView.bmp",
            "leftView.bmp",
            "rightView.bmp",
            "topView.bmp",
            "trimetricView.bmp",
        ]
        blob_service_client = get_blob_service_client()
        dl_links = list(
            map(
                lambda file_name: generate_download_link(
                    blob_service_client, folder_name + "/out/" + file_name
                ),
                output_files,
            )
        )

        blob_service_client = get_blob_service_client()
        sanitizedInput = sanitizedInput + "Dateipfad: " + input_file_path
        response = open_ai_agent(sanitizedInput)

        return {
            "response": response["output"],
            "files": dl_links,
        }

    except Exception as e:
        print(f"Error in running the chain: {str(e)}")
        return None
