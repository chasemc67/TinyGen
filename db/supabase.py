from supabase import Client, create_client
from config import supabase_url, supabase_api_key

url: str = supabase_url
key: str = supabase_api_key

def create_supabase_client():
    supabase: Client = create_client(url, key)
    return supabase