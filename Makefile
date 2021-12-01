# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* beerly/*.py


clean:
	@rm -f */version.txt
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr beerly-*.dist-info
	@rm -fr beerly.egg-info

install:
	@pip install . -U

all: clean install check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#         GCP API Deploy
# ----------------------------------
# project id
PROJECT_ID=xxxx

build_docker:
	-@docker build -t eu.gcr.io/${PROJECT_ID}/${DOCKER_IMAGE_NAME} .

run_docker:
#	docker run -e PORT=1234 -p 8000:1234 eu.gcr.io/${PROJECT_ID}/${DOCKER_IMAGE_NAME}
	docker run -e PORT=8000 -p 8080:8000 beerly0
run_it:
	docker run -it -e PORT=1234 -p 8000:1234 eu.gcr.io/${PROJECT_ID}/${DOCKER_IMAGE_NAME} sh

push_docker:
	-@docker push eu.gcr.io/${PROJECT_ID}/${DOCKER_IMAGE_NAME}

configure_api:
	gcloud config set project ${PROJECT_ID}

deploy_api:
	-@gcloud run deploy \
			--image eu.gcr.io/${PROJECT_ID}/${DOCKER_IMAGE_NAME} \
			--platform managed \
			--region europe-west1 \
			--set-env-vars "GOOGLE_APPLICATION_CREDENTIALS=/credentials.json" \
			--memory '4Gi'

# ----------------------------------
#             API
# ----------------------------------

run_api:
	uvicorn api.fast:app --reload
