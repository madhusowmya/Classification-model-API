# Use an official Python runtime as a parent image
FROM python:3.9.12

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 1313

# Run the run_api.sh script when the container launches
CMD ["bash", "run_api.sh"]