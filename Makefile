.PHONY: clean
clean: 
	rm .coverage* || true
	rm coverage*.xml || true
	rm -fr htmlcov || true
	rm -fr dist || true
	rm -fr .pytest_cache || true
	find . -name __pycache__ -exec rm -fr {} \; || true

.PHONY: install
install:
	poetry install

.PHONY: check
check: 
	poetry check

.PHONY: cov
cov: 
	poetry run coverage run

.PHONY: report
report: 
	poetry run coverage report

.PHONY: html
html: 
	poetry run coverage html

.PHONY: xml
xml: 
	poetry run coverage xml

.PHONY: build
build: 
	poetry build

.PHONY: publish
publish: 
	poetry publish -u __token__ -p "$(PYPI_API_TOKEN)"

# Run python interactive
.PHONY: python
python: 
	poetry run python

# Echo activte command, need to then manually cope & paste
.PHONY: act
act: 
	poetry env activate

# Deactivate virtual env
.PHONY: deact
deact: 
	deactivate

# Create & populate virtual env
.PHONY: mvenv
mvenv: 
	poetry env use 3.12.7
	poetry install 

# Remove virtual env
.PHONY: rmvenv
rmvenv: 
	rm -fr .venv || true

.PHONY: req
req: 
	poetry export --without-hashes -f requirements.txt | cut -d ';' -f1 > requirements.txt

.PHONY: image
image: 
	docker build -t devtools .

.PHONY: up
up: 
	docker-compose up --build 

.PHONY: down
down: 
	docker-compose down

.PHONY: watch
watch: 
	docker-compose watch

.PHONY: colima
colima:
	colima stop && colima start