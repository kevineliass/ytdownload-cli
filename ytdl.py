from pytube import YouTube
from logger import console
from pathlib import Path
import os
import subprocess

from progressbar import progress_bar
import media

class YouTubeDownload:
    def __init__(self, source, interactive, skip_existing, output_path):
        self.source = source
        self.interactive = interactive
        self.skip_existing = skip_existing
        self.output_path = output_path
        self.yt = YouTube(source, on_progress_callback=progress_bar, on_complete_callback=None)
        self.default_filename = self.yt.streams.get_audio_only().default_filename
        self.TMP_VIDEO_FILE = output_path / '.video00000001.mp4.tmp'
        self.TMP_AUDIO_FILE = output_path / '.audio00000001.mp4.tmp'

    def download(self, stream, filename, output_path):
        dl = stream.download(filename=filename, output_path=output_path, skip_existing=False)
        return Path(dl)

    def download_video(self):
        self.show_info()
        file_video = self.set_filename(extension='.mp4')
        if self.skip(file_video):
            console.warn(f'Saltando "{file_video.name}"')
            return 'SKIP'
        resolution, stream = self.set_resolution()
        console.log('Descargando Video...')
        video_tmp = self.download(stream, self.TMP_VIDEO_FILE, output_path=self.output_path)
        console.log('Descargando Audio...')
        audio_tmp = self.download(self.yt.streams.get_audio_only(), self.TMP_AUDIO_FILE, output_path=self.output_path)
        console.log('Uniendo archivos multimedia...')
        self.process_video(video_tmp, audio_tmp, file_video)
        console.log('Eliminando archivos temporales')
        self.delete_temporary_files()
        console.log(f'Terminado para "{file_video}"')

    def download_audio(self):
        self.show_info()
        stream = self.yt.streams.get_audio_only() # mp4 default
        file = self.set_filename(extension='.mp3') # archivo final
        if self.skip(file):
            console.warn(f'Saltando "{file.name}"')
            return 'SKIP'
        console.log('Iniciando descarga')
        dl_tmp = self.download(stream, self.TMP_AUDIO_FILE, self.output_path) # archivo temporal de audio
        console.log('Convirtiendo a formato mp3')
        media.convert_to_mp3(dl_tmp, file)
        console.log('Eliminando archivos temporales')
        self.delete_temporary_files()
        console.log(f'Terminado para "{file}"')

    def skip(self, file):
        if file.exists() and self.skip_existing:
            return True
        elif file.exists() and not self.skip_existing:
            console.warn(f'Eliminando para sobreescribir "{file.name}"')
            os.remove(file.absolute())
        return False

    def set_resolution(self):
        streams = self.yt.streams.filter(mime_type='video/mp4').order_by('resolution')
        resolution_dict = {}
        for stream in streams: # filtramos las resoluciones disponibles para que no se repita ninguna
            if not stream.resolution in resolution_dict:
                resolution_dict[stream.resolution] = stream
        resolutions = list(resolution_dict.keys())
        if self.interactive:
            console.print(f'Resoluciones disponibles: {resolutions}')
            resolution = console.input('>>> ')
            if resolution == '' or not resolution in resolutions:
                resolution = resolutions[-1]
                console.warn(f'Se establecion el valor por defecto: {resolution}')
            return resolution, resolution_dict[resolution]
        resolution = resolutions[-1]
        console.warn(f'Descargando en: {resolution}')
        return resolution, resolution_dict[resolution]

    def set_filename(self, extension='.mp4'):
        default_filename = (self.output_path / self.default_filename).with_suffix(extension)
        if self.interactive:
            filename = console.input('Guardar como: ')
            filename = default_filename if filename == '' else default_filename.with_name(filename).with_suffix(extension)
            return filename
        return default_filename
    
    # ffmpeg -i video.mp4 -i audio.m4a -c:v copy -c:a copy output.mp4
    def process_video(self, video_file, audio_file, output):
        cmd = f'ffmpeg -i "{video_file.absolute()}" -i "{audio_file.absolute()}" -c:v copy -c:a copy "{output.absolute()}"'
        subprocess.run(cmd, shell=True, capture_output=True)
    
    def delete_temporary_files(self):
        if self.TMP_AUDIO_FILE.exists():
            os.remove(self.TMP_AUDIO_FILE.absolute())
        if self.TMP_VIDEO_FILE.exists():
            os.remove(self.TMP_VIDEO_FILE.absolute())

    def show_info(self):
        console.print('*' * 50)
        console.print(f'Titulo: {self.yt.title}')
        console.print(f'Canal: {self.yt.author}')
        console.print(f'Vistas: {self.yt.views}')
        console.print('*' * 50)