FROM python:3.5.5-slim

ENV GOOGLE_APPLICATION_CREDENTIALS /usr/src/app/Xin-Wang-de9a9df354bb.json

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt gunicorn
EXPOSE 8080

COPY . .

CMD ["gunicorn","app:app"]
