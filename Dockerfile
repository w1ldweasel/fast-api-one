# Use an official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY . /app

# No cache enabled to not cache downloaded packages for smaller image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the FastAPI app
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# ENTRYPOINT to run FastAPI app
ENTRYPOINT ["uvicorn", "carsharing:app", "--host", "0.0.0.0"]

# Use CMD to provide default arguments
CMD ["--port", "8000"]
