# 1. Use a lightweight Python 'Kitchen'
FROM python:3.12-slim

# 2. Set the working area
WORKDIR /app

# 3. Copy our requirements and code into the container
COPY requirements.txt .
COPY main.py .

# 4. Install the tools using our official requirements file
RUN pip install --no-cache-dir -r requirements.txt

# 5. Start the engine
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
