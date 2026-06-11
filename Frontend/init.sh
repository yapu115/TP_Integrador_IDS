#!/bin/bash
echo "=== Instalando dependencias en .venv ==="

python3 -m venv .venv

source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "=== Instalación finalizada. Ahora activa el entorno con: source venv/bin/activate ==="