# syntax=docker/dockerfile:1
FROM python:3.7.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && apt-get -y install cmake build-essential python3-dev libevent-dev gcc g++ wget
RUN pip3 install -U pip
RUN pip3 install https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.2.0/en_core_web_lg-3.2.0.tar.gz
RUN pip3 install -U -r requirements.txt
#RUN sudo python3 -m spacy download en_core_web_lg
EXPOSE 80
COPY . /code/
#CMD ["gunicorn", "-b", "0.0.0.0:80", "falconapp:app"]
CMD ["python", "falconapp.py"]
