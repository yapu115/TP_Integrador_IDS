#!/bin/bash
echo "=== Instalando dependencias en venv ==="
python3 -m venv venv

if [ -x ./venv/bin/pip ]; then
  PIP=./venv/bin/pip
elif [ -x ./venv/Scripts/pip.exe ]; then
  PIP=./venv/Scripts/pip.exe
else
  echo "No se encontró pip en el entorno virtual."
  exit 1
fi

"$PIP" install --upgrade pip
"$PIP" install -r requirements.txt

echo "=== Instalación finalizada. Ahora activa el entorno con: source venv/bin/activate ==="