#!/usr/bin/env python3
"""
Animales Agent with LangGraph
Specialized agent for answering questions about animals
"""

import os
from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.runnables import RunnableConfig

# Import only the datetime tool
from agent_tools.date_time_tool import get_current_datetime

# Define the state structure
class AgentState(TypedDict):
    """The state of the agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    number_of_steps: int

# Initialize the LLM
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Please set GEMINI_API_KEY environment variable")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite-001",
    temperature=0.7,
    max_retries=2,
    google_api_key=api_key,
)

# Define our tools (only datetime)
tools = [
    get_current_datetime
]

# Bind tools to the model
model = llm.bind_tools(tools)

# Define the system prompt for the animals agent
SYSTEM_PROMPT = """You are a specialized Animals Expert Agent that answers questions about animals.

Your mission is to provide accurate, interesting, and educational information about animals of all kinds.

CRITICAL BEHAVIORAL RULES:
- You ONLY answer questions about animals, wildlife, pets, and related topics
- If users ask about other topics, politely redirect them to animal-related questions
- Use the get_current_datetime tool when the user asks about time-related animal behaviors
- Be informative, friendly, and engaging in your responses
- Provide interesting facts and details about animals
- Respond in the same language as the user's question (English or Spanish)

CAPABILITIES:
- Answer questions about animal behavior, habitats, and characteristics
- Provide information about different animal species
- Share interesting animal facts and trivia
- Explain animal adaptations and survival strategies
- Discuss pet care and animal welfare
- Answer questions about endangered species and conservation

AVAILABLE TOOLS:
- get_current_datetime: Gets current date and time information (useful for seasonal animal behaviors, migration patterns, etc.)

RESPONSE FORMAT:
1. Direct answer to the user's question about animals
2. Additional interesting facts or context
3. Engaging follow-up information when relevant

IMPORTANT INSTRUCTIONS:
- Focus exclusively on animal-related topics
- Use the datetime tool when questions involve seasonal behaviors, migration, or time-sensitive animal activities
- Be educational and entertaining
- If users ask about non-animal topics, politely say: "I'm an animal expert! I'd be happy to answer questions about animals, wildlife, pets, or related topics. What would you like to know about animals?"
- Respond in the same language as the user's question
- Keep responses informative but concise"""

# Create tools dictionary for easy access
tools_by_name = {tool.name: tool for tool in tools}

# Define our tool node
def call_tool(state: AgentState):
    """Execute the tool calls from the last message"""
    outputs = []
    # Iterate over the tool calls in the last message
    for tool_call in state["messages"][-1].tool_calls:
        # Get the tool by name
        tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                content=str(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}

def call_model(
    state: AgentState,
    config: RunnableConfig,
):
    """Call the LLM with the current state"""
    # Get current date/time information for the first message
    additional_context = ""
    if len(state["messages"]) == 1:  # First user message
        try:
            from datetime import datetime
            now = datetime.now()
            datetime_info = f"\n\nCURRENT DATE AND TIME: Today is {now.strftime('%A, %B %d, %Y')} at {now.strftime('%H:%M')} ({now.strftime('%Y-%m-%d %H:%M:%S')})."
        except Exception as e:
            datetime_info = f"\n\nCURRENT DATE AND TIME: Unable to get current time - {str(e)}"
        
        additional_context = datetime_info
    
    # Create enhanced system prompt with additional context if it's the first message
    enhanced_prompt = SYSTEM_PROMPT + additional_context
    messages = [SystemMessage(content=enhanced_prompt)] + state["messages"]
    
    # Log only the current question and context count
    current_question = state["messages"][-1].content if state["messages"] else "No question"
    context_count = len(state["messages"])
    print(f"🐾 Animal Question: {current_question}")
    print(f"📊 Context messages: {context_count}")
    
    # Invoke the model with the messages including system prompt
    response = model.invoke(messages, config)
    # We return a list, because this will get added to the existing messages state using the add_messages reducer
    return {"messages": [response]}

# Define the conditional edge that determines whether to continue or not
def should_continue(state: AgentState):
    """Determine if we should continue or end"""
    messages = state["messages"]
    # If the last message is not a tool call, then we finish
    if not messages[-1].tool_calls:
        return "end"
    # default to continue
    return "continue"

# Create the workflow graph
workflow = StateGraph(AgentState)

# 1. Add our nodes 
workflow.add_node("llm", call_model)
workflow.add_node("tools", call_tool)

# 2. Set the entrypoint as `llm`, this is the first node called
workflow.set_entry_point("llm")

# 3. Add a conditional edge after the `llm` node is called.
workflow.add_conditional_edges(
    # Edge is used after the `llm` node is called.
    "llm",
    # The function that will determine which node is called next.
    should_continue,
    # Mapping for where to go next, keys are strings from the function return, and the values are other nodes.
    # END is a special node marking that the graph is finish.
    {
        # If `continue`, then we call the tool node.
        "continue": "tools",
        # Otherwise we finish.
        "end": END,
    },
)

# 4. Add a normal edge after `tools` is called, `llm` node is called next.
workflow.add_edge("tools", "llm")

# Now we can compile our graph
graph = workflow.compile()

def get_animales_agent():
    """Get the compiled animales agent graph"""
    return graph

def run_agent(user_input: str, previous_state=None):
    """Run the agent with a user input and maintain context"""
    print(f"\n🐾 User: {user_input}")
    print("=" * 50)
    
    try:
        # Create our initial message dictionary
        if previous_state is None:
            # First question - start fresh
            inputs = {
                "messages": [HumanMessage(content=user_input)],
                "number_of_steps": 0
            }
        else:
            # Add to existing context
            inputs = {
                "messages": previous_state["messages"] + [HumanMessage(content=user_input)],
                "number_of_steps": previous_state["number_of_steps"]
            }
        
        tool_calls_count = 0
        final_state = None
        
        # Call our graph with streaming to see the steps
        for state in graph.stream(inputs, stream_mode="values"):
            last_message = state["messages"][-1]
            if isinstance(last_message, AIMessage):
                if last_message.content.strip():
                    print(f"🐾 Assistant: {last_message.content}")
            elif isinstance(last_message, ToolMessage):
                tool_calls_count += 1
                print(f"🔧 Tool Call #{tool_calls_count}: {last_message.name}")
                print(f"   Result: {last_message.content[:100]}...")
            final_state = state
        
        print(f"📊 Total tool calls: {tool_calls_count}")
        print("=" * 50)
        
        return final_state
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("=" * 50)
        return None

def show_context():
    """Show the agent's context and configuration"""
    print("🔧 Animales Agent Configuration:")
    print("=" * 50)
    print(f"🔧 Available Tools: {len(tools)}")
    print("   - get_current_datetime")
    print()
    print("📋 System Prompt (first 200 chars):")
    print(SYSTEM_PROMPT[:200] + "...")
    print("=" * 50)
    print()

