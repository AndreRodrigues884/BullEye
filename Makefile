.PHONY: build up down logs clean install

# Desenvolvimento
dev:
	docker-compose up --build

# Produção
prod:
	docker-compose --profile production up --build -d

# Parar serviços
down:
	docker-compose down

# Logs
logs:
	docker-compose logs -f

# Limpar containers e volumes
clean:
	docker-compose down -v --rmi all

# Instalar dependências localmente
install:
	cd frontend && npm install
	cd backend && npm install
	cd ml-service && pip install -r requirements.txt

# Reset do banco de dados
reset-db:
	docker-compose stop postgres
	docker volume rm bulleye_postgres_data
	docker-compose up postgres -d

# Executar testes
test:
	docker-compose exec backend npm test
	docker-compose exec ml-service python -m pytest

# Entrar nos containers
shell-frontend:
	docker-compose exec frontend sh

shell-backend:
	docker-compose exec backend sh

shell-ml:
	docker-compose exec ml-service bash