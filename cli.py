from argparse import ArgumentParser
from pathlib import Path

def cli():
    parse = ArgumentParser(prog='YouTube Download', description='Descarga videos o audio de youtube.com')
    parse.add_argument('source', type=str, help='Url de un video o lista de reproducción')
    type_download = parse.add_mutually_exclusive_group(required=True)
    type_download.add_argument('-v', '--video', action='store_true', help='Establece descarga de video')
    type_download.add_argument('-a', '--audio', action='store_true', help='Establece descarga de audio')
    parse.add_argument('-i', '--interactive', action='store_true', help='Pregunta en tiempo de ejecución nombre del archivo o resolución de descarga')
    parse.add_argument('-sE', '--skip-existing', action='store_true', help='Saltar archivos que ya existan')
    parse.add_argument('-oP', '--output-path', type=Path, default=Path('.'), help='Ruta donde se guardaran las descargas')
    parse.add_argument('-l', '--list', action='store_true', help='Procesar el source como una url hacia una lista de reproducción en youtube')
    return parse.parse_args()