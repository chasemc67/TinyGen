# TinyGen

A simple API to generate code diffs using ChatGPT

## Running the Application Locally

1. First, clone the repository to your local machine and navigate to the project directory:

```bash
git clone <repository-url>
cd <project-directory>
source venv/bin/activate
pip install -r requirements.txt
```

Teardown:
```bash
deactivate
```

2. create a new .env file for secrets, you can get this information from [supabase](https://supabase.com/dashboard/project/fvvmbtjoztejtalynctc/settings/api)
your .env file should look like this:
```
SUPABASE_URL=your_supabase_url
SUPABASE_API_KEY=your_supabase_api_key
```


3. Run the app
```bash
uvicorn main:app --reload
```

Now, the server should be up and running at http://localhost:8000. You can view the interactive API documentation at http://localhost:8000/docs.

To test your server, you can run the following CURL command:
```bash
curl http://localhost:8000/test
```

To make a proper request to generate a response, and record the input and output in supabase, run the following CURL
```bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "yourgitrepo.url", "prompt": "your prompt"}' http://127.0.0.1:8000/generate
```


## Deploy changes to prod
Use Heroku for production:
```bash
heroku login
git push heroku main
heroku open
heroku logs --tail
```


### Python things:
```bash
source venv/bin/activate # activate virtual env
deactive # deactivate virtual env
pip freeze > requirements.txt # update deps
```