import pandas as pd

class GeneradorReportes:
    """
    Clase responsable del Módulo 4: Persistencia y Salida de Datos.
    Se encarga de estructurar y exportar las métricas de red a archivos Microsoft Excel.
    """
    
    @staticmethod
    def exportar_invitados_a_excel(métricas_invitados, ruta_salida="datos/reporte_invitados.xlsx"):
        """
        Toma el diccionario consolidado de usuarios invitados, lo transforma
        en un DataFrame de Pandas y lo exporta con formato de hoja de cálculo.
        """
        if not métricas_invitados:
            return False, "No existen datos consolidados para exportar en el rango de fechas seleccionado."

        try:
            # Reestructurar el diccionario para convertirlo en filas de una tabla
            # Estructura de entrada: { 'username': { 'conexiones': X, 'input_bytes': Y, ... } }
            datos_tabla = []
            for username, metricas in métricas_invitados.items():
                datos_tabla.append({
                    "Usuario Invitado": username,
                    "Cantidad Conexiones": metricas["conexiones"],
                    "Tráfico Bajada (Bytes)": metricas["input_bytes"],
                    "Tráfico Subida (Bytes)": metricas["output_bytes"],
                    "Tráfico Total (Bytes)": metricas["trafico_total_bytes"]
                })

            # Crear el DataFrame de Pandas
            df = pd.DataFrame(datos_tabla)

            # Ordenar los datos de forma descendente según el tráfico total consumido
            df = df.sort_values(by="Tráfico Total (Bytes)", ascending=False)

            # Exportar a Excel utilizando el motor openpyxl (requiere pip install pandas openpyxl)
            # index=False evita que se agregue una columna numérica extra con los índices de fila
            df.to_excel(ruta_salida, index=False, sheet_name="Invitados")
            
            return True, f"Reporte exportado con éxito en: {ruta_salida}"

        except Exception as e:
            return False, f"Error crítico durante la escritura del archivo Excel: {str(e)}"