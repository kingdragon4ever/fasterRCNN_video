# -*- coding:utf-8 -*-

import cv2
from os import listdir
from os.path import join


def generate_processed_video(dir_processed_frames, frames_name, frames_name_size, dir_processed_video,
                             processed_video_name):
    first_frame_name = frames_name % str(0).zfill(frames_name_size)
    path_first_frame = join(dir_processed_frames, first_frame_name)
    img_model = cv2.imread(path_first_frame)
    height, width, layers = img_model.shape
    path_processed_video = join(dir_processed_video, processed_video_name)
    video = cv2.VideoWriter(path_processed_video, cv2.cv.FOURCC("M", "J", "P", "G"), 24, (width, height))
    for image_name in sorted(listdir(dir_processed_frames)):
        image_path = join(dir_processed_frames, image_name)
        print image_path
        image = cv2.imread(image_path)
        video.write(image)
    cv2.destroyAllWindows()
    video.release()
