Iniciar o banco no Xampp (mudar pro Docker)

Iniciar venv:
    .\venv\Scripts\Activate.ps1  

Iniciar projeto:
    uvicorn index:asgi_app --host localhost --port 3000

Rodar com Docker:
    docker-compose up --build

Derrubar a instãncia do Docker completamente:
    docker-compose down
