
from pytube import YouTube
#melhor qualidade de audio
#streams = YouTube('https://youtu.be/9bZkp7q19f0').streams.filter(only_audio=True, file_extension='mp4').desc()
yt = YouTube('https://www.youtube.com/watch?v=9YEno3UBDe0')
thumbnail_url = yt.thumbnail_url
stream = yt.streams.filter(progressive=True, file_extension='mp4')


quality_list = [s.resolution for s in stream]

print(quality_list)