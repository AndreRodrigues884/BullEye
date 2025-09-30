# reset-database.ps1
# Script para resetar e inicializar database do BullEye

Write-Host "[1/7] Parando containers e removendo volumes..." -ForegroundColor Yellow
docker-compose down -v

Write-Host "[2/7] Aguardando limpeza..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

Write-Host "[3/7] Iniciando PostgreSQL..." -ForegroundColor Cyan
docker-compose up -d postgres

Write-Host "[4/7] Aguardando PostgreSQL iniciar (20 segundos)..." -ForegroundColor Cyan
Start-Sleep -Seconds 20

Write-Host "[5/7] Copiando e executando init.sql..." -ForegroundColor Yellow
docker cp database\init.sql bulleye-postgres:/tmp/init.sql
docker-compose exec postgres psql -U bulleye_user -d bulleye_db -f /tmp/init.sql

Write-Host "[6/7] Verificando tabelas criadas..." -ForegroundColor Green
docker-compose exec postgres psql -U bulleye_user -d bulleye_db -c "\dt"

Write-Host "[7/7] Iniciando todos os servicos..." -ForegroundColor Cyan
docker-compose up -d

Write-Host "" -ForegroundColor White
Write-Host "Aguardando servicos iniciarem (10 segundos)..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

Write-Host "" -ForegroundColor White
Write-Host "==================================================" -ForegroundColor Green
Write-Host "Database inicializada com sucesso!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host "" -ForegroundColor White

Write-Host "Testando conexao Python..." -ForegroundColor Yellow
docker-compose exec ml-service python db_utils.py list

Write-Host "" -ForegroundColor White
Write-Host "Pronto! Database BullEye configurada." -ForegroundColor Green
Write-Host "" -ForegroundColor White
Write-Host "Proximos passos:" -ForegroundColor Cyan
Write-Host "  1. Coletar dados: docker-compose exec ml-service python scheduler.py --mode test" -ForegroundColor White
Write-Host "  2. Ver dados: docker-compose exec ml-service python db_utils.py summary" -ForegroundColor White
Write-Host "  3. API docs: http://localhost:8000/docs" -ForegroundColor White