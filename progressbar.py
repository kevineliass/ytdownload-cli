from progress.bar import ChargingBar
from logger import console

bar = ChargingBar('Descargando: ', max=100)
progress_tmp = 0

def progress_bar(stream, data_chunk, bytes_remaining):
    global bar
    global progress_tmp
    current_progress = 100 - ((bytes_remaining * 100) / stream.filesize)
    bar.next(n=current_progress - progress_tmp)
    progress_tmp = current_progress
    if current_progress == 100:
        bar.finish()
# if stream.filesize _____ 100%
# else bytes_remaining ___ x

def finish_download(stream, file_path):
    console.log(f'Se descargo {file_path}')