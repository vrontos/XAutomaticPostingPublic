# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your code into the container
COPY . .

# Command to run your application
CMD ["python", "XAutomaticPosting.py"]
