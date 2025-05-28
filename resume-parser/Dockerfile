FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements and source code
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . ./

# Expose port
EXPOSE 5000

# Run the app with gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:create_app()"]
