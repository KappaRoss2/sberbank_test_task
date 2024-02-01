FROM python:3.9
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /usr/src/app/requirements.txt
WORKDIR /usr/src/app

RUN pip3 install -r requirements.txt

COPY . /usr/src/app

EXPOSE 8000