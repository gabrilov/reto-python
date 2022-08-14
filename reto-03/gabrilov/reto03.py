#!/usr/bin/env python
import toml
from os import scandir, environ, path, makedirs
from magic import Magic
import re


path_to_config_file = f"{environ['HOME']}/.config/diogenes"
config_file= f"{path_to_config_file}/diogenes.conf"


# Lista los jpg de la ruta que se pase como parámetro
def ls_jpg(ruta: str) -> list[str]:
    mime = Magic(mime=True)
    return [arch.name for arch in scandir(
        ruta) if arch.is_file() and mime.from_file(arch) == 'image/jpeg']


# Obtiene el directorio de descargas del usuario
def get_download_dir_from_system() -> str:
    homepath: str = environ['HOME']
    carpeta: str = ''
    with open(homepath + '/.config/user-dirs.dirs', 'rt') as archivo_dir:
        contenido: list[str] = archivo_dir.readlines()
    for _, linea in enumerate(contenido):
        resultado = re.search(
            r'XDG_DOWNLOAD_DIR="\$HOME\/([a-zA-Z0-9].*)"$', linea)
        if resultado is not None:
            carpeta = resultado.group(1)
        if carpeta is None:
            exit("No hay definida carpeta de descargas")
    return f"{homepath}/{carpeta}"


# Devuelve el contenido del archivo de configuración
# y si no existe, lo crea
def check_config_file() -> dict[str, str]:
    if not path.exists(config_file): 
        create_config_file()       
    return read_config_file()


# Crea un archivo de configuración con el contenido por defecto
def create_config_file():
    config_file_content = {"directorio": get_download_dir_from_system()}
    if not path.exists(path_to_config_file):
        makedirs(path_to_config_file)
    with open(config_file, 'w') as f:
        toml.dump(config_file_content, f)
        

# Devuelve el contenido del archivo de configuración        
def read_config_file() -> dict[str, str]:
    try:
        return toml.load(config_file)
    except:
        exit("Error leyendo archivo de configuración")        


def main():
    config_file_content = check_config_file()
    # Obtenemos una cadena con la ruta de descargas
    download_path = config_file_content["directorio"]
    print(f'Carpeta de descargas: {download_path}\n')
    archivos_descargas: list[str] = ls_jpg(download_path)
    for index, archivo in enumerate(archivos_descargas):
        prefix: str = "=>" if (index + 1) % 2 == 0 else ""
        print(f'{index + 1} {prefix} {archivo}')


if __name__ == "__main__":
    main()
