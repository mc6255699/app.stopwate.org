FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*


# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*


# Install 1Password CLI
RUN curl -fsSL https://cache.agilebits.com/dist/1P/op2/pkg/v2.29.0/op_linux_amd64_v2.29.0.zip -o op.zip && \
    unzip op.zip -d op-cli && \
    mv op-cli/op /usr/local/bin/op && \
    chmod +x /usr/local/bin/op && \
    rm -rf op.zip op-cli



# Create app directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Run the dev server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
