FROM python:3.5.5-slim

ENV GOOGLE_APPLICATION_CREDENTIALS /usr/src/app/Xin-Wang-de9a9df354bb.json
ENV NUTRITIONIX_KEY <nutritionix-api-key>
ENV NUTRITIONIX_APP_ID <nutritionix-application-id>

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt
EXPOSE 8080
EXPOSE 8000

COPY . .

CMD ["gunicorn","app:app"]
