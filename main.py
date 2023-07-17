import bcrypt
from fastapi import FastAPI
from app.models import RequestRecord
from db.supabase import create_supabase_client
from langchain.openai import create_openai_llm
from integtations.github.github import get_github_files_and_contents

app = FastAPI()

# init supabase client
supabase = create_supabase_client()
llm = create_openai_llm()

@app.get("/test")
def read_test():
    return {"message": "hello"}

@app.get("test-llm")
def test_llm():
    return llm.predict("What is a cool name for a dog?")

@app.get("test-github")
def test_github():
    return get_github_files_and_contents('https://github.com/chasemc67/TinyGen')

# Append to the history table log
@app.post("/generate")
def record_request(request: RequestRecord):
    try:
        # Add request into history table
        request = supabase.from_("request_history")\
            .insert({"url": request.url, "prompt": request.prompt, "response": ""})\
            .execute()

        if request:
            return {"message": "Request recorded successfully"}
        else: 
            return {"message": "Request recording failed"}
    except Exception as e:
        print("Error: ", e)
        return {"message": "Request recording failed"}

