FROM python:3.10.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240

WORKDIR /app

RUN apt update && apt -y install netcat postgresql

RUN pip install --upgrade pip

RUN groupadd -r djus && useradd -d /app -r -g djus djus \
    && chown djus:djus -R /app

RUN mkdir /app/static && mkdir /app/media

COPY run_uwsgi.sh /app/
COPY uwsgi/uwsgi.ini /app/
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod -R 775 /app/run_uwsgi.sh

ENTRYPOINT ["/app/run_uwsgi.sh"]

