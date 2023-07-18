from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import openai_api_key

key: str = openai_api_key

# TODO create singleton class here like with the DB client?
def create_openai_llm():
    return OpenAI(openai_api_key=key, temperature=0)

# TODO this prompt should probably be either generated or modified by some chain-of-thought reasoning
# specifically if the agent was give a task of "adding a route", I'd expect it to be able to come up with
# the step "i need to find where the routes are defined" as part of its reasoning process
# and that could inform this prompt. 
find_relevant_files_prompt = PromptTemplate(
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
def run_llm_chain_find_relevant_files(userPrompt: str, content: str) -> str:
    llm = create_openai_llm()
    llmchain = LLMChain(llm=llm, prompt=find_relevant_files_prompt)
    return llmchain.run({
        'userPrompt': userPrompt,
        'content': content[:5000]
    })



generate_potential_diff_for_file_prompt = PromptTemplate(
    input_variables=["userPrompt", "fileName", 'fileContent'],
    template="""
    Role: Software Engineering Expert. Suggests per-file code changes to server a large goal.
    We are trying to make a large code change, and we've narrowed down which files we 
    think will require changes. 
    
    You will be given a description of the overarching code change, and then one file at a time. 

    If you think the supplied file should be changed, respond with the change. Otherwise, respond with nothing.

    problem:
    ```
    {userPrompt}
    ```

    fileName:
    ```
    {fileName}
    ```

    code:
    ```
    {fileContent}
    ```

    If you think this file should be changed, answer with only a code block representing the change. Otherwise, answer with nothing.

    Answer: 
    """
)

def run_llm_chain_potential_diff_for_file(userPrompt: str, fileName: str, content: str) -> str:
    llm = create_openai_llm()
    llmchain = LLMChain(llm=llm, prompt=generate_potential_diff_for_file_prompt)
    return llmchain.run({
        'userPrompt': userPrompt,
        'fileName': fileName,
        'fileContent': content[:5000]
    })