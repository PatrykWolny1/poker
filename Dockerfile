FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip python3.12-venv build-essential

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv venv-python-poker

RUN venv-python-poker/bin/pip3 install --no-cache-dir -r /app/requirements.txt

COPY . .

CMD ["venv-python-poker/bin/python3", "main.py"]
