# -*- coding:utf8 -*-
import os
import cv2
import numpy as np

path = './yichang3/3/'
filelist = os.listdir(path)
total_num = len(filelist)


video=cv2.VideoWriter("./yichang3/3/VideoTest.mp4", cv2.VideoWriter_fourcc('m','p','4','v'), 15, (1200,1200))
for item in filelist:
  if item.endswith('.jpg'):
           item='./yichang3/3/'+item
           img1 = cv2.imread(item)
     #      print (item)


           video.write(img1)
           cv2.imshow("Image", img1)
           key=cv2.waitKey(100)


video.release()
cv2.destroyAllWindows()
