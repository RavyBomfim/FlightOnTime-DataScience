# ============================================
# Stage 1: Builder - Compile dependencies
# ============================================
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy and install Python dependencies
COPY requirements-api.txt .
RUN pip install --no-cache-dir --user -r requirements-api.txt

# ============================================
# Stage 2: Runtime - Minimal production image
# ============================================
FROM python:3.11-slim

# Add metadata labels
LABEL maintainer="FlightOnTime Team"
LABEL version="1.0.0"
LABEL description="FlightOnTime Machine Learning API"

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -u 1001 appuser

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser API ./API
COPY --chown=appuser:appuser helpers ./helpers
COPY --chown=appuser:appuser models ./models
COPY --chown=appuser:appuser metadata ./metadata

# Create necessary directories with correct permissions
RUN mkdir -p data && chown -R appuser:appuser /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH=/home/appuser/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1

# Switch to non-root user
USER appuser

# Expose API port
EXPOSE 8000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Run the application with production settings
CMD ["python", "-m", "uvicorn", "API.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1", \
     "--log-level", "info"]
