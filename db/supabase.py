from supabase import Client, create_client
from config import supabase_url, supabase_api_key

url: str = supabase_url
key: str = supabase_api_key

def create_supabase_client():
    supabase: Client = create_client(url, key)
    return supabase

def record_request(request: RequestRecord, supabaseClient):
     # Add request into history table
    request = supabase.from_("request_history")\
        .insert({"url": request.url, "prompt": request.prompt, "response": ""})\
        .execute()
    return request

def update_request(requestId, response: str, supabaseClient):
    request = supabase.from_("request_history")\
        .update({"response": response})\
        .eq("id", requestId)\
        .execute()
    return request