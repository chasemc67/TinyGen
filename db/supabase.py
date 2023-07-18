from supabase import create_client
from config import supabase_url, supabase_api_key
from app.models import RequestRecord

url: str = supabase_url
key: str = supabase_api_key

class SupabaseClient:
    _instance = None

    def __init__(self):
        if SupabaseClient._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SupabaseClient._instance = create_client(url, key)

    @staticmethod
    def get_instance():
        if SupabaseClient._instance is None:
            SupabaseClient()
        return SupabaseClient._instance


def supabase_record_request(request: RequestRecord):
    supabase = SupabaseClient.get_instance()
     # Add request into history table
    request = supabase.from_("request_history")\
        .insert({"url": request.url, "prompt": request.prompt, "response": ""})\
        .execute()
    return request

def supabase_update_request(requestId, response: str):
    supabase = SupabaseClient.get_instance()
    request = supabase.from_("request_history")\
        .update({"response": response})\
        .eq("id", requestId)\
        .execute()
    return request