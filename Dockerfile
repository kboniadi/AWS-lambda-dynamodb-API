# Base image
FROM python:3.8

RUN useradd user

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . /app

USER root
RUN chmod +x /app/boot.sh
USER user

ENV FLASK_APP app/main.py

EXPOSE 5000

# CMD ["flask", "run"]
ENTRYPOINT ["./boot.sh"]