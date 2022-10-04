FROM python:3.10-slim-buster

WORKDIR /home/app/Flak-RestFul-SQLAlchemy

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python3","app.py"]