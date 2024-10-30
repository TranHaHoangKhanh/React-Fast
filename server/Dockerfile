# Use the official Python image as the base image
FROM python:latest

# Set the working directory in the container
WORKDIR /api

# Copy the requirements file into the container
COPY ./requirements.txt /api/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code into the container
COPY . /api

# Expose the port your FastAPI application will run on (default is 8000)
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]