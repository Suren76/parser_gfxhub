FROM python:3.11-slim
ADD . /project
RUN pip3 install -r /project/requirements.txt
RUN apt-get update
RUN apt-get install -y wget

ENTRYPOINT ["python", "/project/app.py"]
