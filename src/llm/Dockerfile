FROM ollama/ollama

WORKDIR /app

EXPOSE 11434

# Create the start.sh script using RUN
# RUN echo '#!/bin/bash\n\
# ollama serve &\n\
# until ollama status > /dev/null 2>&1; do\n\
#     echo "Waiting for ollama service to start..."\n\
#     sleep 2\n\
# done\n\
# ollama run llama3' > /app/start.sh

RUN echo '#!/bin/bash\n\
ollama serve &\n\
ollama run llama3' > /app/start.sh

# Make the script executable
RUN chmod +x /app/start.sh

# Override the default entrypoint
ENTRYPOINT ["/app/start.sh"]