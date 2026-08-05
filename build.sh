#!/usr/bin/env bash
# Comando de build para Render (e utilizável no Railway).
# No Render, cole em "Build Command": ./build.sh
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Estáticos são servidos pelo WhiteNoise, então precisam ser coletados no build.
python manage.py collectstatic --noinput

# O Render não tem fase de "release" separada como o Procfile do Railway,
# então a migração roda aqui. É idempotente.
python manage.py migrate --noinput
