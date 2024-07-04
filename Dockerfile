FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN addgroup --gid 10001 user && adduser --ingroup user --disabled-login --uid 10001 user

WORKDIR /app

RUN chown -R user /app
COPY app/requirements.txt /app/
RUN pip install -r requirements.txt

COPY --chown=user app/ /app/

USER user

RUN #mkdir -p /app/image_builder_kafka/static && ./manage.py collectstatic --noinput

EXPOSE 8000

#CMD ["gunicorn image_builder_kafka.asgi:application -k uvicorn.workers.UvicornWorker -b :8080 -w 1 --chdir /app --timeout 120 --threads 4"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

