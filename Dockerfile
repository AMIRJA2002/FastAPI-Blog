FROM python:3.13

RUN apt-get update && apt-get install -y wget

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Download wait-for-it script
# RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
#     chmod +x wait-for-it.sh

# Make sure the database is up before running alembic migrations
# RUN ./wait-for-it.sh postgres --timeout=60 -- alembic upgrade head

RUN alembic upgrade head

EXPOSE 8000

CMD ["python", "app.py"]