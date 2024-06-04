FROM python:3.8-slim

WORKDIR /app

COPY log_service.py /app/log_service.py
RUN pip install docker bottle

CMD ["python", "log_service.py"]
