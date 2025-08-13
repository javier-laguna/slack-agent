#!/usr/bin/env python3
"""
Herramienta para obtener fecha y hora actual
"""

from datetime import datetime
from typing import Dict
from langchain_core.tools import tool

@tool
def get_current_datetime() -> Dict[str, str]:
    """
    Gets the current date and time in a readable format.
    
    Returns:
        Dict with current date and time information
    """
    try:
        now = datetime.now()
        
        return {
            "current_date": now.strftime("%Y-%m-%d"),
            "current_time": now.strftime("%H:%M:%S"),
            "current_datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "day_of_week": now.strftime("%A"),
            "month": now.strftime("%B"),
            "year": str(now.year),
            "formatted_date": now.strftime("%d de %B de %Y"),
            "formatted_time": now.strftime("%H:%M"),
            "timezone_info": "UTC (asumiendo zona horaria del sistema)"
        }
        
    except Exception as e:
        return {
            "error": f"Error al obtener fecha/hora: {str(e)}",
            "current_date": "N/A",
            "current_time": "N/A"
        }

@tool
def get_date_info() -> str:
    """
    Gets current date information in a readable format for the user.
    
    Returns:
        String with current date information
    """
    try:
        now = datetime.now()
        return f"Hoy es {now.strftime('%A, %d de %B de %Y')} y son las {now.strftime('%H:%M')}"
        
    except Exception as e:
        return f"Error al obtener fecha: {str(e)}" 