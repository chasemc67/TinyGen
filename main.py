from fastapi import FastAPI
from app.models import RequestRecord
from db.supabase import supabase_record_request
from langchains.openai import create_openai_llm
from integrations.github import get_github_files_and_contents
from app.generate_diff import get_suggested_diffs_for_prompt_and_repo

app = FastAPI()

@app.post("/generate")
async def generate(request: RequestRecord):
    try:
        # Add request into history table
        supabase_request = supabase_record_request(request)

        if supabase_request:
            print("Request recorded successfully")
        else: 
            return {"message": "Request recording failed"}
    except Exception as e:
        print("Error: ", e)
        return {"message": "Request recording failed"}

    results = await get_suggested_diffs_for_prompt_and_repo(request.prompt, request.url)

    #TODO update the request record with the response


    formatted_results = [{"filename": result.originalFile.filename, "diff": result.diff} for result in results]
    return {"results": formatted_results}
