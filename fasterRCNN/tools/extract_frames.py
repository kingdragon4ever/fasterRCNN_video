# -*- coding:utf-8 -*-

import cv2
from os.path import join


def extract_frames_from_video(path_video, dir_frames, frames_name, frames_name_size):
    # noinspection PyArgumentList
    cap = cv2.VideoCapture(path_video)
    num_frames = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2XYZ)
        # cv2.imshow("frame", frame)
        # if cv2.waitKey(41) & 0xFF == ord("q"):
        #    break
        str_counter = str(num_frames).zfill(frames_name_size)
        name = frames_name % str_counter
        path_frame = join(dir_frames, name)
        cv2.imwrite(path_frame, frame)
        print num_frames
        num_frames += 1
    print "All frames extracted from the video."
    cap.release()
    cv2.destroyAllWindows()
