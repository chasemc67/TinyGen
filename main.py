import bcrypt
from fastapi import FastAPI
from app.models import User, Item
from db.supabase import create_supabase_client

app = FastAPI()

# init supabase client
supabase = create_supabase_client()

def user_exists(key: str = "email", value: str = None):
    user = supabase.from_("users").select("*").eq(key, value).execute()
    return len(user.data) > 0

# Create a new user 
@app.post("/user")
def create_user(user: User):
    try:
        # Convert the email to lowercase
        user_email = user.email.lower()
        # hash password 
        hashed_password = bcrypt.hashpw(user.password, bcrypt.gensalt())

        # check if user already exists
        if user_exists(value=user_email):
            return {"message": "User already exists"}
        
        # Add user into users table
        user = supabase.from_("users")\
            .insert({"name": user.name, "email": user_email, "password": hashed_password})\
            .execute()

        if user:
            return {"message": "User created successfully"}
        else: 
            return {"message": "User creation failed"}
    except Exception as e:
        print("Error: ", e)
        return {"message": "User creation failed"}

@app.post("/concatenate/")
async def concatenate_strings(item: Item):
    result = item.string1 + item.string2
    return {"result": result}