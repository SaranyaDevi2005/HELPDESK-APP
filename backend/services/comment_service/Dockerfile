FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM python:3.9-slim AS production
WORKDIR /app
COPY --from=builder /app /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8003
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
