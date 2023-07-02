# Base image
FROM python:3.11.4

# set working directory
WORKDIR /app

# Copy file
COPY main.py /app
COPY requirements.txt /app
COPY model /app/model
COPY ms /app/ms

# Install dependencies
RUN pip install -r requirements.txt

# Run application
EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]