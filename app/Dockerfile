FROM python:3.9

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libev-dev \
    libffi-dev \
    python3-dev \
    && gcc --version \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]