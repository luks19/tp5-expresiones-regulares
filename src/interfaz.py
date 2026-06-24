import customtkinter as ctkinter
from tkinter import filedialog, messagebox
from validador import MotorValidacion
from procesador import ProcesadorDatos
from reportes import GeneradorReportes

# Configuración estética global de la interfaz gráfica
ctkinter.set_appearance_mode("System")  # Adapta el tema claro/oscuro según el sistema operativo
ctkinter.set_default_color_theme("blue")

class VentanaPrincipal(ctkinter.CTk):
    """
    Clase que define la Interfaz Gráfica de Usuario (UI).
    Modula los campos de entrada de datos y conecta los motores de procesamiento.
    """
    def __init__(self):
        super().__init__()
        
        # Instanciación de las clases lógicas del sistema
        self.validador = MotorValidacion()
        self.procesador = ProcesadorDatos()
        
        # Variables de estado en memoria
        self.registros_validos = []
        self.datos_procesados_invitados = {}
        self.ruta_csv = ""

        # Configuración estructural de la ventana principal
        self.title("Sistema de Auditoría de Conexiones Wi-Fi - Ejercicio 9")
        self.geometry("900x650")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # ------------------ PANEL SUPERIOR: SELECCIÓN DE ARCHIVOS ------------------
        self.frame_archivo = ctkinter.CTkFrame(self)
        self.frame_archivo.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.frame_archivo.grid_columnconfigure(1, weight=1)

        self.btn_cargar = ctkinter.CTkButton(self.frame_archivo, text="Seleccionar CSV", command=self.seleccionar_archivo)
        self.btn_cargar.grid(row=0, column=0, padx=10, pady=10)

        self.lbl_ruta = ctkinter.CTkLabel(self.frame_archivo, text="Archivo no seleccionado", text_color="gray")
        self.lbl_ruta.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # ------------------ PANEL CENTRAL: FILTROS TEMPORALES ------------------
        self.frame_filtros = ctkinter.CTkFrame(self)
        self.frame_filtros.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.lbl_desde = ctkinter.CTkLabel(self.frame_filtros, text="Fecha Inicio (AAAA-MM-DD):")
        self.lbl_desde.grid(row=0, column=0, padx=10, pady=10)
        self.txt_desde = ctkinter.CTkEntry(self.frame_filtros, placeholder_text="2026-01-01", width=120)
        self.txt_desde.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_hasta = ctkinter.CTkLabel(self.frame_filtros, text="Fecha Fin (AAAA-MM-DD):")
        self.lbl_hasta.grid(row=0, column=2, padx=10, pady=10)
        self.txt_hasta = ctkinter.CTkEntry(self.frame_filtros, placeholder_text="2026-01-31", width=120)
        self.txt_hasta.grid(row=0, column=3, padx=10, pady=10)

        self.btn_procesar = ctkinter.CTkButton(self.frame_filtros, text="Analizar Datos", fg_color="green", hover_color="darkgreen", command=self.ejecutar_analisis)
        self.btn_procesar.grid(row=0, column=4, padx=20, pady=10)

        # ------------------ PANEL INFERIOR: VISUALIZACIÓN DE RESULTADOS ------------------
        self.tabs_resultados = ctkinter.CTkTabview(self)
        self.tabs_resultados.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        self.tab_invitados = self.tabs_resultados.add("Usuarios Invitados")
        self.tab_errores = self.tabs_resultados.add("Registros Descartados")
        
        # Configuración del área de texto para mostrar las métricas consolidada de los invitados
        self.txt_resultado_invitados = ctkinter.CTkTextbox(self.tab_invitados, font=("Courier New", 12))
        self.txt_resultado_invitados.pack(fill="both", expand=True, padx=5, pady=5)

        # Configuración del área de texto para mostrar las auditorías de descarte por Regex
        self.txt_resultado_errores = ctkinter.CTkTextbox(self.tab_errores, font=("Courier New", 11), text_color="orange")
        self.txt_resultado_errores.pack(fill="both", expand=True, padx=5, pady=5)

        # ------------------ BOTONERA DE EXPORTACIÓN ------------------
        self.btn_exportar = ctkinter.CTkButton(self, text="Exportar Resultados a Excel", state="disabled", command=self.exportar_reporte)
        self.btn_exportar.grid(row=3, column=0, padx=20, pady=15, sticky="ew")

    def seleccionar_archivo(self):
        """Maneja el explorador de archivos para cargar el CSV de conexiones Wi-Fi."""
        ruta = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if ruta:
            self.ruta_csv = ruta
            self.lbl_ruta.configure(text=ruta, text_color="white")
            
            # Procesamiento sintáctico inmediato mediante el Motor de Validación
            validos, descartados = self.validador.procesar_archivo_csv(ruta)
            
            if validos is None:
                messagebox.showerror("Error", "No se pudo leer el archivo seleccionado.")
                return

            self.registros_validos = validos
            
            # Volcar los registros descartados de manera obligatoria en su correspondiente pestaña
            self.txt_resultado_errores.delete("1.0", ctkinter.END)
            self.txt_resultado_errores.insert("1.0", f"AUDITORÍA DE INTEGRIDAD - REGISTROS DESCARTADOS (Total: {len(descartados)})\n")
            self.txt_resultado_errores.insert(ctkinter.END, "="*85 + "\n\n")
            for err in descartados:
                self.txt_resultado_errores.insert(ctkinter.END, f"Fila {err['linea']} | Motivo: {err['motivo']}\n> Contenido: {err['contenido']}\n\n")
            
            messagebox.showinfo("Carga Completa", f"Archivo analizado.\nRegistros Válidos: {len(validos)}\nRegistros Descartados: {len(descartados)}")

    def ejecutar_analisis(self):
        """Maneja los filtros temporales e invoca la lógica de consolidación del Ejercicio 9."""
        if not self.registros_validos:
            messagebox.showwarning("Advertencia", "Debe cargar un archivo CSV válido antes de ejecutar el análisis.")
            return

        f_inicio = self.txt_desde.get()
        f_fin = self.txt_hasta.get()

        if not f_inicio or not f_fin:
            messagebox.showwarning("Campos vacíos", "Por favor introduzca ambas fechas de corte.")
            return

        # Filtrar y acumular datos usando la lógica del procesador
        self.datos_procesados_invitados = self.procesador.obtain_usuarios_invitados(self.registros_validos, f_inicio, f_fin)
        
        # Refrescar la pantalla de la interfaz
        self.txt_resultado_invitados.delete("1.0", ctkinter.END)
        self.txt_resultado_invitados.insert("1.0", f"REPORTE CONSOLIDADO DE USUARIOS INVITADOS\n")
        self.txt_resultado_invitados.insert(ctkinter.END, f"Período evaluado: {f_inicio} hasta {f_fin}\n")
        self.txt_resultado_invitados.insert(ctkinter.END, f"Cantidad total de invitados detectados: {len(self.datos_procesados_invitados)}\n")
        self.txt_resultado_invitados.insert(ctkinter.END, "="*85 + "\n\n")
        
        if not self.datos_procesados_invitados:
            self.txt_resultado_invitados.insert(ctkinter.END, "No se registraron conexiones de invitados en el intervalo de fechas provisto.")
            self.btn_exportar.configure(state="disabled")
            return

        # Formatear la salida como tabla en formato texto de ancho fijo
        plantilla_cabecera = "{:<25} | {:<12} | {:<20} | {:<20}\n"
        plantilla_fila = "{:<25} | {:<12} | {:<20} | {:<20}\n"
        
        self.txt_resultado_invitados.insert(ctkinter.END, plantilla_cabecera.format("Usuario Invitado", "Conexiones", "Tráfico Subida (B)", "Tráfico Total (B)"))
        self.txt_resultado_invitados.insert(ctkinter.END, "-"*85 + "\n")
        
        for user, met in self.datos_procesados_invitados.items():
            self.txt_resultado_invitados.insert(ctkinter.END, plantilla_fila.format(
                user, met["conexiones"], met["output_bytes"], met["trafico_total_bytes"]
            ))
            
        # Habilitar el botón de exportación a Excel tras procesar con éxito
        self.btn_exportar.configure(state="normal")

    def exportar_reporte(self):
        """Dispara el módulo de persistencia de datos para guardar el archivo Excel."""
        exito, msg = GeneradorReportes.exportar_invitados_a_excel(self.datos_procesados_invitados)
        if exito:
            messagebox.showinfo("Éxito", msg)
        else:
            messagebox.showerror("Error", msg)