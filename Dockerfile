FROM python:alpine3.8

WORKDIR /corider
COPY . /corider

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python ./main.py