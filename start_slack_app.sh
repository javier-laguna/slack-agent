#!/bin/bash

echo "🐾 Iniciando Slack Animales Agent..."
echo "====================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: Archivo .env no encontrado"
    echo "📝 Crea un archivo .env con las siguientes variables:"
    echo "🔧 Asegúrate de configurar:"
    echo "   - GEMINI_API_KEY"
    echo "   - SLACK_BOT_TOKEN"
    echo "   - SLACK_SOCKET_TOKEN"
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
echo "🐾 Iniciando agente de animales en Slack..."

# Start the Slack app
uv run python slack_app.py
