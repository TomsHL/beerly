FROM python:3.8.12-buster

COPY raw_data /raw_data
COPY models /models

COPY api /api

#RUN export LC_ALL=C


RUN pip install --upgrade pip

RUN apt-get update \
    && apt-get install tesseract-ocr -y \
    libtesseract-dev \
    tesseract-ocr-eng \
    tesseract-ocr-script-latn \
    && apt-get clean \
    && apt-get autoremove

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt


#RUN export PYTHONIOENCODING="UTF-8"
COPY beerly /beerly

CMD uvicorn api.fast:app --reload --host 0.0.0.0 --port $PORT
