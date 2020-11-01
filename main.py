from Video import Video

print("Hi, Welcome to the first version of the video editor, this version only supports increasing a video file by an "
      "x amount and adding music to it. This can be used when creating an timelapse.")
inputVideoFile = input('What is the file name of the video? Example: video.mkv: ')
speedUpRate = input("How much do you want to speed up the video? Example: Type 2 to speed the video up 2x: ")
musicAudioFile = input("what is the file name of the audio? Example: music.wav: ")

video_to_change = Video(inputVideoFile)

print("Program go brrrrr")

video_to_change.speed_up(speedUpRate)
video_to_change.add_in_audio(musicAudioFile)
print("Created the file: " + video_to_change.get_result_file_name())
print("Looks like im done, see ya")