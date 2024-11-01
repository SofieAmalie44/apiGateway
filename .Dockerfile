# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy current directory contents into the container
COPY . /app

# Install the required packages
RUN pip install -r requirements.txt

# Make port 4000 available to the world outside this container
EXPOSE 4000

# Run app.py when the container launches
CMD ["python", "app.py"]
