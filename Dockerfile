# Use an official Python runtime as the base image
FROM python:3.11  

# Set the working directory inside the container
WORKDIR /app

# Copy your requirements.txt file
COPY requirements.txt ./

# Install dependencies using pip
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Expose port (optional, adjust based on your application)
EXPOSE 8080 

# Command to run the application (replace with your actual entry point)
CMD [ "python", "main.py" ]
