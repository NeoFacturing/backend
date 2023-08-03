from typing import Union, Optional, Dict, List
import logging

from app.core.azure_utils import generate_download_link, get_blob_service_client
from app.core.agent import open_ai_agent


def sanitize_input(input: str) -> str:
    """Sanitize the input by stripping whitespace and replacing newlines."""
    try:
        return input.strip().replace("\n", " ")
    except Exception as e:
        logging.error(f"Error in sanitizing the input: {str(e)}")
        raise


def generate_download_links(folder_name: str, file_names: List[str]) -> List[str]:
    blob_service_client = get_blob_service_client()
    return [
        generate_download_link(blob_service_client, f"{folder_name}/out/{file_name}")
        for file_name in file_names
    ]


def get_response(
    input: str, ai: str, input_file: Optional[str]
) -> Optional[Dict[str, Union[str, List[str]]]]:
    """
    Get a response from the AI model based on the user input.

    Args:
        input (str): Input text to get a response from the AI model.
        ai (str): AI model to use.
        input_file (str, optional): Path to the input file.

    Returns:
        dict: AI model's response with optional download links for files.
    """
    sanitized_input = sanitize_input(input)

    try:
        if input_file is None:
            sanitized_input += f" Frage den Benutzer nach dem Dateipfad."
            response = open_ai_agent(sanitized_input)
            return {
                "response": response["output"],
                "files": [],
            }

        folder_name = input_file.split("/")[0]
        input_file_path = f"{folder_name}/input.step"

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
        dl_links = generate_download_links(folder_name, output_files)

        if input_file is not None:
            sanitized_input += f" Dateipfad: {input_file_path}"

        response = open_ai_agent(sanitized_input)
        return {
            "response": response["output"],
            "files": dl_links,
        }
    except Exception as e:
        logging.error(f"Error in running the chain: {str(e)}")
        return None
