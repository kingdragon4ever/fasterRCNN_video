import subprocess
from os.path import join


def add_audio_to_video(path_video, dir_processed_video, name_processed_video, dir_audio, name_audio,
                       name_processed_video_with_audio):
    path_audio = join(dir_audio, name_audio)
    path_processed_video = join(dir_processed_video, name_processed_video)
    path_processed_video_with_audio = join(dir_processed_video, name_processed_video_with_audio)

    command = "ffmpeg -i {video} -ab 160k -ac 2 -ar 44100 -vn {audio}".format(video=path_video, audio=path_audio)
    subprocess.call(command, shell=True)

    command = "ffmpeg -itsoffset 3 -i {vid_pro} -i {audio} -codec copy -shortest {vid_pro_audio}".format(
        vid_pro=path_processed_video, audio=path_audio, vid_pro_audio=path_processed_video_with_audio)
    subprocess.call(command, shell=True)
