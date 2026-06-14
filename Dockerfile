FROM python:3.11-slim

WORKDIR /opt/pipeline
COPY requirements.txt /opt/pipeline/requirements.txt
RUN pip install --no-cache-dir -r /opt/pipeline/requirements.txt
COPY . /opt/pipeline

CMD ["python", "-m", "unittest", "discover", "-s", "tests", "-v"]
