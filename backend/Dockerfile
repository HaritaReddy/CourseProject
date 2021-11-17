# syntax=docker/dockerfile:1
FROM python:3.7.0
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && apt-get -y install cmake
RUN pip3 install -r requirements.txt
EXPOSE 80
COPY . /code/
CMD ["gunicorn", "-b", "0.0.0.0:80", "falconapp:app"]
