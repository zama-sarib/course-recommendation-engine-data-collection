FROM python:alpine as build

WORKDIR /source
COPY . /source/
RUN python3 -m venv /source/venv
RUN . /source/venv/bin/activate && \
python3 -m ensurepip --upgrade && \
python3 -m pip install -r /source/requirements.txt

FROM python:alpine as final

WORKDIR /source
COPY --from=build /source /source
CMD . /source/venv/bin/activate && python3 main.py