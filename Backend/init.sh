#!/bin/bash

echo "=== Creando entorno virtual de Python ==="
python3 -m venv venv

echo "=== Activando entorno virtual ==="
source venv/bin/activate

echo "=== Instalando dependencias iniciales ==="
if [ -f requirements.txt ]; then
    pip install --upgrade pip
    
    pip install -r requirements.txt
    
    echo "=== ¡Entorno inicializado correctamente! ==="
else
    echo "Error: No se encontró el archivo requirements.txt en esta carpeta."
fi