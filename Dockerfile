FROM python:3.8-alpine

COPY requirements.txt /opt/app/
COPY app/ /opt/app/

RUN apk --update add gcc build-base libffi-dev gcc musl-dev make && \
    pip3 install -r /opt/app/requirements.txt

WORKDIR /opt/app

CMD python3 /opt/app/app.py
