FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 4732

# Copy the .env file if it exists
# COPY .env* ./

CMD ["python", "app.py"]