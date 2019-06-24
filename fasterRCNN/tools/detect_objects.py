import _init_paths
import os
import cv2
import caffe
import numpy as np
import matplotlib.pyplot as plt
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms


# noinspection PyTypeChecker
def vis_detections(class_name, dets, ax, color, thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return

    for i in inds:
        bbox = dets[i, :4]
        score = dets[i, -1]

        ax.add_patch(
            plt.Rectangle((bbox[0], bbox[1]),
                          bbox[2] - bbox[0],
                          bbox[3] - bbox[1], fill=False,
                          edgecolor=color, linewidth=3.5)
        )
        ax.text(bbox[0], bbox[1] - 2,
                '{:s} {:.3f}'.format(class_name, score),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=14, color='white')


# noinspection PyTypeChecker
def analyze_frame(net, image_name, dir_frames, dir_processed_frames, classes):
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the demo image
    im_file = os.path.join(dir_frames, image_name)
    im = cv2.imread(im_file)

    # Detect all object classes and regress object bounds
    scores, boxes = im_detect(net, im)

    # Visualize detections for each class
    conf_thresh = 0.8
    nms_thresh = 0.3
    fig, ax = plt.subplots(figsize=(16, 8))
    im_pro = im[:, :, (2, 1, 0)]
    ax.imshow(im_pro, aspect='equal')
    color_list = plt.cm.Set1(np.linspace(0, 1, 9))
    for cls_ind, cls in enumerate(classes[1:]):
        cls_ind += 1  # because we skipped background
        color = color_list[(cls_ind-1) % 9]
        cls_boxes = boxes[:, 4 * cls_ind:4 * (cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, nms_thresh)
        dets = dets[keep, :]
        vis_detections(cls, dets, ax, color, thresh=conf_thresh)
    plt.axis('off')
    fig.tight_layout()
    plt.savefig(os.path.join(dir_processed_frames, image_name), facecolor="black")
    plt.close(fig)


def detect_objects_in_frames(dir_frames, dir_processed_frames, prototxt, caffemodel, classes):
    cfg.TEST.HAS_RPN = True  # Use RPN for proposals

    caffe.set_mode_gpu()
    caffe.set_device(0)
    cfg.GPU_ID = 0
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)

    print '\n\nLoaded network {:s}'.format(caffemodel)

    # Warmup on a dummy image
    im = 128 * np.ones((300, 500, 3), dtype=np.uint8)
    for i in xrange(2):
        _, _ = im_detect(net, im)

    im_names = os.listdir(dir_frames)
    for index, im_name in enumerate(sorted(im_names)):
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print 'Processing frame: {}'.format(im_name)
        analyze_frame(net, im_name, dir_frames, dir_processed_frames, classes)
