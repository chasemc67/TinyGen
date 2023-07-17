from langchain.llms import OpenAI
from config import openai_api_key

key: str = openai_api_key

def create_openai_llm():
    return OpenAI(openai_api_key=key, temperature=0.9)