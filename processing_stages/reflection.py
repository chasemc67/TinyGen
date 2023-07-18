from typing import List
from processing_stages.generate_diff import get_suggested_diffs_for_prompt_and_repo, SuggestedDiff
from llm_models.openai import run_llm_chain_reflection

def concatenate_diffs(suggestedDiffs: List[SuggestedDiff]) -> str:
    formatted_diffs = []
    for file in suggestedDiffs:
        formatted_diffs.append(f"Filename: {file.processedFile.originalFile.filename}\n```\n{file.diff}\n```")
    return "\n\n".join(formatted_diffs)

def get_yes_or_no_from_reflection_response(response: str) -> bool:
    return 'yes' in response.lower()

async def get_suggested_diffs_for_prompt_and_repo_with_reflection(prompt: str, repo: str, iterations: int) -> List[SuggestedDiff]:
    attemptedIterations = 0
    llmSatisfied = False

    currentRespone: SuggestedDiff = None

    while (not llmSatisfied) and (attemptedIterations < iterations):
        currentRespone = await get_suggested_diffs_for_prompt_and_repo(prompt, repo)
        reflectionResponse = run_llm_chain_reflection(prompt, concatenate_diffs(currentRespone))
        
        if get_yes_or_no_from_reflection_response(reflectionResponse):
            llmSatisfied = True
            break
        print("Reflection not satisfied, trying again...")
        attemptedIterations += 1

    return currentRespone