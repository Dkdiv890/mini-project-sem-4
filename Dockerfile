FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the default Hugging Face Space port
EXPOSE 7860

# Run the application with Gunicorn
# Bind to 0.0.0.0 and port 7860 for HF Spaces compatibility
CMD ["gunicorn", "--timeout", "150", "--workers", "1", "--threads", "4", "--bind", "0.0.0.0:7860", "app:app"]
