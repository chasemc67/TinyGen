# TinyGen

A simple API to generate code diffs using ChatGPT

## Running the Application Locally

1. First, clone the repository to your local machine and navigate to the project directory:

```bash
git clone <repository-url>
cd <project-directory>
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Now, the server should be up and running at http://localhost:8000. You can view the interactive API documentation at http://localhost:8000/docs.

To get out of the virtual env run
```
deactivate
```

To test your server, you can run the following CURL command:
```
curl -X POST "http://localhost:8000/concatenate/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"string1\":\"Hello\",\"string2\":\"World\"}"
```


## Supabase Config
Create a `config.py` file which looks like the following:
```
url="https://abc.supabase.co"
api="dummy-api"
```

Get this information from [supabase](https://supabase.com/dashboard/project/fvvmbtjoztejtalynctc/settings/api), and see [this tutorial](https://blog.theinfosecguy.xyz/building-a-crud-api-with-fastapi-and-supabase-a-step-by-step-guide) for more info