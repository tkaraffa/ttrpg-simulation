FROM python:3.8.10-slim

WORKDIR /src
ENV PYTHONPATH=/src

COPY requirements.txt /src/requirements.txt
RUN pip install --user -r requirements.txt

COPY src ./
ENTRYPOINT [ "python" ]