from typing import List
import asyncio
from dataclasses import dataclass
from langchains.openai import run_llm_chain_for_input
from integrations.github import GithubFile, get_github_files_and_contents
import re


@dataclass
class ProcessedGithubFile:
    originalFile: GithubFile
    llmResponse: int


# Define the function you want to run on each object:
async def process_item(item: GithubFile, userPrompt: str) -> ProcessedGithubFile:
    # This is a placeholder function that doesn't do much.
    # Replace it with whatever function you want to run.
    # await asyncio.sleep(1)  # simulate IO delay
    # return ProcessedGithubFile(item, f"Processed {item.filename} with code {item.content}")
    #return f"Processed {item.filename} with code {item.content}"

    result = run_llm_chain_for_input(userPrompt, item.content)
    int_result =  parse_number_from_answer(result) or 0
    return ProcessedGithubFile(item, int_result)


def parse_number_from_answer(answer: str) -> int:
    match = re.search(r'\d+', answer)
    if match:
        return int(match.group())
    else:
        return None


# TODO since I think this syntax is dependent on the python version
# We should find a way to define it such that heroku and local development will respect/enforce it
async def process_all_items(items: List[GithubFile], userPrompt: str) -> List[ProcessedGithubFile]:
    # Create a list of tasks to run:
    tasks = [process_item(item, userPrompt) for item in items]

    # Run the tasks:
    #loop = asyncio.get_event_loop()
    # results = loop.run_until_complete(asyncio.gather(*tasks))
    results = await asyncio.gather(*tasks)

    # Do something with the results:
    return results

async def find_relevant_files_for_prompt_and_repo(prompt: str, repo: str) -> List[ProcessedGithubFile]:
    githubFiles = get_github_files_and_contents(repo)
    processedGithubFiles = await process_all_items(githubFiles, prompt)

    print(processedGithubFiles)
    return processedGithubFiles

def get_top_n_hits_from_processed_files(processedGithubFiles: List[ProcessedGithubFile], n: int) -> List[ProcessedGithubFile]:
     # Sort the list in descending order based on the llmResponse field
    sorted_files = sorted(processedGithubFiles, key=lambda x: x.llmResponse, reverse=True)
    return sorted_files[:n]


async def get_top_n_relevent_files_for_prompt_and_repo(prompt: str, repo: str, n: int) -> List[ProcessedGithubFile]:
    processedGithubFiles = await find_relevant_files_for_prompt_and_repo(prompt, repo)
    return get_top_n_hits_from_processed_files(processedGithubFiles, n)