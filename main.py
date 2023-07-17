from fastapi import FastAPI
from app.models import RequestRecord
from db.supabase import supabase_record_request
from langchains.openai import create_openai_llm
from integrations.github import get_github_files_and_contents
from app.generate_diff import get_suggested_diffs_for_prompt_and_repo

app = FastAPI()

llm = create_openai_llm()

@app.get("/test")
def read_test():
    return {"message": "hello"}

@app.get("/testllm")
def test_llm():
    return llm.predict("What is a cool name for a dog?")

@app.get("/testgithub")
def test_github():
    return get_github_files_and_contents('https://github.com/chasemc67/TinyGen')

# Append to the history table log
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

    result = await get_suggested_diffs_for_prompt_and_repo(request.prompt, request.url)

    #TODO update the request record with the response

    #TODO format the message better
    return {"message": result[0].diff}
