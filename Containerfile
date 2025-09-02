FROM registry.access.redhat.com/ubi9/python-311:latest

# Install system dependencies as root
USER root
RUN dnf update -y && \
    dnf install -y gcc python3-devel && \
    dnf clean all

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir .

# Copy source code
COPY elos_google_search_mcp/ ./elos_google_search_mcp/

# Create non-root user with a unique UID
RUN useradd -m -u 10001 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the MCP server
ENTRYPOINT ["python", "-m", "elos_google_search_mcp.server"]
