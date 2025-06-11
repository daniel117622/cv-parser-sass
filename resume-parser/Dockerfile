FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Create NLTK data directory and set permissions
RUN mkdir -p /root/nltk_data

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy source code
COPY . ./

# Expose port
EXPOSE 5000

# Run the app with gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:create_app()"]