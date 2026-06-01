# ---- Stage 1: Builder (necesita devel para compilar flash-attn) ----
FROM nvidia/cuda:12.8.0-devel-ubuntu22.04 AS builder

RUN apt-get update && apt-get install -y \
    python3.10 python3.10-distutils python3-pip git build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && pip install --no-cache-dir flash-attn --no-build-isolation \
       -f https://flash-attn.pages.dev/whl/torch280cu128.html \
    && pip install --no-cache-dir git+https://github.com/huggingface/diffusers.git

# ---- Stage 2: Runtime (imagen más ligera, sin herramientas de compilación) ----
FROM nvidia/cuda:12.8.0-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y \
    python3.10 python3.10-distutils python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copiamos solo los paquetes Python instalados desde el builder
COPY --from=builder /usr/local/lib/python3.10/dist-packages /usr/local/lib/python3.10/dist-packages
COPY --from=builder /usr/local/bin/huggingface-cli /usr/local/bin/
COPY --from=builder /usr/local/bin/rq /usr/local/bin/

WORKDIR /app

# Copiamos la app (los modelos se montan en volumen, no se bakean en la imagen)
COPY . .

RUN chmod +x entrypoint.sh

# Directorio donde se montará el volumen de modelos
VOLUME /models

# Exponemos el puerto que usará Flask
EXPOSE 5050

# El entrypoint descarga los modelos si no están en el volumen
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python3", "main.py"]
