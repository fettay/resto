FROM python:3.7-alpine
WORKDIR /code
RUN apk add --no-cache gcc g++ musl-dev linux-headers postgresql-dev
COPY server/requirements.txt server/requirements.txt
RUN pip install -r server/requirements.txt
COPY server server
WORKDIR /code/server
