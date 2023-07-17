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
def generate(request: RequestRecord):
    try:
        # Add request into history table
        request = supabase_record_request(request)

        if request:
            print("Request recorded successfully")
        else: 
            return {"message": "Request recording failed"}
    except Exception as e:
        print("Error: ", e)
        return {"message": "Request recording failed"}

    # TODO get files from github to pass to LLM (or invoke LLM now with custom github tool)

    return {"message": "Request recording succeeded"}


@app.get("/testendtoend")
async def testEndToEnd():
    result = await get_suggested_diffs_for_prompt_and_repo("Add a new app.get route called CoolDogs which returns the string \"Finley\"", "https://github.com/chasemc67/TinyGen")
    return {"message": result[0].diff}