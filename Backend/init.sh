#!/bin/bash
echo "=== Instalando dependencias en venv ==="
python -m venv venv

./venv/Scripts/pip install --upgrade pip
./venv/Scripts/pip install -r requirements.txt

echo "=== Instalación finalizada. Ahora activa el entorno con: source venv/Scripts/activate ==="