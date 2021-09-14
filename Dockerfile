FROM python:3.8-alpine
WORKDIR /code
COPY . /code
COPY db/ /code/db/
RUN ls -la /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV SQL_HOST=localhost
ENV SQL_USER=harmeet
ENV SQL_PASS=welcome@123
ENV SQL_DB_NAME=wiki_db

ENV REDIS_HOST=localhost
ENV REDIS_PORT=6379
ENV REDIS_DB_NAME=0


RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]
