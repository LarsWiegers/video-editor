import shlex
import subprocess
import numpy as np

acceleratedButNotCutVideoPath = 'acceleratedButNotCutVideoPath.mp4'
cutUpVideo = 'cutup.mp4'
finalVideo = 'output.mp4'

def get_frame_rate(filename):
    con = "ffprobe -v error -select_streams v:0 -show_entries stream=avg_frame_rate -of " \
          "default=noprint_wrappers=1:nokey=1 " + filename

    proc = subprocess.Popen(con, stdout=subprocess.PIPE, shell=True)
    framerateString = str(proc.stdout.read())[2:-5]
    a = int(framerateString.split('/')[0])
    b = int(framerateString.split('/')[1])
    return int(np.round(np.divide(a, b)))

def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            return output.strip()

def get_duration(filename):
    con = "ffprobe -show_entries stream=r_frame_rate,nb_read_frames -select_streams v -count_frames -of " \
          "compact=p=0:nk=1 -v 0 " + filename
    result = run_command(con)
    text = result.decode('ascii')

    frames = text.split("|")[1]
    durationFrame = text.split("/")[0]
    timesPerSecond = text.split("/")[1].split("|")[0]
    return int(frames) / int((int(durationFrame) / int(timesPerSecond)))


print("Hi, Welcome to the first version of the video editor, this version only supports increasing a video file by an "
      "x amount and adding music to it. This can be used when creating an timelapse.")
inputVideoFile = input('What is the file name of the video? Example: video.mkv: ')
speedUpRate = input("How much do you want to speed up the video? Example: Type 2 to speed the video up 2x: ")
musicAudioFile = input("what is the file name of the audio? Example: music.wav: ")

print("Program go brrrrr")
subprocess.call('ffmpeg -hide_banner -loglevel panic -i ' + inputVideoFile + ' -y -an -filter:v "setpts="' + str(round((1 / int(speedUpRate)), 1)) + '"*PTS" ' + acceleratedButNotCutVideoPath)
subprocess.call('ffmpeg -hide_banner -loglevel panic -i ' + acceleratedButNotCutVideoPath + ' -y -ss 00:00:00 -t 00:00:' + str(get_duration(inputVideoFile) / int(speedUpRate)) + ' -async 1 ' + cutUpVideo)
subprocess.call('ffmpeg -hide_banner -loglevel panic -i ' + cutUpVideo + ' -i ' + musicAudioFile + ' -y -map 0:v -map 1:a -c:v copy -shortest ' + finalVideo)
print("Looks like im done, see ya")