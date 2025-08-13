# 🐾 Animales Agent - Instalación en Windows con WSL

Guía completa para instalar y ejecutar el Agente de Animales en Windows usando WSL (Windows Subsystem for Linux).

## 🚀 Instalación Rápida en Windows

### 1. Instalar WSL2

#### Opción A: Instalación Automática (Recomendado)
```powershell
# Abrir PowerShell como Administrador y ejecutar:
wsl --install
```

#### Opción B: Instalación Manual
```powershell
# Habilitar características de Windows
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Reiniciar Windows

# Descargar e instalar WSL2
# Descargar desde: https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi
```

### 2. Configurar WSL

Después de instalar WSL:

1. **Reiniciar Windows**
2. **Abrir WSL** (se abrirá automáticamente o busca "Ubuntu" en el menú inicio)
3. **Crear usuario y contraseña** cuando se solicite

### 3. Instalar Dependencias en WSL

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y pip
sudo apt install python3 python3-pip python3-venv -y

# Instalar curl (para instalar uv)
sudo apt install curl -y

# Instalar git
sudo apt install git -y
```

### 4. Instalar uv en WSL

```bash
# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Recargar shell o reiniciar WSL
source ~/.bashrc
```

### 5. Clonar y Configurar el Proyecto

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd slack_agent

# Crear entorno virtual
uv venv

# Activar entorno virtual
source .venv/bin/activate

# Instalar dependencias
uv pip install -r requirements.txt
```

### 6. Configurar Variables de Entorno

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

### 7. Probar la Instalación

```bash
# Probar el agente
python test_animales_agent.py

# Ejecutar en modo interactivo
python animales_agent.py
```

## 🎯 Uso en WSL

### Ejecutar con Slack
```bash
# Usar los scripts existentes (funcionan igual que en Mac/Linux)
./start_slack_app.sh

# O ejecutar directamente
python slack_app.py
```

### Scripts Disponibles
```bash
# Iniciar app
./start_slack_app.sh

# Iniciar en modo debug
./start_slack_app_debug.sh

# Detener app
./stop_slack_app.sh

# Configuración rápida
./quick_start.sh
```

## 🔧 Configuración de Slack

### 1. Crear la App en Slack

#### Paso 1: Crear la App
1. Ve a [api.slack.com/apps](https://api.slack.com/apps)
2. Haz clic en **"Create New App"**
3. Selecciona **"From scratch"**
4. Nombre: `Animales Agent`
5. Selecciona tu workspace

#### Paso 2: Habilitar AI Apps
1. En el panel izquierdo, ve a **"Agents & AI Apps"**
2. Habilita la función **"Agents & AI Apps"**

#### Paso 3: Configurar Socket Mode
1. Ve a **"Socket Mode"**
2. Habilita Socket Mode
3. Genera un **App-Level Token**:
   - Nombre: `animales-agent-socket`
   - Scope: `connections:write`

#### Paso 4: Configurar Permisos
1. Ve a **"OAuth & Permissions"**
2. En **"Scopes"** agrega:
   - `assistant:write`
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
3. **Copia el Bot Token**

### 2. Actualizar .env con los Tokens

```bash
# En WSL, editar .env
nano .env

# Agregar los tokens copiados de Slack
GEMINI_API_KEY=tu_api_key_de_gemini
SLACK_BOT_TOKEN=xoxb-tu-bot-token-aqui
SLACK_SOCKET_TOKEN=xapp-tu-app-token-aqui
```

## 🐛 Solución de Problemas

### Error: "wsl --install no funciona"
```powershell
# Verificar si WSL está habilitado
wsl --list --verbose

# Si no aparece, habilitar manualmente
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all
```

### Error: "uv no se encuentra"
```bash
# Recargar shell
source ~/.bashrc

# O agregar manualmente al PATH
export PATH="$HOME/.cargo/bin:$PATH"
```

### Error: "Permisos denegados en scripts"
```bash
# Dar permisos de ejecución
chmod +x *.sh
```

### Error: "No se puede conectar a Slack"
- Verifica que los tokens estén correctos
- Asegúrate de que la app esté instalada en el workspace
- Revisa que todos los eventos estén habilitados

### Error: "GEMINI_API_KEY no encontrado"
```bash
# Verificar que el archivo .env existe
ls -la .env

# Verificar contenido
cat .env
```

## 📁 Estructura del Proyecto en WSL

```
slack_agent/
├── animales_agent.py         # Agente principal
├── slack_app.py             # Integración con Slack
├── agent_tools/
│   └── date_time_tool.py    # Herramienta de fecha/hora
├── requirements.txt         # Dependencias
├── start_slack_app.sh       # Script de inicio
├── test_animales_agent.py   # Script de prueba
├── env_example.txt          # Ejemplo de variables de entorno
├── README_WINDOWS_WSL.md    # Este archivo
└── .env                     # Variables de entorno
```

## 🚀 Comandos Rápidos

```bash
# Activar entorno virtual
source .venv/bin/activate

# Probar agente
python test_animales_agent.py

# Ejecutar con Slack
python slack_app.py

# Ver logs en tiempo real
tail -f slack_app_debug.log

# Detener app
./stop_slack_app.sh
```

## 📝 Notas Importantes

1. **WSL2**: Asegúrate de usar WSL2 para mejor rendimiento
2. **Archivos**: Los archivos del proyecto se comparten entre Windows y WSL
3. **Terminal**: Usa Windows Terminal para mejor experiencia
4. **Backup**: Los archivos están en tu sistema Windows, haz backup regularmente

## 🔗 Recursos Adicionales

- [WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [Windows Terminal](https://github.com/microsoft/terminal)
- [Slack API Documentation](https://api.slack.com/)
- [Google Gemini API](https://ai.google.dev/)
