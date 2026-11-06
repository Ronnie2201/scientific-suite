# Use official Python slim image
FROM python:3.11-slim

# Set metadata
LABEL maintainer="Your Name <you@example.com>"
LABEL description="Scientific Computing Suite"
LABEL version="1.0.0"

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies for PyQt5 and matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Qt5 dependencies for PyQt5
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xinerama0 \
    libxcb-xfixes0 \
    libdbus-1-3 \
    libfontconfig1 \
    # Optional: for headless rendering
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (security best practice)
RUN useradd -m -u 1000 scientist && \
    mkdir -p /app /workspace && \
    chown -R scientist:scientist /app /workspace

# Set working directory
WORKDIR /app

# Copy requirements first (for better layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=scientist:scientist . .

# Switch to non-root user
USER scientist

# Set matplotlib backend to non-interactive for headless usage
ENV MPLBACKEND=Agg

# Default command (CLI)
CMD ["python", "-m", "interface.cli"]