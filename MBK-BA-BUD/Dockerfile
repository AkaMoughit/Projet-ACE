# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Copy the contents of the local src directory to the working directory
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port 80
EXPOSE 80

# Command to run the application
CMD ["uvicorn", "main:app", "--reload"]
