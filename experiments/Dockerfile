FROM python:3.12-slim

WORKDIR /app

COPY experiments/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir "setuptools<81" && \
    pip install --no-cache-dir -r requirements.txt

COPY experiments /app/experiments

CMD ["python", "experiments/train_and_push.py"]