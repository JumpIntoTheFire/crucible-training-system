FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend package — context is project root so backend.main:app import works
COPY backend/ ./backend/

EXPOSE 8000

# Init DB tables then start server
CMD ["sh", "-c", "python -m backend.init_db && uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"]
