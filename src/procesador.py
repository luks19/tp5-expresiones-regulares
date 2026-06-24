import re
from datetime import datetime

class ProcesadorDatos:
    """
    Clase responsable de la aplicación de reglas de negocio del Ejercicio 9:
    Filtrado temporal, detección de usuarios invitados mediante expresiones regulares
    y consolidación del tráfico total de red.
    """
    def __init__(self):
        # Patrón Regex para identificar variantes de 'guest' o 'invitado' (case-insensitive)
        self.patron_invitado = re.compile(r"^(?i)(guest|invitado).*$")

    def obtener_usuarios_invitados(self, registros_validos, fecha_inicio_str, fecha_fin_str):
        """
        Filtra los registros válidos por rango de fechas y patrón de usuario.
        Retorna un diccionario con las métricas consolidadas por cada usuario invitado.
        """
        # Estructura de acumulación final
        métricas_invitados = {}

        try:
            # Conversión de los límites ingresados por el usuario a objetos datetime para comparación exacta
            limite_inicio = datetime.strptime(fecha_inicio_str.strip(), "%Y-%m-%d")
            # Se fija el fin del día (23:59:59) para que el rango sea inclusivo de la fecha final
            limite_fin = datetime.strptime(fecha_fin_str.strip() + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # Retorna un diccionario vacío si los formatos de fecha ingresados en la UI son incorrectos
            return métricas_invitados

        for registro in registros_validos:
            # Parsear la fecha del registro actual (formato garantizado por el módulo validador)
            fecha_registro = datetime.strptime(registro["fecha_inicio"], "%Y-%m-%d %H:%M:%S")

            # Evaluación del rango temporal: Inicio <= Registro <= Fin
            if limite_inicio <= fecha_registro <= limite_fin:
                username = registro["username"]

                # Evaluación semántica mediante expresión regular para identificar invitados
                if self.patron_invitado.match(username):
                    # Cálculo del tráfico total del registro en bytes (Input + Output)
                    trafico_registro = registro["input_octets"] + registro["output_octets"]

                    if username not in métricas_invitados:
                        # Inicialización del registro del usuario invitado único
                        métricas_invitados[username] = {
                            "conexiones": 1,
                            "input_bytes": registro["input_octets"],
                            "output_bytes": registro["output_octets"],
                            "trafico_total_bytes": trafico_registro
                        }
                    else:
                        # Acumulación de métricas en caso de reincidencia de conexión
                        métricas_invitados[username]["conexiones"] += 1
                        métricas_invitados[username]["input_bytes"] += registro["input_octets"]
                        métricas_invitados[username]["output_bytes"] += registro["output_octets"]
                        métricas_invitados[username]["trafico_total_bytes"] += trafico_registro

        return métricas_invitados