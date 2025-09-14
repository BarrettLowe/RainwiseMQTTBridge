# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir: Disables the cache which reduces the image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src directory into the container at /app
COPY src/ .

# Run main.py when the container launches
# The -u flag ensures that print statements are sent straight to logs without being buffered.
CMD ["python", "-u", "main.py"]
