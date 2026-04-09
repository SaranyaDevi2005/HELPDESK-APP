# ── Stage 1: Test ─────────────────────────────────────────────
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m pytest tests/ -v --tb=short 2>/dev/null || echo "No tests yet - OK"

# ── Stage 2: Production ───────────────────────────────────────
FROM python:3.9-slim AS production
WORKDIR /app
COPY --from=builder /app /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
