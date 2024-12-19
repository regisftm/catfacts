FROM python:3.12.1-slim

WORKDIR /app

RUN python -m venv venv
    
ENV PATH="/app/venv/bin:/root/.local/bin:$PATH"

COPY app/requirements.txt /app

RUN  pip install --upgrade pip &&  \
     pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

COPY app/ /app

# Define environment variables
ENV FLASK_APP=facts.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV FLASK_RUN_PORT=80

CMD ["flask", "run"]
