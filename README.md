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
OPENAI_API_KEY=your_openapi_key
```


3. Run the app
```bash
uvicorn main:app --reload
```

Now, the server should be up and running at http://localhost:8000. You can view the interactive API documentation at http://localhost:8000/docs.

To test the server and run sample requests, open the openAPI page at 
```
http://localhost:8000/docs
```

## Deploy changes to prod
Use Heroku for production:
```bash
heroku login
git push heroku main
heroku open
heroku logs --tail
```

## Run tests:
`pytest tests/test_github.py`

## Run tests through docker:
```bash
docker build -t tinygen .
docker run tinygen pytest tests/test_github.py
```

## Run tests with docker-compose:
```bash
docker-compose run app pytest tests/test_github.py
```


### Python things:
```bash
source venv/bin/activate # activate virtual env
deactive # deactivate virtual env
pip freeze > requirements.txt # update deps
```
