#!/bin/bash
echo "=== Instalando dependencias en venv ==="
python -m venv venv

./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo "=== Instalación finalizada. Ahora activa el entorno con: source venv/bin/activate ==="