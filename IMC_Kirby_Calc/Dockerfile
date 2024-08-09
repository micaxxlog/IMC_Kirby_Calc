FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y\
    && apt-get install python3-venv -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
COPY app.py app.py
COPY templates/ templates/

RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 40000

CMD ["python", "app.py"]
