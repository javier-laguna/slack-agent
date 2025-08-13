# Integración de Agente de Animales con Slack

Este proyecto integra tu agente especializado en animales con Slack usando la nueva funcionalidad de AI Apps.

## 🚀 Configuración Rápida

### 1. Crear la App en Slack

#### Paso 1: Crear la App
1. Ve a [api.slack.com/apps](https://api.slack.com/apps)
2. Haz clic en **"Create New App"**
3. Selecciona **"From scratch"**
4. Nombre: `Animales Agent` (o el que prefieras)
5. Selecciona tu workspace

#### Paso 2: Habilitar AI Apps
1. En el panel izquierdo, ve a **"Agents & AI Apps"**
2. Habilita la función **"Agents & AI Apps"**
3. Esto agregará automáticamente el scope `assistant:write`

#### Paso 3: Configurar Socket Mode
1. Ve a **"Socket Mode"** en el panel izquierdo
2. Habilita Socket Mode
3. Genera un **App-Level Token**:
   - Nombre: `animales-agent-socket`
   - Scope: `connections:write`
4. **Guarda este token** - lo necesitarás después

#### Paso 4: Configurar Permisos
1. Ve a **"OAuth & Permissions"**
2. En **"Scopes"** agrega:
   - `assistant:write` (ya agregado automáticamente)
   - `im:history`
   - `chat:write`

#### Paso 5: Configurar Event Subscriptions
1. Ve a **"Event Subscriptions"**
2. Habilita eventos
3. En **"Subscribe to bot events"** agrega:
   - `assistant_thread_started`
   - `assistant_thread_context_changed`
   - `message.im`

#### Paso 6: Instalar la App
1. Ve a **"Install App"**
2. Haz clic en **"Install to Workspace"**
3. **Copia el Bot Token** que aparece después de la instalación

### 2. Configurar Variables de Entorno

Crea un archivo `.env` basado en `env_example.txt`:

```bash
# Copiar archivo de ejemplo
cp env_example.txt .env

# Editar con tus tokens
nano .env
```

Variables necesarias:
```bash
# Google Gemini API
GEMINI_API_KEY=tu_api_key_de_gemini

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-tu-bot-token-aqui
SLACK_SOCKET_TOKEN=xapp-tu-app-token-aqui
```

### 3. Instalar Dependencias

```bash
# Crear entorno virtual con uv
uv venv
source .venv/bin/activate

# Instalar dependencias
uv pip install -r requirements.txt
```

### 4. Ejecutar la App

```bash
./start_slack_app.sh
```

## 🎯 Cómo Usar

### En Slack:
1. Busca tu app en la lista de apps de Slack
2. Haz clic en el ícono de la app en la barra lateral
3. Se abrirá el contenedor de AI Apps
4. Haz preguntas como:
   - "¿Cuáles son los animales más rápidos del mundo?"
   - "What is the largest animal on Earth?"
   - "¿Por qué los gatos ronronean?"
   - "How do penguins survive in cold weather?"

### Características:
- ✅ Conversación fluida como en la terminal
- ✅ Mantiene contexto entre mensajes
- ✅ Prompts sugeridos para empezar
- ✅ Indicadores de estado (procesando, etc.)
- ✅ Manejo de errores robusto
- ✅ Respuestas educativas sobre animales

## 🔧 Estructura del Proyecto

```
slack_agent/
├── animales_agent.py         # Agente especializado en animales
├── slack_app.py             # Integración con Slack
├── agent_tools/             # Herramientas del agente
│   └── date_time_tool.py    # Herramienta de fecha/hora
├── requirements.txt         # Dependencias
├── start_slack_app.sh       # Script de inicio
├── test_animales_agent.py   # Script de prueba
├── env_example.txt          # Ejemplo de variables de entorno
└── README_SLACK_INTEGRATION.md
```

## 🐛 Solución de Problemas

### Error: "SLACK_BOT_TOKEN not found"
- Verifica que copiaste el token correcto desde la sección "Install App"
- El token debe empezar con `xoxb-`

### Error: "SLACK_APP_TOKEN not found"
- Verifica que copiaste el App-Level Token desde "Socket Mode"
- El token debe empezar con `xapp-`

### La app no responde en Slack
- Verifica que habilitaste todos los eventos en "Event Subscriptions"
- Asegúrate de que la app está instalada en el workspace
- Revisa los logs de la aplicación para errores

### Error de permisos
- Verifica que agregaste todos los scopes necesarios
- Reinstala la app después de cambiar scopes

## 📝 Notas Importantes

1. **Socket Mode**: Solo para desarrollo. En producción deberías usar HTTP endpoints
2. **Contexto**: Cada conversación mantiene su propio estado
3. **Rate Limits**: Slack tiene límites de rate, pero el agente los maneja automáticamente
4. **Seguridad**: Nunca compartas tus tokens en código público
5. **Enfoque**: El agente está especializado en preguntas sobre animales

## 🚀 Próximos Pasos

- [ ] Configurar para producción con HTTP endpoints
- [ ] Agregar más interactividad con Block Kit
- [ ] Implementar notificaciones automáticas
- [ ] Agregar métricas y monitoreo
- [ ] Expandir conocimientos sobre más especies animales

## 📚 Recursos

- [Slack AI Apps Documentation](https://api.slack.com/docs/apps/ai)
- [Slack Bolt for Python](https://slack.dev/bolt-python/)
- [Slack API Reference](https://api.slack.com/web)
- [Google Gemini API](https://ai.google.dev/)
