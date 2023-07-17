from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from config import openai_api_key

key: str = openai_api_key

prompt = PromptTemplate(
    input_variables=["userPrompt", "content"],
    template="""
    Role: Software Engineer Assistant, makes no code changes. Only finds relevant code to be changed later.
    You will be given a userPrompt and a string of code. 
    The userPrompt is the larger change we're trying to make, and the code is a single file.
    Your job is to find which files will likely be part of the larger change.
    
    You must return a number between 0 and 100 for how likely you think this code will need to be modified as part of the larger change. 
    The only output you should respond with is the single number between 0 and 100. The higher the nubmer, the more likely the content is relevant to satisfy the prompt. 
    
    userPrompt: 
    ```
    {userPrompt} 
    ```
    
    code: 
    ```
    {content}
    ```

    Answer:
    """
)


def create_openai_llm():
    return OpenAI(openai_api_key=key, temperature=0)


def run_llm_chain_for_input(userPrompt: str, content: str) -> str:
    llm = create_openai_llm()
    llmchain = LLMChain(llm=llm, prompt=prompt)
    return llmchain.run({
        'userPrompt': userPrompt,
        'content': content
    })