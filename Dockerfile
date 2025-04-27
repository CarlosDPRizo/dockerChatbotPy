FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl unzip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# 🚫 Remove essa verificação de CSV aqui
# Treina o modelo (agora o arquivo estará disponível em tempo de execução)
RUN mkdir -p modelos

EXPOSE 3000
CMD ["uvicorn", "index:asgi_app", "--host", "0.0.0.0", "--port", "3000"]