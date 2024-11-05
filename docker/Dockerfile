FROM python:3.9-slim

WORKDIR /app

COPY src/ /app/src/
COPY config/ /app/config/
COPY scripts/ /app/scripts/
COPY docker/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["powershell", "./scripts/data_quality_pipeline.ps1"]
