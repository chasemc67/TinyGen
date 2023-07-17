from dotenv import load_dotenv
import os

load_dotenv() # load local .env file if it exists for local development

supabase_url = os.getenv("SUPABASE_URL")
supabase_api_key = os.getenv("SUPABASE_API_KEY")