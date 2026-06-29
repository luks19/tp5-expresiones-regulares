# Sistema de Auditoría de Conexiones Wi-Fi — Ejercicio 9

## 1. Explicación General del Proyecto
El propósito de esta aplicación es procesar de forma automatizada archivos de registros de tráfico de conexiones Wi-Fi con formato de valores separados por comas (CSV). El sistema actúa como una herramienta de auditoría de red orientada a la seguridad y optimización de recursos, permitiendo aislar de manera precisa la actividad de los perfiles que acceden bajo la condición de "invitados" a la infraestructura de la institución.

A través de este software, un administrador de red puede ingresar un rango cronológico específico para calcular la cantidad exacta de usuarios invitados únicos que se conectaron y consolidar el volumen de tráfico total de datos que consumió cada uno de ellos. Esto facilita la toma de decisiones estratégicas respecto al control de ancho de banda y la asignación de políticas de conectividad inalámbrica.

### Objetivos Técnicos Cumplidos:
* **Validación Sintáctica con Regex:** Filtrado e inspección estricta de cada campo del archivo CSV utilizando expresiones regulares nativas.
* **Validación de Entrada del Usuario:** Control del formato de las fechas ingresadas en la interfaz gráfica mediante expresiones regulares, con verificación de coherencia del rango temporal antes de procesar.
* **Auditoría de Datos Corruptos:** Aislamiento y reporte detallado de todas las líneas que contienen errores de formato o campos vacíos para su posterior depuración.
* **Persistencia de Negocio:** Consolidación de métricas de red y exportación automatizada de los resultados a entornos de hojas de cálculo de Microsoft Excel (.xlsx), con diálogo de selección de ruta de destino.

---

## 2. Modalidad de Trabajo e Integrantes
Este proyecto fue diseñado e implementado siguiendo pautas de desarrollo modular de software y control de versiones por ramas.

**Grupo Asignado:**
* Jeremias Villach
* Faustino De Lucia
* Lucas Valdemoros
* Geronimo Giordano

---

## 3. Instalación y Ejecución

### Requisitos Previos
* Python 3.10 o superior
* Sistema operativo con soporte para Tkinter (Linux, Windows, macOS)

### Instalación de Dependencias
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Ejecución de la Aplicación
```bash
python3 src/main.py
```

---

## 4. Arquitectura del Software y Desarrollo Individual
La aplicación se estructuró bajo un patrón modular e independiente para garantizar mantenibilidad, escalabilidad y un flujo de datos controlado. Cada módulo fue desarrollado en su respectiva rama funcional de Git para reflejar el aporte del equipo:

### Módulo de Interfaz de Usuario (src/interfaz.py)
* **Función:** Responsable de la capa de presentación gráfica del sistema mediante la librería CustomTkinter. Implementa los componentes de selección de archivos del sistema operativo, los campos de entrada de texto para los límites de fecha con validación Regex integrada, la verificación de coherencia del rango temporal (fecha inicio <= fecha fin), y los cuadros contenedores optimizados para la muestra de los reportes en pantalla con 5 columnas de métricas (Usuario, Conexiones, Tráfico Bajada, Tráfico Subida, Tráfico Total) y los logs de auditoría de errores. La exportación a Excel se realiza mediante un diálogo de selección de ruta de destino.

### Módulo del Motor de Validación (src/validador.py)
* **Función:** Encargado del control sintáctico del archivo CSV de entrada. Mediante el uso del módulo nativo re, analiza línea por línea el archivo descartando registros incompletos o con formatos corruptos (direcciones MAC mal formadas, marcas de tiempo inválidas o variables de tráfico no numéricas). Clasifica los datos en una lista de registros válidos y otra de registros descartados.

### Módulo Procesador de Datos (src/procesador.py)
* **Función:** Implementa la lógica de negocio del Ejercicio 9. Toma los registros sintácticamente limpios, los filtra cronológicamente utilizando objetos datetime en base al rango provisto por el operador y ejecuta la expresión regular de coincidencia semántica `(?i)^(guest|invitado).*$` para aislar las sesiones de invitados. Realiza el cálculo matemático acumulado de tráfico por usuario único aplicando la fórmula: Tráfico Total = Input_Octets + Output_Octets.

### Módulo de Persistencia y Salida (src/reportes.py)
* **Función:** Gestiona la exportación física de los datos. Transforma el diccionario de acumulación en memoria en un objeto estructurado DataFrame de la librería Pandas, ordena las métricas en forma descendente según el consumo total y escribe el archivo binario final compatible con Microsoft Excel (.xlsx).

---

## 5. Especificación Técnica de las Expresiones Regulares
El núcleo del sistema utiliza patrones lógicos compilados a través del módulo re de Python para garantizar la integridad de las transacciones. A continuación se detallan las expresiones regulares implementadas:

1. **Validación de Direcciones Físicas (MAC Cliente / MAC AP):**
   `^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$`
   *Garantiza la detección estructural de 6 bloques de dos dígitos hexadecimales separados de forma homogénea por dos puntos o guiones.*

2. **Validación de Métricas Numéricas (Session_Time, Input_Octets, Output_Octets):**
   `^\d+$`
   *Fuerza a que los campos contengan exclusivamente caracteres numéricos enteros no negativos, previniendo excepciones en el casteo de datos.*

3. **Validación de Estampa Temporal del CSV (Fecha_Inicio):**
   `^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$`
   *Verifica la estructura estandarizada AAAA-MM-DD HH:MM:SS para asegurar un procesamiento cronológico seguro.*

4. **Validación de Nombres de Usuario (Username):**
   `^\S+$`
   *Garantiza que el campo de usuario contenga al menos un carácter no vacío y sin espacios en blanco.*

5. **Validación de Fechas de la Interfaz Gráfica:**
   `^\d{4}-\d{2}-\d{2}$`
   *Controla que las fechas ingresadas por el operador en los campos de la UI respeten el formato AAAA-MM-DD antes de invocar la lógica de procesamiento.*

6. **Filtrado Semántico de Usuarios Invitados (Ejercicio 9):**
   `(?i)^(guest|invitado).*$`
   *Activa la insensibilidad a mayúsculas y minúsculas (?i) en el inicio de la cadena (^) para agrupar todas las variantes de nombres de usuario que comiencen con las raíces estipuladas por la regla de negocio, aceptando cualquier sufijo mediante la clausura de Kleene (.*$).*

---

## 6. Estructura del Proyecto

```
tp5-expresiones-regulares/
├── datos/
│   └── conexiones_wifi.csv
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── validador.py
│   ├── procesador.py
│   ├── interfaz.py
│   └── reportes.py
├── .gitignore
├── requirements.txt
└── README.md
```