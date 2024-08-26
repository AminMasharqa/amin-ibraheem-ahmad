# Use the Selenium standalone Chrome image as a base
FROM selenium/standalone-chrome:latest

# Set environment variables to prevent issues with debconf
ENV DEBIAN_FRONTEND=noninteractive

# Update, fix APT repository issues, and install Python and required tools
USER root
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update --allow-releaseinfo-change && \
    apt-get install -y python3 python3-pip python3-venv build-essential && \
    rm -rf /var/lib/apt/lists/*

# Create and activate a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Cython to resolve the issue with `cython_sources`
RUN pip install --no-cache-dir Cython

# Install PyYAML from pre-built binary wheels
RUN pip install --no-cache-dir PyYAML==5.3.1

# Install awscli and botocore
RUN pip install --no-cache-dir awscli==1.27.10 botocore==1.29.10

# Copy the requirements file to the container
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the handler script to the container
COPY handler.py /app/handler.py

# Set the working directory
WORKDIR /app

# Command to run the scraper
CMD ["python", "handler.py"]
