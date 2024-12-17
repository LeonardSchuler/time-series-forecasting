.PHONY: all build clean docs lint install venv venvdev
all: requirements/main.txt requirements/dev.txt docs


# Check if MLFLOW_TRACKING_SERVER is already set in the environment
ifneq ($(origin MLFLOW_TRACKING_SERVER_DOMAIN), environment)
    MLFLOW_TRACKING_SERVER_DOMAIN := localhost
endif

# Check if MLFLOW_TRACKING_SERVER_PORT is already set in the environment
ifneq ($(origin MLFLOW_TRACKING_SERVER_PORT), environment)
    MLFLOW_TRACKING_SERVER_PORT := 5000
endif

clean:
	@echo "Cleaning up..."
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -vrf {} \; 2>/dev/null
	python setup.py clean --all
	@echo "Done."

lint:
	@echo "Running linter..."
	mypy src/

tracking:
	mlflow server --host ${MLFLOW_TRACKING_SERVER_DOMAIN} --port ${MLFLOW_TRACKING_SERVER_PORT}

requirements/main.txt: requirements/main.in
	@echo "Generating requirements/main.txt from requirements/main.in..."
	cd requirements && pip-compile --output-file main.txt main.in
	@echo "Done."

requirements/dev.txt: requirements/dev.in requirements/main.in
	@echo "Generating requirements/dev.txt from requirements/dev.in..."
	cd requirements && pip-compile --output-file dev.txt dev.in
	@echo "Done."

venvdev:
	python3 -m venv .venv
	source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements/dev.txt && pip install -e .

docs:
	@echo "Generating documentation as html..."
	@$(MAKE) -C docs html
	open ./docs/_build/html/index.html
	@echo "Find documentation here: ./docs/_build/html/index.html"
	@echo "Done."

build:
	@echo "Building..."
	python setup.py sdist bdist_wheel
	python setup.py clean --all
	@echo "Done."

s3package: build
	@echo "Uploading to S3..."
	mkdir -p dist/utils
	mv dist/*.whl dist/utils
	aws --region us-east-1 s3 sync --delete dist/utils s3://aws-bucket/utils
	@echo "URL: https://s3.console.aws.amazon.com/s3/buckets/aws-bucket?region=us-east-1&prefix=utils/"
	@echo "Done."
