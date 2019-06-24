# -*- coding: utf-8 -*
#!/usr/bin/env python

# --------------------------------------------------------
# Faster R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""
Demo script showing detections in sample images.

See README.md for installation instructions before running.
"""

import _init_paths
from fast_rcnn.config import cfg
from fast_rcnn.test import im_detect
from fast_rcnn.nms_wrapper import nms
from utils.timer import Timer
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import caffe, os, sys,cv2
import argparse
import gc

global j
j=1
CLASSES = ('__background__',
             'person')

NETS = {'vgg16': ('VGG16',
                  'animal.caffemodel'),
        'zf': ('ZF',
                  'ZF_faster_rcnn_final.caffemodel')}

x=[]

def vis_detections(im, class_name, dets, thresh=0.5):
    """Draw detected bounding boxes."""
    inds = np.where(dets[:, -1] >= thresh)[0]
    if len(inds) == 0:
        return
    
    x.append(len(inds))
    file=open('data.txt','w') 
    file.write(str(x)); 
    file.close()  
    #print(x)
    if len(inds) >= 1:
        im = im[:, :, (2, 1, 0)]
        fig, ax = plt.subplots(figsize=(12, 12))
        ax.imshow(im, aspect='equal')
        flag=0
        for i in inds:
            bbox = dets[i, :4]
            score = dets[i, -1]
            ax.add_patch(
                plt.Rectangle((bbox[0], bbox[1]),
                              bbox[2] - bbox[0],
                              bbox[3] - bbox[1], fill=False,
                              edgecolor='red', linewidth=3.5))
            print "x1"+str(j)+"="+str(int(bbox[0]))+";","y1"+str(j)+"="+str(int(bbox[1]))+";","x2"+str(j)+"="+str(int(bbox[2]))+";","y2"+str(j)+"="+str(int(bbox[3]))+";"
            ax.text(bbox[0], bbox[1] - 2,
                    '{:s} {:.3f}'.format(class_name, score),
                    bbox=dict(facecolor='blue', alpha=0.5),
                    fontsize=14, color='white')
            print(i+1)
        ax.set_title(('{} detections with '
                      'p({} | box) >= {:.1f}').format(class_name, class_name,
                                                  thresh),
                      fontsize=14)
   
        plt.axis('off')
        plt.tight_layout()
        flag=flag+1
    #f = open("test.txt",'wb')
    #f.write(str(inds+1))
    #f.close()
        print('number:'+str(inds+1))

  
    

        plt.draw()
def demo(net, image_name):
    """Detect object classes in an image using pre-computed object proposals."""

    # Load the demo image
    im_file = os.path.join(cfg.DATA_DIR, 'demo', image_name)
    im = cv2.imread(im_file)

    # Detect all object classes and regress object bounds
    timer = Timer()
    timer.tic()
    scores, boxes = im_detect(net, im)
    timer.toc()
    f = open('location',mode='ab')
    f.write(boxes)
    f.close()
    print ('Detection took {:.3f}s for '
           '{:d} object proposals').format(timer.total_time, boxes.shape[0])

    # Visualize detections for each class
    CONF_THRESH = 0.7
    NMS_THRESH = 0.1
    for cls_ind, cls in enumerate(CLASSES[1:]):
        cls_ind += 1 # because we skipped background
        cls_boxes = boxes[:, 4*cls_ind:4*(cls_ind + 1)]
        cls_scores = scores[:, cls_ind]
        dets = np.hstack((cls_boxes, cls_scores[:, np.newaxis])).astype(np.float32)
        keep = nms(dets, NMS_THRESH)
        dets = dets[keep, :]
        vis_detections(im, cls, dets, thresh=CONF_THRESH)
        global j
        j=j+1
        if j>=5:
             j=1
def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Faster R-CNN demo')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]',
                        default=0, type=int)
    parser.add_argument('--cpu', dest='cpu_mode',
                        help='Use CPU mode (overrides --gpu)',
                        action='store_true')
    parser.add_argument('--net', dest='demo_net', help='Network to use [vgg16]',
                        choices=NETS.keys(), default='vgg16')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    cfg.TEST.HAS_RPN = True  # Use RPN (region proposal Network) for proposals

    args = parse_args()

    prototxt = os.path.join(cfg.MODELS_DIR, NETS[args.demo_net][0],
                            'faster_rcnn_alt_opt', 'faster_rcnn_test.pt')
    caffemodel = os.path.join(cfg.DATA_DIR, 'faster_rcnn_models',
                              NETS[args.demo_net][1])

    if not os.path.isfile(caffemodel):
        raise IOError(('{:s} not found.\nDid you run ./data/script/'
                       'fetch_faster_rcnn_models.sh?').format(caffemodel))

    if args.cpu_mode:
        caffe.set_mode_cpu()
    else:
        caffe.set_mode_gpu()
        caffe.set_device(args.gpu_id)
        cfg.GPU_ID = args.gpu_id
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)

    print '\n\nLoaded network {:s}'.format(caffemodel)

    # Warmup on a dummy image
    im = 128 * np.ones((300, 500, 3), dtype=np.uint8)
    for i in xrange(2):
        _, _= im_detect(net, im)

    im_names =['0001.jpg','0002.jpg','0003.jpg','0004.jpg','0005.jpg','0006.jpg','0007.jpg','0008.jpg','0009.jpg','0010.jpg','0011.jpg','0012.jpg','0013.jpg','0014.jpg','0015.jpg','0016.jpg','0017.jpg','0018.jpg','0019.jpg','0020.jpg','0021.jpg','0022.jpg','0023.jpg','0024.jpg','0025.jpg','0026.jpg','0027.jpg','0028.jpg','0029.jpg','0030.jpg','0031.jpg','0032.jpg','0033.jpg','0034.jpg','0035.jpg','0036.jpg','0037.jpg','0038.jpg','0039.jpg','0040.jpg','0041.jpg','0042.jpg','0043.jpg','0044.jpg','0045.jpg','0046.jpg','0047.jpg','0048.jpg','0049.jpg','0050.jpg']
    for im_name in im_names:
        #inds = np.where(vis_detections.dets[:, -1] >= thresh)[0]
        #if len(inds) >= 10:
            print 'Demo for data/demo/{}'.format(im_name)
            demo(net, im_name)
            plt.savefig("./print/"+im_name)
     #   gc.collect()
    #plt.show()
