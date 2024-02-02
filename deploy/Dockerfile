FROM python:3.9

RUN apt-get update && apt-get install -y wait-for-it

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SECRET_KEY=z421@-_rnnw^t+@_xgjpwtfvpsy-xyp22d*j3ywhhko_(5lvd2
COPY requirements.txt /usr/src/app/requirements.txt
WORKDIR /usr/src/app

RUN pip3 install -r requirements.txt

COPY . /usr/src/app

EXPOSE 8000