import warnings
from langchain_community.chat_models import ChatGooglePalm
from dotenv import load_dotenv
import os

from langchain_core._api import LangChainDeprecationWarning

warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

load_dotenv()

api_key = os.getenv('GEMINI')


chat_model = ChatGooglePalm(google_api_key=api_key)

result = chat_model.invoke("hi")

# Extracting content from result
content = result.content

# Printing the result
print(content)
