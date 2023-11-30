from pathlib import Path

def absPath(file):
    """
    Obtiene la ruta absoluta de un archivo en relación con el directorio actual del script.

    Parámetros:
    - file (str): Nombre del archivo.

    Retorna:
    - str: Ruta absoluta del archivo.
    """
    return str(Path(__file__).parent.absolute() / file)


def existsFile(file):
    """
    Verifica si un archivo existe en el sistema de archivos.

    Parámetros:
    - file (str): Ruta del archivo a verificar.

    Retorna:
    - bool: True si el archivo existe, False en caso contrario.
    """
    return Path(file).is_file()

