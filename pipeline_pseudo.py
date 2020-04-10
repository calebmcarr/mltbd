import argparse

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
  
def input_data(data):
  if(data == file):
    open_file()
    return file_handle
  elif(data == stream):
    open_buffer()
    return buffer_handle


def track(args):
  '''runs a detection, object-oriented version of demo.py'''
  detections = load_mot(args.detection_path, nms_overlap_thresh=args.nms, with_classes=with_classes)
  tracks = track_iou(detections, args.sigma_l, args.sigma_h, args.sigma_iou, args.t_min)
  tracks = build_array(tracks, fmt=args.format)
  return tracks

def detection(args):
  detects = darknet(frames)
  detects = detects_csv()
  return detects

def ev_thresh(tracks,detects):
  tr = len(tracks)
  det = len(detects)
  if(tr>det):
    FAR = FAR + .05
  return FAR

def gui_feed():
  external_call(frames,detects)

def main():
  args = tracker_args()
