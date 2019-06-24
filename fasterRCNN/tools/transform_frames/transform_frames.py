# -*- coding:utf-8 -*-

import os
import shutil
from transform_image import change_all_images_from_bgr_to_other, apply_filter_to_all_images, equalize_all_bgr_images
from transform_image import BGR_TO_XYZ, BGR_TO_GRAY, BGR_TO_HSV, HIGH_PASS_FILTER, LOW_PASS_FILTER

DIR_FRAMES = "../frames"
DIR_XYZ_FRAMES = "frames_xyz"
DIR_HSV_FRAMES = "frames_hsv"
DIR_GRAY_FRAMES = "frames_gray"
DIR_EQ_FRAMES = "frames_eq"
DIR_HP_FILTER_FRAMES = "frames_hp_filter"
DIR_LP_FILTER_FRAMES = "frames_lp_filter"


def make_dirs(dir_names):
    for dir_name in dir_names:
        shutil.rmtree(dir_name, ignore_errors=True)
        try:
            os.makedirs(dir_name)
        except OSError:
            if not os.path.isdir(dir_name):
                raise


def main():
    make_dirs([DIR_XYZ_FRAMES, DIR_HSV_FRAMES, DIR_GRAY_FRAMES, DIR_EQ_FRAMES, DIR_HP_FILTER_FRAMES,
               DIR_LP_FILTER_FRAMES])
    change_all_images_from_bgr_to_other(DIR_FRAMES, DIR_XYZ_FRAMES, BGR_TO_XYZ)
    change_all_images_from_bgr_to_other(DIR_FRAMES, DIR_HSV_FRAMES, BGR_TO_HSV)
    change_all_images_from_bgr_to_other(DIR_FRAMES, DIR_GRAY_FRAMES, BGR_TO_GRAY)
    equalize_all_bgr_images(DIR_FRAMES, DIR_EQ_FRAMES)
    apply_filter_to_all_images(DIR_FRAMES, DIR_HP_FILTER_FRAMES, HIGH_PASS_FILTER)
    apply_filter_to_all_images(DIR_FRAMES, DIR_LP_FILTER_FRAMES, LOW_PASS_FILTER)


if __name__ == "__main__":
    main()
