from pydub import AudioSegment

def convert_to_mp3(source,  output):
    f = AudioSegment.from_file(source.absolute())
    f.export(output.absolute(), format='mp3')
    return True