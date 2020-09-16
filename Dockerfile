FROM python:3.7-alpine
WORKDIR /code
RUN apk add --no-cache gcc g++ musl-dev linux-headers postgresql-dev git
COPY server/requirements.txt server/requirements.txt
RUN pip install -r server/requirements.txt
RUN git clone "https://github.com/eficode/wait-for.git"
RUN chmod +x wait-for/wait-for
COPY server server
WORKDIR /code/server
