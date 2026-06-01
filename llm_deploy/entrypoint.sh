#!/bin/bash
set -e

# Login a Hugging Face usando variable de entorno (nunca hardcodear el token)
if [ -n "$HF_TOKEN" ]; then
    echo "Autenticando en Hugging Face..."
    huggingface-cli login --token "$HF_TOKEN"
else
    echo "AVISO: HF_TOKEN no definido, omitiendo login de Hugging Face"
fi

# Descarga los modelos solo si no están ya en el volumen
if [ ! -d "/models/Qwen3-8B" ]; then
    echo "Descargando Qwen3-8B..."
    huggingface-cli download Qwen/Qwen3-8B --local-dir /models/Qwen3-8B --local-dir-use-symlinks False
fi

if [ ! -d "/models/stable-diffusion-3.5-m" ]; then
    echo "Descargando stable-diffusion-3.5-medium..."
    huggingface-cli download stabilityai/stable-diffusion-3.5-medium --local-dir /models/stable-diffusion-3.5-m --local-dir-use-symlinks False
fi

if [ ! -d "/models/shieldgemma-9b" ]; then
    echo "Descargando shieldgemma-9b..."
    huggingface-cli download google/shieldgemma-9b --local-dir /models/shieldgemma-9b --local-dir-use-symlinks False
fi

exec "$@"
