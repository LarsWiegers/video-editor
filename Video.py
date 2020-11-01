import shlex
import subprocess
import numpy as np


class Video:
    def __init__(self, file):
        self.file = file
        self.acceleratedButNotCutVideoPath = 'acceleratedButNotCutVideoPath.mp4'
        self.cutUpVideo = 'cutup.mp4'
        self.finalVideo = 'output.mp4'

    def get_frame_rate(self):
        con = "ffprobe -v error -select_streams v:0 -show_entries stream=avg_frame_rate -of " \
              "default=noprint_wrappers=1:nokey=1 " + self.file

        proc = subprocess.Popen(con, stdout=subprocess.PIPE, shell=True)
        framerateString = str(proc.stdout.read())[2:-5]
        a = int(framerateString.split('/')[0])
        b = int(framerateString.split('/')[1])
        return int(np.round(np.divide(a, b)))

    def get_duration(self):
        con = "ffprobe -show_entries stream=r_frame_rate,nb_read_frames -select_streams v -count_frames -of " \
              "compact=p=0:nk=1 -v 0 " + self.file
        text = self.run_command(con)

        frames = text.split("|")[1]
        durationFrame = text.split("/")[0]
        timesPerSecond = text.split("/")[1].split("|")[0]
        return int(frames) / int((int(durationFrame) / int(timesPerSecond)))

    @staticmethod
    def run_command(command):
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                return output.strip().decode('ascii')

    def speed_up(self, speed_up_rate):
        self.run_command(
            'ffmpeg -hide_banner -loglevel panic -i ' + self.file + ' -y -an -filter:v "setpts="' + str(
                round((1 / int(speed_up_rate)), 1)) + '"*PTS" ' + self.acceleratedButNotCutVideoPath)

        self.run_command(
            'ffmpeg -hide_banner -loglevel panic -i '
            + self.acceleratedButNotCutVideoPath
            + ' -y -ss 00:00:00 -t 00:00:'
            + str(self.get_duration() / int(speed_up_rate))
            + ' -async 1 ' + self.cutUpVideo)

    def add_in_audio(self, music_audio_file):
        self.run_command(
            'ffmpeg -hide_banner -loglevel panic -i '
            + self.cutUpVideo
            + ' -i '
            + music_audio_file
            + ' -y -map 0:v -map 1:a -c:v copy -shortest '
            + self.finalVideo)

    def get_result_file_name(self):
        return self.finalVideo
