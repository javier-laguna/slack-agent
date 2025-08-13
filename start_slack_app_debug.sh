#!/bin/bash

echo "🐾 Iniciando Slack Animales Agent en modo DEBUG..."
echo "=================================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: Archivo .env no encontrado"
    echo "📝 Crea un archivo .env con las variables necesarias"
    exit 1
fi

# Check if required environment variables are set
source .env

if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY no está configurado"
    exit 1
fi

if [ -z "$SLACK_BOT_TOKEN" ]; then
    echo "❌ Error: SLACK_BOT_TOKEN no está configurado"
    exit 1
fi

if [ -z "$SLACK_SOCKET_TOKEN" ]; then
    echo "❌ Error: SLACK_SOCKET_TOKEN no está configurado"
    exit 1
fi

echo "✅ Variables de entorno configuradas correctamente"
echo "🐾 Iniciando agente de animales en modo DEBUG..."
echo "📝 Logs se guardarán en: slack_app_debug.log"
echo "🔄 Para detener: Ctrl+C o 'kill \$(cat slack_app.pid)'"
echo "📊 Para ver logs en tiempo real: tail -f slack_app_debug.log"
echo "========================================================"

# Start the Slack app in background with debug logging
uv run python slack_app.py > slack_app_debug.log 2>&1 &

# Save the process ID
echo $! > slack_app.pid

echo "✅ App iniciada con PID: $(cat slack_app.pid)"
echo "📝 Para ver logs en tiempo real ejecuta: tail -f slack_app_debug.log"
echo "🛑 Para detener ejecuta: ./stop_slack_app.sh"
