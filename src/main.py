import sys
import os

# Añadir el directorio actual al path de ejecución para evitar errores de importación de módulos locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interfaz import VentanaPrincipal

def iniciar_aplicacion():
    """
    Función de entrada principal (Entry Point) del sistema de auditoría.
    Inicializa el entorno gráfico e invoca el bucle de eventos.
    """
    app = VentanaPrincipal()
    app.mainloop()

if __name__ == "__main__":
    iniciar_aplicacion()