FROM python:latest

WORKDIR user/src/app
RUN pip install --upgrade pip

COPY ./reqs.txt .

RUN pip install -r ./reqs.txt

COPY . .

CMD ["python3", "/user/src/app/manage.py", "makemigrations"]
CMD ["python3", "/user/src/app/manage.py", "migrate"]
CMD ["python3", "/user/src/app/manage.py", "runserver", "0.0.0.0:8000"]