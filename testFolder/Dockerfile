FROM python:3

# set the working directory in the container
WORKDIR /app

COPY /app /app

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]
