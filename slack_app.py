#!/usr/bin/env python3
"""
Slack AI App for Cost Analyzer Agent
Integrates the GCP Cost Analyzer Agent with Slack's AI Apps feature
"""

import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError

# Import our animales agent
from animales_agent import get_animales_agent, run_agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Get the animales agent
animales_agent = get_animales_agent()

# Store conversation states (thread_ts -> agent_state)
conversation_states: Dict[str, Any] = {}

@app.event("assistant_thread_started")
def handle_assistant_thread_started(event, say, client):
    """Handle when a user starts a new AI app conversation"""
    try:
        thread_ts = event.get("thread_ts")
        channel_id = event.get("context", {}).get("channel_id")
        
        logger.info(f"New AI app thread started: {thread_ts}")
        logger.info(f"Channel ID: {channel_id}")
        logger.info(f"Full event: {event}")
        
        # For AI apps, channel_id might be in different location
        if not channel_id:
            # Try to get from different possible locations
            channel_id = event.get("channel_id") or event.get("channel")
        
        if not channel_id:
            logger.error("No channel_id found in event")
            return
        
        # Set initial status
        client.assistant_threads_setStatus(
            channel_id=channel_id,
            thread_ts=thread_ts,
            status="🐾 Iniciando agente de animales..."
        )
        
        # Set suggested prompts
        client.assistant_threads_setSuggestedPrompts(
            channel_id=channel_id,
            thread_ts=thread_ts,
            prompts=[
                "¿Cuáles son los animales más rápidos del mundo?",
                "What is the largest animal on Earth?",
                "¿Por qué los gatos ronronean?",
                "How do penguins survive in cold weather?"
            ]
        )
        
        # Send welcome message
        welcome_message = """🐾 **Bienvenido al Agente de Animales**

Soy tu asistente especializado en responder preguntas sobre animales. Puedo ayudarte con:

• 🦁 Información sobre diferentes especies
• 🐾 Comportamiento animal
• 🌍 Hábitats y adaptaciones
• 🐕 Cuidado de mascotas
• 🦋 Datos curiosos sobre animales

**Ejemplos de preguntas:**
• ¿Cuáles son los animales más rápidos del mundo?
• What is the largest animal on Earth?
• ¿Por qué los gatos ronronean?
• How do penguins survive in cold weather?

¡Hazme cualquier pregunta sobre animales!"""
        
        say(
            text=welcome_message,
            thread_ts=thread_ts
        )
        
    except Exception as e:
        logger.error(f"Error in assistant_thread_started: {e}")

@app.event("assistant_thread_context_changed")
def handle_assistant_thread_context_changed(event, say, client):
    """Handle when user changes context (opens different channel)"""
    try:
        thread_ts = event.get("thread_ts")
        context = event.get("context", {})
        
        logger.info(f"AI app context changed: {thread_ts} -> {context}")
        
    except Exception as e:
        logger.error(f"Error in assistant_thread_context_changed: {e}")

@app.event("message")
def handle_message(event, say, client):
    """Handle incoming messages in AI app threads"""
    try:
        # Only handle messages in AI app threads
        if not event.get("thread_ts"):
            return
            
        thread_ts = event.get("thread_ts")
        channel_id = event.get("channel")
        user_message = event.get("text", "").strip()
        user_id = event.get("user")
        
        # Skip bot messages
        if event.get("bot_id"):
            return
            
        # Skip empty messages
        if not user_message:
            return
            
        logger.info(f"Processing message in thread {thread_ts}: {user_message}")
        logger.info(f"Channel ID: {channel_id}")
        
        if not channel_id:
            logger.error("No channel_id found in message event")
            return
        
        # Set status to show we're processing
        client.assistant_threads_setStatus(
            channel_id=channel_id,
            thread_ts=thread_ts,
            status="🐾 Buscando información sobre animales..."
        )
        
        # Get previous state for this thread
        previous_state = conversation_states.get(thread_ts)
        
        # Run the animales agent
        try:
            logger.info(f"Calling run_agent with message: {user_message}")
            final_state = run_agent(user_message, previous_state)
            logger.info(f"run_agent returned: {final_state is not None}")
            
            if final_state:
                # Store the updated state
                conversation_states[thread_ts] = final_state
                
                logger.info(f"Final state messages count: {len(final_state.get('messages', []))}")
                
                # Get the last AI message (skip tool messages)
                last_ai_message = None
                for i, message in enumerate(reversed(final_state["messages"])):
                    logger.info(f"Message {i}: type={type(message)}, content={getattr(message, 'content', 'NO_CONTENT')[:100] if hasattr(message, 'content') else 'NO_CONTENT'}")
                    
                    # Skip tool messages and messages with tool calls
                    if (hasattr(message, 'content') and 
                        message.content and 
                        not message.content.startswith('{') and  # Skip JSON tool results
                        'AIMessage' in str(type(message))):  # Only AI messages
                        last_ai_message = message.content
                        logger.info(f"Found AI message: {last_ai_message[:100]}")
                        break
                
                if last_ai_message:
                    # Send response back to Slack
                    say(
                        text=last_ai_message,
                        thread_ts=thread_ts
                    )
                else:
                    # If no AI message found, send a default response
                    say(
                        text="🐾 Estoy buscando información sobre animales. ¿Qué animal te interesa conocer?",
                        thread_ts=thread_ts
                    )
            else:
                say(
                    text="❌ Ocurrió un error al procesar tu pregunta. Por favor, intenta de nuevo.",
                    thread_ts=thread_ts
                )
                
        except Exception as agent_error:
            logger.error(f"Agent error: {agent_error}")
            say(
                text=f"❌ Error en el agente: {str(agent_error)}",
                thread_ts=thread_ts
            )
        
        # Clear status
        if channel_id:
            client.assistant_threads_setStatus(
                channel_id=channel_id,
                thread_ts=thread_ts,
                status=""
            )
        
    except Exception as e:
        logger.error(f"Error in message handler: {e}")
        try:
            # Try to send error message
            say(
                text="❌ Ocurrió un error inesperado. Por favor, intenta de nuevo.",
                thread_ts=event.get("thread_ts")
            )
        except:
            pass

@app.error
def custom_error_handler(error, body, logger):
    """Handle errors"""
    logger.exception(f"Error: {error}")
    logger.info(f"Request body: {body}")

def main():
    """Start the Slack app"""
    if not os.environ.get("SLACK_BOT_TOKEN"):
        raise ValueError("SLACK_BOT_TOKEN environment variable is required")
    if not os.environ.get("SLACK_SOCKET_TOKEN"):
        raise ValueError("SLACK_SOCKET_TOKEN environment variable is required")
    
    # Start the app
    handler = SocketModeHandler(app, os.environ["SLACK_SOCKET_TOKEN"])
    logger.info("🐾 Starting Slack Animales Agent...")
    handler.start()

if __name__ == "__main__":
    main()
