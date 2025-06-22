@echo off
echo Iniciando APIs...

start cmd /k "python -m uvicorn geraquestoes:app --reload --port 8000"
start cmd /k "python -m uvicorn cadastro:app --reload --port 8001"
start cmd /k "python -m uvicorn login:app --reload --port 8002"

echo Todas as APIs foram iniciadas em janelas separadas.
pause
