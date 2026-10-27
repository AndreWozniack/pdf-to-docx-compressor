#!/bin/bash
cd "$(dirname "$0")"

echo "=========================================================="
echo "  Iniciando Conversor PDF para Word com Otimização..."
echo "=========================================================="

# Cria ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "Configurando ambiente Python (primeira execução)..."
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt
fi

echo "Iniciando servidor local e abrindo navegador..."
./venv/bin/python app.py
