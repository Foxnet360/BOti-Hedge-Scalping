#!/bin/bash
# Script para configurar el entorno virtual para el bot de algotrading

# Colores para mensajes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Configurando entorno virtual para el bot de algotrading de Binance Futures...${NC}"

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python 3 no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Crear entorno virtual
echo -e "${YELLOW}Creando entorno virtual...${NC}"
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error al crear el entorno virtual. Asegúrate de tener instalado el paquete venv."
    echo "Puedes instalarlo con: sudo apt-get install python3-venv (Ubuntu/Debian)"
    exit 1
fi

# Activar entorno virtual
echo -e "${YELLOW}Activando entorno virtual...${NC}"
source venv/bin/activate

# Actualizar pip
echo -e "${YELLOW}Actualizando pip...${NC}"
pip install --upgrade pip

# Instalar dependencias
echo -e "${YELLOW}Instalando dependencias...${NC}"
pip install -r requirements.txt

# Crear archivo .env para las credenciales
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creando archivo .env para las credenciales...${NC}"
    cat > .env << EOL
# Credenciales de Binance
BINANCE_API_KEY=tu_api_key_aqui
BINANCE_API_SECRET=tu_api_secret_aqui
EOL
    echo -e "${GREEN}Archivo .env creado. Por favor, edita el archivo y añade tus credenciales de Binance.${NC}"
else
    echo -e "${YELLOW}El archivo .env ya existe. Asegúrate de que contiene tus credenciales de Binance.${NC}"
fi

echo -e "${GREEN}¡Entorno virtual configurado correctamente!${NC}"
echo -e "${YELLOW}Para activar el entorno virtual, ejecuta: source venv/bin/activate${NC}"
echo -e "${YELLOW}Para desactivar el entorno virtual, ejecuta: deactivate${NC}"
echo -e "${YELLOW}Para ejecutar el bot, usa: python main.py --strategy ma --symbol BTCUSDT --interval 1h${NC}" 