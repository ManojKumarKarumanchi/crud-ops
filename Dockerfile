# ================================
# Multi-stage build for smaller image
# ================================

FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies (needed for cryptography, bcrypt compilation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# ================================
# Production image
# ================================

FROM python:3.12-slim

WORKDIR /app

# Create non-root user for security
RUN useradd -m -u 1000 appuser

# Copy Python dependencies from builder to user home
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY main.py .
COPY app/ ./app/

# Copy utility scripts (optional - for manual DB operations)
COPY seed_database.py .

# Set ownership
RUN chown -R appuser:appuser /app /home/appuser/.local

# Switch to non-root user
USER appuser

# Make sure scripts in .local are usable
ENV PATH=/home/appuser/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Healthcheck - disabled for Railway (Railway has its own health checks)
# HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
#     CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

# Run application with multiple workers for production
# Use shell form to allow $PORT environment variable expansion
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000} --workers 4
