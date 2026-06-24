import re

class MotorValidacion:
    """
    Clase encargada de la lectura, análisis sintáctico y filtrado
    de registros de tráfico Wi-Fi mediante expresiones regulares.
    """
    def __init__(self):
        # Compilación de patrones Regex para optimizar el rendimiento en bucles
        self.patron_mac = re.compile(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")
        self.patron_numerico = re.compile(r"^\d+$")
        self.patron_fecha = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
        self.patron_username = re.compile(r"^\S+$")

    def validar_registro(self, fila, numero_linea):
        """
        Valida que una fila del CSV (lista de strings) contenga todos sus campos
        con el formato correcto y no estén vacíos.
        """
        if len(fila) < 8 or any(campo.strip() == "" for campo in fila):
            return False, "Campos incompletos o vacíos"

        session_id, username, mac_cliente, mac_ap, fecha_inicio, session_time, input_octets, output_octets = [c.strip() for c in fila[:8]]

        # Validaciones consecutivas mediante el módulo 're'
        if not self.patron_username.match(username):
            return False, f"Username inválido: '{username}'"
        if not self.patron_mac.match(mac_cliente):
            return False, f"MAC Cliente inválida: '{mac_cliente}'"
        if not self.patron_mac.match(mac_ap):
            return False, f"MAC AP inválida: '{mac_ap}'"
        if not self.patron_fecha.match(fecha_inicio):
            return False, f"Formato de fecha inválido: '{fecha_inicio}'"
        if not self.patron_numerico.match(session_time):
            return False, f"Session_Time no es numérico: '{session_time}'"
        if not self.patron_numerico.match(input_octets):
            return False, f"Input_Octets no es numérico: '{input_octets}'"
        if not self.patron_numerico.match(output_octets):
            return False, f"Output_Octets no es numérico: '{output_octets}'"

        # Si supera todas las expresiones regulares, se retorna estructurado con tipos nativos corregidos
        registro_valido = {
            "session_id": session_id,
            "username": username,
            "mac_cliente": mac_cliente,
            "mac_ap": mac_ap,
            "fecha_inicio": fecha_inicio,
            "session_time": int(session_time),
            "input_octets": int(input_octets),
            "output_octets": int(output_octets)
        }
        return True, registro_valido

    def procesar_archivo_csv(self, ruta_archivo):
        """
        Lee el archivo CSV, distribuyendo las líneas en registros válidos o descartados.
        """
        registros_validos = []
        registros_descartados = []

        try:
            with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
                # Omitir cabecera si existe
                cabecera = archivo.readline()
                
                for num_linea, linea in enumerate(archivo, start=2):
                    linea_limpia = linea.strip()
                    if not linea_limpia:
                        continue # Ignorar líneas en blanco
                    
                    # División por comas (formato CSV estándar)
                    campos = linea_limpia.split(",")
                    es_valido, resultado = self.validar_registro(campos, num_linea)
                    
                    if es_valido:
                        registros_validos.append(resultado)
                    else:
                        registros_descartados.append({
                            "linea": num_linea,
                            "contenido": linea_limpia,
                            "motivo": resultado
                        })
        except FileNotFoundError:
            return None, [{"linea": 0, "contenido": "", "motivo": "Archivo no encontrado"}]

        return registros_validos, registros_descartados