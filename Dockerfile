# docker build -t leondeoliveirapedrosa/back-chat:dev . && docker push leondeoliveirapedrosa/back-chat:dev
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "backchat.asgi:application", "--host", "0.0.0.0", "--port", "8000"]