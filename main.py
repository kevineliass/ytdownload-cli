#!/usr/bin/python3
from logger import console
from cli import cli
from ytdl import YouTubeDownload
from pytube import Playlist
from pathlib import Path

class YouTubeDownloadError(Exception):
    pass

def download(video, audio, source, interactive, skip_existing, output_path):
    yt = YouTubeDownload(source, interactive, skip_existing, output_path)
    if video:
        yt.download_video()
    elif audio:
        yt.download_audio()
    else:
        console.log('Esto nunca se va a ejecutar ;)')

def main(args=None):
    if not args.list: # si es solo un enlace directo
        download(args.video, args.audio, args.source, args.interactive, args.skip_existing, args.output_path)
    else: # si es una lista de reproducción
        console.log('Obteniendo elementos de la lista de reproducción')
        pl = Playlist(args.source)
        console.print('----------------------------------------')
        console.print(f'Titulo de la playlist: {pl.title}')
        console.print(f'Número de elementos: {pl.length}')
        console.print('----------------------------------------')
        console.print('') # creamos una carpeta para las descargas con el titulo de la playlist
        folder = args.output_path / pl.title
        if folder.exists():
            console.warn(f'Se usara el directorio existente con el nombre de la playlist "{folder}"')
        else:
            console.log(f'Creando directorio con el nombre de la playlist "{folder}"')
            folder.mkdir()
        for index, url in enumerate(pl.video_urls, start=1):
            console.print(f'[{index}]  {url}')
            download(args.video, args.audio, url, args.interactive, args.skip_existing, Path(folder.absolute()))
            console.print('')


if __name__ == '__main__':
    args = cli()
    try:
        main(args)
    except KeyboardInterrupt:
        console.err('Programa interrumpido por el usuario!')
        exit(1)
    except YouTubeDownloadError as err:
        console.err(err)
        exit(1)
    finally:
        console.log('Termino la ejecución')
