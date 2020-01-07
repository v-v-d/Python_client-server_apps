FROM python:3.6
COPY . /app
WORKDIR /app
RUN apt-get update \
    && apt-get install -y \
        python3 \
        python3-pyqt5
RUN pip install --upgrade pip
RUN pip install -r requirements.txt