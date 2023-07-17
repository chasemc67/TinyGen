import bcrypt
from fastapi import FastAPI
from app.models import RequestRecord
from db.supabase import create_supabase_client
from langchains.openai import create_openai_llm
from integrations.github import get_github_files_and_contents

app = FastAPI()

# init supabase client
supabase = create_supabase_client()
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
def record_request(request: RequestRecord):
    try:
        # Add request into history table
        request = record_request(request, supabase)

        if request:
            print("Request recorded successfully")
        else: 
            return {"message": "Request recording failed"}
    except Exception as e:
        print("Error: ", e)
        return {"message": "Request recording failed"}

