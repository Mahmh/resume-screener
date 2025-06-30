# ollama/Dockerfile
FROM ollama/ollama:latest

# copy in our little entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]