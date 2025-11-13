# Script de inicialização do ChefConta
# Execute este arquivo para iniciar o sistema

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "    ChefConta - Sistema de Gestao Financeira   " -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se o ambiente virtual existe
if (-Not (Test-Path "venv")) {
    Write-Host "[ERRO] Ambiente virtual nao encontrado!" -ForegroundColor Red
    Write-Host "Execute: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Ativar ambiente virtual
Write-Host "[1/3] Ativando ambiente virtual..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

# Verificar se as dependencias estao instaladas
Write-Host "[2/3] Verificando dependencias..." -ForegroundColor Green
$packages = pip list
if (-Not ($packages -match "customtkinter")) {
    Write-Host "[AVISO] Dependencias nao instaladas!" -ForegroundColor Yellow
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Verificar se o banco de dados existe
if (-Not (Test-Path "database\chefconta.db")) {
    Write-Host "[AVISO] Banco de dados nao inicializado!" -ForegroundColor Yellow
    Write-Host "Inicializando banco de dados..." -ForegroundColor Yellow
    python src\utils\init_db.py
}

# Executar aplicação
Write-Host "[3/3] Iniciando ChefConta..." -ForegroundColor Green
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Sistema iniciando... Por favor, aguarde." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

python main.py

# Verificar se houve erro
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERRO] Ocorreu um erro ao executar o sistema!" -ForegroundColor Red
    Write-Host "Verifique o arquivo INSTALACAO.md para mais detalhes." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Aplicacao encerrada." -ForegroundColor Cyan
