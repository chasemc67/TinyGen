# Use an official Python runtime as the base image
# break dockerfile for test
FROM 219620959316.dkr.ecr.us-east-1.amazonaws.com/ramp-base-images/python-3.10-slim-bullseye:2023-09-26.0

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /app
COPY . .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Set default environment variables (can be overridden)
# These are placeholders and should be set to actual values when running the container
ENV SUPABASE_URL=default_supabase_url
ENV SUPABASE_API_KEY=default_supabase_api_key
ENV OPENAI_API_KEY=default_openai_key

# Make port 8000 available to the world outside the container
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
