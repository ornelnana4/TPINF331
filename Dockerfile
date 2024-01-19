FROM python:3.8  

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app/

RUN apt-get upgrade && pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python3","manage.py","runserver","0.0.0.0:8000"]