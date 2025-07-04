@echo off
echo Iniciando APIs...

start cmd /k "python -m uvicorn geraquestoes:app --reload --port 8000"
start cmd /k "python -m uvicorn cadastro:app --reload --port 8001"
start cmd /k "python -m uvicorn login:app --reload --port 8002"
start cmd /k "python -m uvicorn ranqueamento:app --reload --port 8003"

echo Todas as APIs foram iniciadas em janelas separadas.
pause
