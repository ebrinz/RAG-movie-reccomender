# Base image

FROM ollama/ollama:latest
EXPOSE 11434
RUN mkdir -p /app
RUN cat <<'EOF' > /app/start.sh
#!/bin/bash
ollama serve &
sleep 5
ollama pull llama3
# Keep the Ollama server running in the foreground
wait
EOF
RUN chmod +x /app/start.sh
ENTRYPOINT ["/app/start.sh"]