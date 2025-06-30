#!/bin/sh
set -e

# 1) start the Ollama daemon in the background
ollama serve &
OLLAMA_PID=$!

# 2) give it a moment (or better, poll /dev/tcp) to spin up
sleep 5

# 3) pull your model once the daemon is live
ollama pull deepseek-r1:1.5b

# 4) now block on the Ollama process so the container doesn’t exit
wait $OLLAMA_PID