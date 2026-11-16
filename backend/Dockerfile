FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Create virtual environment
RUN uv venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Install FastAPI & image dependencies
RUN uv pip install fastapi uvicorn pillow python-multipart

# Install lightweight CPU-only PyTorch and TorchVision
RUN uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Copy application code
COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
