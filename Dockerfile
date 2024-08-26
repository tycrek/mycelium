FROM python:3.12-slim
WORKDIR /app
COPY ./ ./
RUN pip install --no-cache-dir flask pywemo schedule flask-apscheduler
CMD python wemo.py
