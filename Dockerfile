# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=simple_web_app.py
ENV FLASK_ENV=production

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the web application
COPY simple_web_app.py .

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port for the web application
EXPOSE 5000

# Set the default command to run the web app
CMD ["python", "simple_web_app.py"] 