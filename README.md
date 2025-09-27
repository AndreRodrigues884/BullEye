# 🎯 BullEye - Stock Market ML Prediction

Sistema completo de previsão do mercado de ações usando Machine Learning, com interface web moderna.

## 🚀 Tecnologias

- **Frontend**: Vue.js 3 + Vuetify + Chart.js
- **Backend**: Node.js + Express + PostgreSQL + Redis  
- **ML**: Python + TensorFlow + FastAPI
- **DevOps**: Docker + GitHub Actions

## 📋 Pré-requisitos

- Docker & Docker Compose
- Git
- Node.js 18+ (opcional, para desenvolvimento local)
- Python 3.11+ (opcional, para desenvolvimento local)

## 🛠️ Setup Rápido

```bash
# Clonar e entrar no diretório
git clone <seu-repo>
cd bulleye

# Subir todos os serviços
make dev

# Ou usando docker-compose diretamente
docker-compose up --build
```

## 🔗 URLs de Acesso

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **ML Service**: http://localhost:8000
- **Database**: localhost:5432
- **Redis**: localhost:6379

## 📁 Estrutura do Projeto

```
bulleye/
├── frontend/          # Vue.js application
├── backend/           # Node.js API
├── ml-service/        # Python ML service  
├── database/          # SQL scripts
├── nginx/             # Reverse proxy config
├── docker-compose.yml # Container orchestration
└── Makefile          # Helper commands
```

## 🧪 Comandos Úteis

```bash
make dev        # Ambiente de desenvolvimento
make prod       # Ambiente de produção  
make logs       # Ver logs dos containers
make clean      # Limpar containers e volumes
make test       # Executar testes
make reset-db   # Resetar banco de dados
```

## 📊 Features

- ✅ Coleta automática de dados financeiros
- ✅ Modelos ML para previsão de preços
- ✅ API RESTful com cache Redis
- ✅ Dashboard interativo com gráficos
- ✅ Sistema de autenticação JWT
- ✅ Monitoramento e logs

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request
