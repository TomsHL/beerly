FROM python:3.8.12-buster

COPY beerly /beerly
COPY raw_data/dataset_cleaned /raw_data/dataset_cleaned
COPY raw_data/dataset_reviews /raw_data/dataset_reviews
COPY raw/data/dataset_light /raw_data/dataset_light
COPY requirements.txt /requirements.txt
COPY api /api

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
