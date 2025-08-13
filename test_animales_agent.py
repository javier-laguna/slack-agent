#!/usr/bin/env python3
"""
Test script for the Animales Agent
"""

from animales_agent import run_agent

def test_animales_agent():
    """Test the animales agent with a simple question"""
    print("🧪 Testing Animales Agent...")
    print("=" * 50)
    
    # Test question
    test_question = "¿Cuántas patas tiene un gato?"
    
    print(f"Pregunta de prueba: {test_question}")
    print("-" * 50)
    
    # Run the agent
    result = run_agent(test_question)
    
    if result:
        print("✅ Agent test completed successfully!")
    else:
        print("❌ Agent test failed!")
    
    print("=" * 50)

if __name__ == "__main__":
    test_animales_agent()
