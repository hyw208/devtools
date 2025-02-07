# devtools
devtools

# pre-requisites 
1. python 3.12
2. make
3. poetry
4. docker & docker-compose

# add deps 
1. poetry add "fastapi[standard]" 
2. poetry add pytest coverage flake8 mypy black --group dev

# to run pytest coverage and generate xml and html
1. make install cov report xml html

# to run 
1. python devtools/api.py
2. uvicorn devtools.api:app --host 0.0.0.0 
3.  
