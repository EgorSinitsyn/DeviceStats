FROM python:3.9

WORKDIR /tests


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["locust", "-f", "locustfile.py", "--host", "http://app:8000"]