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
    template="You will be given a userPrompt and a string of conent. You must return a number between 0 and 100 for how likely you think the content is related to the user prompt. The only output you should respond with is the single number between 0 and 100. The higher the nubmer, the more likely the content is relevant to satisfy the prompt. userPrompt: {userPrompt} content: {content}"
)

def create_openai_llm():
    return OpenAI(openai_api_key=key, temperature=0.1)

def create_llm_agent():
    llm = create_openai_llm()
    tools = load_tools(["llm-math"], llm=llm)
    agent = initialize_agent(llm=llm, tools=tools, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    response = agent.run("what is the square root of 123531")
    print("Agent Respone: ", response)


def run_llm_chain_for_input(userPrompt: str, content: str) -> str:
    llm = create_openai_llm()
    llmchain = LLMChain(llm=llm, prompt=prompt)
    return llmchain.run({
        'userPrompt': userPrompt,
        'content': content
    })