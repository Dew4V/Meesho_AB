# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Set the port (GCP will send traffic to this)
ENV PORT 8080

# Start the Flask app
CMD ["python", "main.py"]