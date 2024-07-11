FROM python:3.12.3

LABEL version="0.1"

LABEL authors="wagner"

ENV PYTHONPATH="/app/src"

ENV PYTHONDONTWRITEBYTECODE="false"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000/tcp

CMD [ "gunicorn", "--preload", "src.app:app" ]
