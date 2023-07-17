import bcrypt
from fastapi import FastAPI
from app.models import RequestRecord
from db.supabase import create_supabase_client

app = FastAPI()

# init supabase client
supabase = create_supabase_client()

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
