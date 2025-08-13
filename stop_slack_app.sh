#!/bin/bash

echo "🛑 Deteniendo Slack Animales Agent..."

if [ -f slack_app.pid ]; then
    PID=$(cat slack_app.pid)
    echo "📊 Proceso encontrado con PID: $PID"
    
    # Check if process is still running
    if ps -p $PID > /dev/null; then
        echo "🔄 Deteniendo proceso..."
        kill $PID
        sleep 2
        
        # Check if process was killed
        if ps -p $PID > /dev/null; then
            echo "⚠️  Proceso no se detuvo, forzando..."
            kill -9 $PID
        else
            echo "✅ Proceso detenido correctamente"
        fi
    else
        echo "ℹ️  Proceso ya no está corriendo"
    fi
    
    # Remove PID file
    rm -f slack_app.pid
else
    echo "❌ No se encontró archivo slack_app.pid"
    echo "💡 La app podría no estar corriendo o se detuvo inesperadamente"
fi

echo "📝 Logs disponibles en: slack_app_debug.log"
echo "🔄 Para reiniciar ejecuta: ./start_slack_app_debug.sh"
