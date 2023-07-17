from typing import List
import asyncio
from dataclasses import dataclass
from langchains.openai import run_llm_chain_for_input
from integrations.github import GithubFile, get_github_files_and_contents


@dataclass
class ProcessedGithubFile:
    originalFile: GithubFile
    llmResponse: str


# Define the function you want to run on each object:
async def process_item(item: GithubFile, userPrompt: str) -> ProcessedGithubFile:
    # This is a placeholder function that doesn't do much.
    # Replace it with whatever function you want to run.
    # await asyncio.sleep(1)  # simulate IO delay
    # return ProcessedGithubFile(item, f"Processed {item.filename} with code {item.content}")
    #return f"Processed {item.filename} with code {item.content}"

    result = run_llm_chain_for_input(userPrompt, item.content)
    return ProcessedGithubFile(item, result)



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