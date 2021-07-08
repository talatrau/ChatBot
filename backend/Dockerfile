FROM python:3.8

WORKDIR /django

COPY . .

RUN pip install --upgrade pip \
    && pip install -r req.txt

EXPOSE 8000

CMD python manage.py migrate \
    && python manage.py runserver 0.0.0.0:8000
