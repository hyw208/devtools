# devtools
devtools

# pre-requisites 
1. python 3.12
2. make
3. poetry
4. docker & docker-compose

# add deps 
1. > poetry add "fastapi[standard]" 
2. > poetry add pytest coverage flake8 mypy black --group dev

# to run pytest coverage and generate xml and html
1. > make install cov report xml html

# to run 
1. > python devtools/api.py
2. > uvicorn devtools.api:app --host 0.0.0.0 
3. > docker-compose up
4. > make up
5. 

# to build image
1. > docker build -t devtools . 

# export deps to requirements.txt ** need to install poetry export plug-in
1. > poetry export --without-hashes -f requirements.txt | cut -d ';' -f1 > requirements.txt

# docker for mac 
1. ref https://smallsharpsoftwaretools.com/tutorials/use-colima-to-run-docker-containers-on-macos/
2. mac docker -> colima
3. > colima start
4. > docker context use colima


# docker-compose 
1. > docker-compose up

# docker exec 
1. docker exec -it <container name> bash 
   
# further reading 
1. error handling https://ankurdhuriya.medium.com/handling-failures-in-celery-workers-retries-timeouts-and-error-handling-97571b131267

2. add db https://github.com/alperencubuk/fastapi-celery-redis-postgres-docker-rest-api/blob/main/api/main.py

3. chaining & grouping & chording 
   a. https://mazaherian.medium.com/mastering-task-orchestration-with-celery-exploring-groups-chains-and-chords-991f9e407a4f
   b. https://docs.celeryq.dev/en/stable/userguide/canvas.html

