FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "kgeb/extract.py", "--docs", "documents.txt", "--out", "entities_output.json"]
