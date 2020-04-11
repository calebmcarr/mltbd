import argparse
import sys
import os, os.path, re
from shutil import copyfile
import cv2
#import libraries from other folders
sys.path.insert(1, '/darknet/python')
sys.path.insert(1, '/iou-tracker')
#import for detector
from detect_dknet import detect_img
#imports for tracker
from iou_tracker import track_iou
from util import load_mot
import build_array

#global FAR/Threshold 
FAR = 0.05

class tracker_args:
  detection_path = './data/detections'
  output_path = './data/tracks'
  frames_path = './data/frames'
  fmt = visdrone
  sigma_l = 0.9
  sigma_h = 0.98
  sigma_iou = 0.1
  t_min = 23
  ttl = 8
  nms = 0.6
  
def input_data(vid_loc):
  '''open video, store all frames to data/img_frames'''
  path_output_dir = './data/img_frames'
  video = cv2.VideoCapture(vid_loc)
  count = 0
  while(vidcap.isOpened():
        flag, img = video.read()
        if flag:
          cv2.imwrite(os.path.join(path_output_dir, '%d.png') % count, img)
          count += 1
        else:
          break
  cv2.destroyAllWindows()
  video.release()


def track(args):
  '''runs a detection, object-oriented version of demo.py'''
  detections = load_mot(args.detection_path, nms_overlap_thresh=args.nms, with_classes=with_classes)
  tracks = track_iou(detections, args.sigma_l, args.sigma_h, args.sigma_iou, args.t_min)
  tracks = build_array(tracks, fmt=args.format)
  return tracks

def detection(image,thresh):
  '''runs a darknet detection.  Returns an array of form [(object, probability, (b.x, b.y, b.w, b.h)), (object2....]
  image should be the path (relative to root) showing the input image zoomed in on a track's bounding boxes'''
  detections = detect_img(image,thresh)
  #TODO Write bit to save detections properly to args.detection_path, stand in now
  det_path_write()
  return detections

def ev_thresh(detections):
  det = len(detections)
  if(det > 1):
    FAR = FAR + .05
  else:
    pass

def gui_feed():
  external_call(frames,detects)

def main():
  args = tracker_args()
  frame_count = 0
  vid_loc = './data/video.mp4'
  #create bootstrap detection
  bootstrap = detection('./data/img_frames/1'+'.png',FAR)
  #enter loop where tracker is fed detections, detector fed tracks, and threshold evaluated as this changes
  while(1):
        #grab a set amt. of frames from ./data/frames and move it to args.frames_path
        #delete args.frame_path first
        for root, dirs, files in os.walk(args.frames_path):
          for file in files:
            os.remove(os.path.join(root, file))
        #grab next 100 frames from ./data/img_frames offset by frame_count
        for i in range(100):
          src = './data/img_frames'+str(i+frame_count)+'.png'
          copyfile(src,args.frames_path)
        frame_count += 100
        #call tracks now
        tracks = track(args)
        #TODO write bit to zoom in on frames with tracks, change args.frames_path
        #call detection() on last image in args.frames_path 
        detections = detection(args.frames_path+'/'+str(frame_count-1)+'.png')
        #call ev_thresh() to see if FAR shoud be updated
        ev_thresh()
        
