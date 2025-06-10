FROM python:3.9-slim

# Install the mariadb client
RUN apt-get update && apt-get install -y mariadb-client && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /Backup

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /Backup

# Set the entrypoint command
CMD ["python", "backup.py"]
