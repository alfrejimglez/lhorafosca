import os
import chardet
import requests
import re

# Pedir la URL completa al usuario
full_url = input("Introduce la URL completa de uno de los segmentos ")

# Usar una expresión regular para extraer la URL base, el token, y el número del segmento final
match = re.match(r"(.*segment)(\d+)\.vtt(\?.*)", full_url)
if not match:
    print("La URL no tiene el formato esperado.")
    exit()

base_url = match.group(1)  # Parte de la URL hasta 'segment'
token = match.group(3)  # Token después del .vtt
end_segment = int(match.group(2))  # Número del segmento final (e.g., 110)

# Asumimos que el segmento inicial siempre es 1
start_segment = 1

# Ruta de la carpeta donde se descargará el archivo
output_dir = r"C:\Users\alfre\Documentos\Lahorafosca"
output_file = os.path.join(output_dir, "subtitles_combined.vtt")

# Inicializar el archivo de salida con la cabecera WEBVTT
with open(output_file, "w", encoding="utf-8") as outfile:
    outfile.write("WEBVTT\n\n")

# Descargar y combinar los subtítulos
for i in range(start_segment, end_segment + 1):
    # Crear la URL para cada segmento
    url = f"{base_url}{i}.vtt{token}"

    # Descargar el archivo VTT
    response = requests.get(url)

    # Verificar si la descarga fue exitosa
    if response.status_code == 200:
        print(f"Descargando segmento {i}")

        # Detectar la codificación del contenido recibido
        result = chardet.detect(response.content)
        encoding = result['encoding']

        # Leer el contenido con la codificación detectada
        vtt_content = response.content.decode(encoding).splitlines()

        # Guardar el contenido, omitiendo la primera línea (WEBVTT)
        with open(output_file, "a", encoding="utf-8") as outfile:
            outfile.write("\n".join(vtt_content[1:]) + "\n")
    else:
        print(f"Error al descargar el segmento {i}: {response.status_code}")

print(f"Subtítulos combinados guardados en {output_file}")
