
from pytube import YouTube
#melhor qualidade de audio
#streams = YouTube('https://youtu.be/9bZkp7q19f0').streams.filter(only_audio=True, file_extension='mp4').desc()
yt = YouTube('https://www.youtube.com/watch?v=3WHhIe8k44M')
thumbnail_url = yt.thumbnail_url
stream = yt.streams.filter(file_extension='mp4',only_video=True,adaptive=True)


quality_list = [s.resolution for s in stream]

print(quality_list)


# urls = {
#     "private_video":"https://www.youtube.com/watch?v=Ki_Szad3hNE", 
#     "private_playlist":"https://www.youtube.com/playlist?list=PLLcS6ldQh_lwGNK3Nx-aDikadwYLLyFM9",
#     "invalid_url":"link", 
#     "playlist_url":"https://www.youtube.com/playlist?list=PLLcS6ldQh_lwxzNRjsAgwjVg_CcOJsxFd",
#     "short":"https://www.youtube.com/shorts/89pR3PQsxpg",
#     "video_on_playlist":"https://www.youtube.com/watch?v=BiQIc7fG9pA&list=RDGMEM6ijAnFTG9nX1G-kbWBUCJAVMJnzVOgNR_rE&index=27"
# }

# for name,url in urls.items():
#     print("\n\n")
#     link = YouTubeLink(url)
#     label = f"{name} {link.available_for_download()} \nis video {link.is_video} is playlist {link.is_playlist} "
#     print(label)