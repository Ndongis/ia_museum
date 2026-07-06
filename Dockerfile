FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    DATABASE_URL=postgresql://postgres:postgres@localhost:5432/vectordb \
    PG_POOL_MIN=1 \
    PG_POOL_MAX=10

# ── Dépendances système : PostgreSQL + outils de compilation pour pgvector ────
RUN apt-get update && apt-get install -y --no-install-recommends \
        postgresql postgresql-contrib postgresql-server-dev-all \
        build-essential git ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

# ── Compilation et installation de l'extension pgvector ──────────────────────
RUN git clone --branch v0.7.4 --depth 1 https://github.com/pgvector/pgvector.git /tmp/pgvector \
    && cd /tmp/pgvector && make && make install \
    && rm -rf /tmp/pgvector

    # ── Modèles Kokoro-ONNX (TTS) ─────────────────────────────────────────────────
RUN mkdir -p /app/kokoro_models \
    && curl -L -o /app/kokoro_models/kokoro-v1.0.onnx \
        https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx \
    && curl -L -o /app/kokoro_models/voices-v1.0.bin \
        https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin

WORKDIR /app

# ── Dépendances Python ────────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Code de l'application ─────────────────────────────────────────────────────
COPY . .
RUN chmod +x entrypoint.sh

EXPOSE 7680

ENTRYPOINT ["./entrypoint.sh"]