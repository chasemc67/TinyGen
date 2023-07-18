from dataclasses import dataclass
from typing import List
from processing_stages.find_relevant_files import get_top_n_relevent_files_for_prompt_and_repo, ProcessedGithubFile
from llm_models.openai import run_llm_chain_potential_diff_for_file

@dataclass
class SuggestedDiff:
    processedFile: ProcessedGithubFile
    diff: str


# TODO parallelize this like in find_relevant_files.py
async def get_suggested_diffs_for_prompt_and_repo(prompt: str, repo: str) -> List[SuggestedDiff]:
    processedGithubFiles = await get_top_n_relevent_files_for_prompt_and_repo(prompt, repo, 3)
    suggestedDiffs = []
    for processedFile in processedGithubFiles:
        if processedFile.llmResponse > 20:
            suggestedDiff = SuggestedDiff(processedFile, run_llm_chain_potential_diff_for_file(prompt, processedFile.originalFile.filename, processedFile.originalFile.content))
            suggestedDiffs.append(suggestedDiff)
    return suggestedDiffs