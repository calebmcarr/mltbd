import argparse
import sys
import os
import cv2
#import libraries from other folders
sys.path.insert(1, '/darknet/python')
sys.path.insert(1, '/iou-tracker')
#import for detector
import detect_dknet
#imports for tracker
from iou_tracker import track_iou
from util import load_mot
import build_array

#global FAR/Threshold 
FAR = 0.05

class tracker_args:
  detection_path = ''
  output_path = ''
  frames_path = ''
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

def detection(image):
  '''runs a darknet detection.  Returns an array of form [(object, probability, (b.x, b.y, b.w, b.h)), (object2....]
  image should be the path (relative to root) showing the input image zoomed in on a track's bounding boxes'''
  detections = detect_img(image)
  return detections

def ev_thresh(tracks,detections):
  tr = len(tracks)
  det = len(detects)
  if(tr>det):
    FAR = FAR + .05
  return FAR

def gui_feed():
  external_call(frames,detects)

def main():
  args = tracker_args()
  vid_loc = './data/video.mp4'
  #create bootstrap detection
  bootstrap = detection('./data/img_frames/1/png')
  #enter loop where tracker is fed detections, detector fed tracks, and threshold evaluated as this changes
