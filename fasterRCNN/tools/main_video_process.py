# -*- coding:utf-8 -*-

import os
import sys
import shutil
from extract_frames import extract_frames_from_video
from detect_objects import detect_objects_in_frames
from generate_video import generate_processed_video
from copy_audio import add_audio_to_video

CLASSES = ('__background__',
           'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
           'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep',
           'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'hat', 'umbrella', 'handbag', 'tie', 'suitcase',
           'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
           'surfboard', 'tennis racket',
           'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich',
           'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant',
           'bed', 'dining table', 'window', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave',
           'oven', 'sink', 'refrigerator', 'blender', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
           'tooth brush')

DIR_AUDIO = "audio"
NAME_AUDIO = "audio.wav"
DIR_FRAMES = "frames"
DIR_PROCESSED_FRAMES = "processed"
DIR_PROCESSED_VIDEO = "processed_video"
FRAMES_NAME = "FRAME%s.jpg"
FRAMES_NAME_SIZE = 4
PROCESSED_VIDEO_NAME = "processed_video.avi"
PROCESSED_VIDEO_WITH_AUDIO_NAME = "processed_video_with_audio.avi"

PROTOTXT = "py-faster-rcnn/models/coco/VGG16/faster_rcnn_end2end/test.prototxt"
CAFFEMODEL = "py-faster-rcnn/data/coco_models/coco_vgg16_faster_rcnn_final.caffemodel"


def make_dirs(dir_names):
    for dir_name in dir_names:
        shutil.rmtree(dir_name, ignore_errors=True)
        try:
            os.makedirs(dir_name)
        except OSError:
            if not os.path.isdir(dir_name):
                raise


def main(path_video):
    make_dirs([DIR_AUDIO, DIR_FRAMES, DIR_PROCESSED_FRAMES, DIR_PROCESSED_VIDEO])
    extract_frames_from_video(path_video, DIR_FRAMES, FRAMES_NAME, FRAMES_NAME_SIZE)
    detect_objects_in_frames(DIR_FRAMES, DIR_PROCESSED_FRAMES, PROTOTXT, CAFFEMODEL, CLASSES)
    generate_processed_video(DIR_PROCESSED_FRAMES, FRAMES_NAME, FRAMES_NAME_SIZE, DIR_PROCESSED_VIDEO,
                             PROCESSED_VIDEO_NAME)
    add_audio_to_video(path_video, DIR_PROCESSED_VIDEO, PROCESSED_VIDEO_NAME, DIR_AUDIO, NAME_AUDIO,
                       PROCESSED_VIDEO_WITH_AUDIO_NAME)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "ERROR: Parameter not found: Path of the original video"
        print "USAGE: main_video_process.py <video_path>"
    else:
        print "STARTING MAIN VIDEO PROCESS"
        main(sys.argv[1])
