FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a directory for logs
RUN mkdir /app/logs

# Set environment variable for Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Run the bot with logging
CMD ["python", "-u", "main.py", "2>&1", "|", "tee", "/app/logs/bot.log"]
