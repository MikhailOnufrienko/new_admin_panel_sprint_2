FROM python:3.10.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240

WORKDIR /app

RUN pip install --upgrade pip

RUN groupadd -r djus && useradd -d /app -r -g djus djus \
    && chown djus:djus -R /app

RUN mkdir /app/static && mkdir /app/media

RUN pip install --no-cache-dir -r requirements.txt

COPY run_uwsgi.sh run_uwsgi.sh
COPY uwsgi/uwsgi.ini uwsgi.ini

COPY . .


ENTRYPOINT ["uwsgi", "--strict", "--ini", "uwsgi.ini"]

