from typing import List
import asyncio
from dataclasses import dataclass
from llm_models.openai import run_llm_chain_find_relevant_files
from integrations.github import GithubFile, get_github_files_and_contents
import re


@dataclass
class ProcessedGithubFile:
    originalFile: GithubFile
    llmResponse: int

# Util for parsing integer number from answer
def parse_number_from_answer(answer: str) -> int:
    match = re.search(r'\d+', answer)
    if match:
        return int(match.group())
    else:
        return None

# sort list of processed files by weighted relevance and take top n results 
def get_top_n_hits_from_processed_files(processedGithubFiles: List[ProcessedGithubFile], n: int) -> List[ProcessedGithubFile]:
     # Sort the list in descending order based on the llmResponse field
    sorted_files = sorted(processedGithubFiles, key=lambda x: x.llmResponse, reverse=True)
    return sorted_files[:n]

async def process_item(item: GithubFile, userPrompt: str) -> ProcessedGithubFile:
    result = run_llm_chain_find_relevant_files(userPrompt, item.content)
    int_result =  parse_number_from_answer(result) or 0
    return ProcessedGithubFile(item, int_result)

async def process_all_items(items: List[GithubFile], userPrompt: str) -> List[ProcessedGithubFile]:
    tasks = [process_item(item, userPrompt) for item in items]
    results = await asyncio.gather(*tasks)
    return results

async def find_relevant_files_for_prompt_and_repo(prompt: str, repo: str) -> List[ProcessedGithubFile]:
    githubFiles = get_github_files_and_contents(repo)
    processedGithubFiles = await process_all_items(githubFiles, prompt)
    return processedGithubFiles


async def get_top_n_relevent_files_for_prompt_and_repo(prompt: str, repo: str, n: int) -> List[ProcessedGithubFile]:
    processedGithubFiles = await find_relevant_files_for_prompt_and_repo(prompt, repo)
    return get_top_n_hits_from_processed_files(processedGithubFiles, n)
    