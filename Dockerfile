FROM python:3-alpine3.15

WORKDIR /corider
COPY . /corider

RUN pip install -r requirements.txt

ENV PORT 5000

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD ["main.py"]