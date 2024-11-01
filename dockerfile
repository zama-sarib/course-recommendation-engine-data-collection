FROM python:3.9.14-slim-bullseye

COPY . /recommendationengine

WORKDIR /recommendationengine

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8080

CMD ["python","main.py"]