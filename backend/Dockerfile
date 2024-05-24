FROM python:3.9-slim

WORKDIR /app

COPY . /app

# Installation des dépendances nécessaires par notre API
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]