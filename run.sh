#!/bin/bash

# Clone the repository
git clone https://github.com/chasemc67/TinyGen.git /repo

# Change directory to the repo
cd /repo

# Run the docker-compose command
docker-compose run app pytest tests/