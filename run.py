#!/usr/bin/env python3
"""
Fitness Assistant - Punto de entrada principal
Ejecutar con: python run.py
"""

import subprocess
import sys
import os

def main():
    """Ejecuta la aplicación Streamlit"""
    try:
        # Cambiar al directorio del script
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Ejecutar streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "src/main.py", 
            "--server.port=8501", 
            "--server.address=localhost"
        ])
    except KeyboardInterrupt:
        print("\n🏁 Aplicación cerrada por el usuario")
    except Exception as e:
        print(f"❌ Error ejecutando la aplicación: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando Fitness Assistant...")
    main()