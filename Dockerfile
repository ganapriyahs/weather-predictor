# 1. Base Image: Slim (Debian-based, easy to debug)
FROM python:3.9-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy dependencies first (Optimization: This layer is cached!)
COPY requirements.txt .

# 4. Install dependencies
# --no-cache-dir: Don't save the downloaded files, keeps image small
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY . .

# 6. Documentation: Tell the user this container listens on port 8000
EXPOSE 8000

# 7. Run the application
# --host 0.0.0.0: Crucial! Allows access from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]