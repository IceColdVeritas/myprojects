# Official Docker Python image becasue it has the latest bug fixes
FROM python:3.9-bullseye

RUN pip install pika

# Need this setting for Python to print
ENV PYTHONUNBUFFERED=1

# Install the application
WORKDIR /usr/src/app

COPY consumer.py .

CMD ["python", "/usr/src/app/consumer.py"]