# Use an official Python runtime as base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Run your bot
CMD ["python", "HelloBot.py"]
