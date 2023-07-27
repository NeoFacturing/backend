import os
import openai
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI

load_dotenv()
openai.api_type = "azure"
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_version = os.getenv('OPENAI_API_VERSION')
chatgpt = AzureChatOpenAI(deployment_name="neofacturing-gpt-35-turbo")
