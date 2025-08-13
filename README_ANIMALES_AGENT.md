# 🐾 Animales Agent - Slack AI App

Un agente especializado en responder preguntas sobre animales, integrado con Slack AI Apps.

## 🚀 Instalación por Sistema Operativo

### 📱 **macOS / Linux**
Sigue las instrucciones en [README_SLACK_INTEGRATION.md](README_SLACK_INTEGRATION.md)

### 🪟 **Windows**
Sigue las instrucciones en [README_WINDOWS_WSL.md](README_WINDOWS_WSL.md)

## Características

- **Especializado en animales**: Responde exclusivamente preguntas sobre animales, vida silvestre y mascotas
- **Integración con Slack**: Funciona como una Slack AI App
- **Herramienta de tiempo**: Utiliza la herramienta de fecha/hora para responder preguntas sobre comportamientos estacionales
- **Multilingüe**: Responde en español e inglés según el idioma de la pregunta
- **Contexto persistente**: Mantiene el contexto de la conversación

## Estructura del Proyecto

```
slack_agent/
├── animales_agent.py          # Agente principal de animales
├── slack_app.py              # Integración con Slack
├── agent_tools/
│   └── date_time_tool.py     # Herramienta de fecha/hora
├── requirements.txt          # Dependencias
├── test_animales_agent.py    # Script de prueba
├── README_ANIMALES_AGENT.md  # Este archivo
├── README_SLACK_INTEGRATION.md # Instalación macOS/Linux
└── README_WINDOWS_WSL.md     # Instalación Windows
```

## Instalación Rápida

### Para macOS / Linux:
```bash
# Crear entorno virtual con uv
uv venv
source .venv/bin/activate

# Instalar dependencias
uv pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus tokens

# Probar instalación
python test_animales_agent.py
```

### Para Windows (WSL):
```powershell
# Instalar WSL
wsl --install

# En WSL, seguir los pasos de macOS/Linux
wsl
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Uso

### Modo Interactivo
```bash
python animales_agent.py
```

### Script de Prueba
```bash
python test_animales_agent.py
```

### Integración con Slack
```bash
python slack_app.py
```

## Ejemplos de Preguntas

- ¿Cuáles son los animales más rápidos del mundo?
- What is the largest animal on Earth?
- ¿Por qué los gatos ronronean?
- How do penguins survive in cold weather?
- ¿Cuánto tiempo viven las tortugas?
- What animals migrate during winter?
- ¿Cuáles son los animales más inteligentes?
- How do bees communicate?

## Herramientas Disponibles

- **get_current_datetime**: Obtiene información de fecha y hora actual (útil para comportamientos estacionales, patrones de migración, etc.)

## Diferencias con el Agente Anterior

- ❌ **Eliminado**: Todas las herramientas de BigQuery
- ❌ **Eliminado**: Análisis de costos de GCP
- ✅ **Nuevo**: Enfoque exclusivo en animales
- ✅ **Nuevo**: Respuestas educativas y entretenidas
- ✅ **Mantenido**: Integración con Slack
- ✅ **Mantenido**: Estructura de LangGraph

## Configuración de Slack

El agente está configurado para funcionar como una Slack AI App con:

- Mensajes de bienvenida personalizados
- Prompts sugeridos sobre animales
- Estados de procesamiento informativos
- Manejo de errores robusto

## Desarrollo

Para agregar nuevas funcionalidades:

1. Modifica `animales_agent.py` para agregar nuevas herramientas
2. Actualiza el `SYSTEM_PROMPT` según sea necesario
3. Prueba con `test_animales_agent.py`
4. Actualiza la integración en `slack_app.py` si es necesario

## 📚 Documentación por Sistema Operativo

- **[macOS / Linux](README_SLACK_INTEGRATION.md)**: Instalación y configuración completa
- **[Windows (WSL)](README_WINDOWS_WSL.md)**: Instalación específica para Windows con WSL
- **[Este archivo](README_ANIMALES_AGENT.md)**: Visión general del proyecto
