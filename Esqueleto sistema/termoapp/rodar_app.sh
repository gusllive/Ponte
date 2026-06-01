#!/bin/bash

# 1. Entra na pasta do backend e liga o servidor Python em segundo plano (&)
cd /home/gustavo/Documentos/app_eng_qui/app/backend
PYTHONPATH=. python3 -m uvicorn main:app --host 127.0.0.1 --port 8000 &

# Guarda o ID do processo do Python para podermos fechar depois
PID_BACKEND=$!

# Espera 3 segundos para garantir que o Python carregou os Pickles antes do Flutter abrir
sleep 3

# 2. Entra na pasta do frontend e roda o aplicativo Flutter
cd /home/gustavo/Documentos/app_eng_qui/app/frontend
flutter run 

# Quando você fechar o Flutter, o script encerra o processo do Python automaticamente
kill $PID_BACKEND