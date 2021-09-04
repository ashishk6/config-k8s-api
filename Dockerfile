FROM python:3.9.6-slim-buster
RUN  pip install flask
COPY run_config.py /app/run_config.py
WORKDIR /app
CMD ["python", "run_config.py"]
