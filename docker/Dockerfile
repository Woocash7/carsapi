FROM python:latest

RUN mkdir /app
COPY . /app
WORKDIR /app
RUN chmod +x /app/docker/docker_prod.sh
ENTRYPOINT ["sh", "/app/docker/docker_prod.sh"]

RUN pip install --upgrade pip setuptools wheel

RUN pip install -r requirements.txt