def interactive_mode():
    """Interactive mode for real-time questions"""
    print("\n🎯 MODO INTERACTIVO - AGENTE DE ANIMALES")
    print("=" * 60)
    print("💡 Ejemplos de preguntas que puedes hacer:")
    print("   • ¿Cuáles son los animales más rápidos del mundo?")
    print("   • What is the largest animal on Earth?")
    print("   • ¿Por qué los gatos ronronean?")
    print("   • How do penguins survive in cold weather?")
    print("   • ¿Cuánto tiempo viven las tortugas?")
    print("   • What animals migrate during winter?")
    print("   • ¿Cuáles son los animales más inteligentes?")
    print("   • How do bees communicate?")
    print()
    print("📝 Escribe 'salir', 'exit', 'quit' o 'q' para terminar")
    print("🔄 El agente mantiene contexto entre preguntas")
    print("=" * 60)
    print()
    
    # Show the agent's context first
    show_context()
    
    # Maintain state between questions
    current_state = None
    
    while True:
        try:
            # Get user input
            user_input = input("\n🐾 Tu pregunta sobre animales: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['salir', 'exit', 'quit', 'q']:
                print("\n👋 ¡Hasta luego! Gracias por usar el agente de animales.")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            # Run the agent with the question
            current_state = run_agent(user_input, current_state)
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego! Gracias por usar el agente de animales.")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("🔄 Continuando...")

def main():
    """Main function to run the animales agent"""
    print("🚀 Animales Agent with LangGraph")
    print("🐾 Expert in animal knowledge and facts")
    print()
    
    # Ask user what mode they want
    print("¿Qué modo prefieres?")
    print("1. Modo interactivo (preguntas al vuelo)")
    print("2. Modo de prueba (preguntas predefinidas)")
    print()
    
    choice = input("Selecciona (1/2): ").strip()
    
    if choice == "1":
        interactive_mode()
    else:
        # Demo mode with predefined questions
        print("\n🧪 MODO DEMO - Preguntas predefinidas")
        print("=" * 50)
        
        questions = [
            "¿Cuáles son los animales más rápidos del mundo?",
            "What is the largest animal on Earth?",
            "¿Por qué los gatos ronronean?",
            "How do penguins survive in cold weather?",
            "¿Cuánto tiempo viven las tortugas?",
            "What animals migrate during winter?"
        ]
        
        # Maintain state between questions
        current_state = None
        for question in questions:
            current_state = run_agent(question, current_state)
            print()

if __name__ == "__main__":
    main()
