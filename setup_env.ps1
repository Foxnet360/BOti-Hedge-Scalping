# Script para configurar el entorno virtual para el bot de algotrading en Windows

Write-Host "Configurando entorno virtual para el bot de algotrading de Binance Futures..." -ForegroundColor Yellow

# Verificar si Python está instalado
try {
    $pythonVersion = python --version
    Write-Host "Python instalado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python no está instalado o no está en el PATH. Por favor, instálalo antes de continuar." -ForegroundColor Red
    exit 1
}

# Crear entorno virtual
Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
python -m venv venv
if (-not $?) {
    Write-Host "Error al crear el entorno virtual. Asegúrate de tener instalado el módulo venv." -ForegroundColor Red
    exit 1
}

# Activar entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
if (-not $?) {
    Write-Host "Error al activar el entorno virtual. Puede que necesites ejecutar Set-ExecutionPolicy RemoteSigned -Scope Process" -ForegroundColor Red
    exit 1
}

# Actualizar pip
Write-Host "Actualizando pip..." -ForegroundColor Yellow
pip install --upgrade pip

# Instalar dependencias
Write-Host "Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt

# Crear archivo .env para las credenciales
if (-not (Test-Path .env)) {
    Write-Host "Creando archivo .env para las credenciales..." -ForegroundColor Yellow
    @"
# Credenciales de Binance
BINANCE_API_KEY=tu_api_key_aqui
BINANCE_API_SECRET=tu_api_secret_aqui
"@ | Out-File -FilePath .env -Encoding utf8
    Write-Host "Archivo .env creado. Por favor, edita el archivo y añade tus credenciales de Binance." -ForegroundColor Green
} else {
    Write-Host "El archivo .env ya existe. Asegúrate de que contiene tus credenciales de Binance." -ForegroundColor Yellow
}

Write-Host "¡Entorno virtual configurado correctamente!" -ForegroundColor Green
Write-Host "Para activar el entorno virtual, ejecuta: .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "Para desactivar el entorno virtual, ejecuta: deactivate" -ForegroundColor Yellow
Write-Host "Para ejecutar el bot, usa: python main.py --strategy ma --symbol BTCUSDT --interval 1h" -ForegroundColor Yellow 