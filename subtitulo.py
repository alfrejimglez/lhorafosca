import os
import chardet
import requests
import re
import time

# Pedir la URL completa al usuario
full_url = input("Introduce la URL completa de uno de los segmentos ")

# Usar una expresión regular para extraer la URL base, el token, y el número del segmento final
match = re.match(r"(.*segment)(\d+)\.vtt(\?.*)", full_url)
if not match:
    print("La URL no tiene el formato esperado.")
    exit()

base_url = match.group(1)  # Parte de la URL hasta 'segment'
token = match.group(3)  # Token después del .vtt

# Asumimos que el segmento inicial siempre es 1
start_segment = 1

# Ruta de la carpeta donde se descargará el archivo
output_dir = os.getcwd()
output_file = os.path.join(output_dir, "subtitles_combined.vtt")

# Asegurar que la carpeta de salida exista
os.makedirs(output_dir, exist_ok=True)

# Inicializar el archivo de salida con la cabecera WEBVTT
with open(output_file, "w", encoding="utf-8") as outfile:
    outfile.write("WEBVTT\n\n")

# Descargar y combinar los subtítulos
i = start_segment
while True:
    url = f"{base_url}{i}.vtt{token}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            print(f"Descargando segmento {i}")

            result = chardet.detect(response.content)
            encoding = result["encoding"] or "utf-8"

            vtt_content = response.content.decode(encoding).splitlines()

            with open(output_file, "a", encoding="utf-8") as outfile:
                outfile.write("\n".join(vtt_content[1:]) + "\n")
            i += 1
        else:
            print(f"Fin de segmentos en {i}: {response.status_code}")
            break

    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el segmento {i}: {e}")
        break

    time.sleep(0.5)

print(f"Subtítulos combinados guardados en {output_file}")
