FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN useradd -m myuser && chown -R myuser:myuser /app
USER myuser

COPY app/requirements.txt /app

RUN python -m venv venv
    
ENV PATH="/app/venv/bin:/home/myuser/.local/bin:$PATH"

RUN  pip install --upgrade pip &&  \
     pip install --trusted-host pypi.python.org -r requirements.txt

COPY app/ /app

CMD ["python", "worker.py"]