from fastapi import FastAPI
from fastapi import HTTPException
from app.models import RequestRecord
from db.supabase import supabase_record_request
from processing_stages.generate_diff import get_suggested_diffs_for_prompt_and_repo
from integrations.github import validate_url

app = FastAPI()

@app.post("/generate", responses={400: {"description": "Invalid URL"}, 500: {"description": "Internal Server Error"}})
async def generate(request: RequestRecord):

    if not validate_url(request.url):
        raise HTTPException(status_code=400, detail="Invalid Github URL, use a pattern like https://github.com/chasemc67/TinyGen")
    if len(request.prompt) > 10000:
        raise HTTPException(status_code=400, detail="Prompt too large")

    try:
        # Add request into history table
        supabase_request = supabase_record_request(request)

        if supabase_request:
            print("Request recorded successfully")
        else: 
            raise HTTPException(status_code=500, detail="Request recording failed")
    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=500, detail="Request recording failed")

    results = await get_suggested_diffs_for_prompt_and_repo(request.prompt, request.url)

    formatted_results = [{"filename": result.processedFile.originalFile.filename, "diff": result.diff} for result in results]
    #TODO update the request record in supabase with the response

    return {"results": formatted_results}
