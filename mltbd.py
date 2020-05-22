import argparse
import sys
import os, os.path, re
from shutil import copyfile
import cv2
import numpy as np
#import libraries from other folders
sys.path.insert(1, './darknet/python')
sys.path.insert(1, './iou-tracker')
#import for detector
from detect_dknet import detect_img
#imports for tracker
from iou_tracker import track_iou
from util import load_mot
from util import iou
from format import build_array
from format import build_array2
#global FAR/Threshold 
FAR = 0.05

class tracker_args:
  detection_path = './data/detections'
  output_path = './data/tracks'
  frames_path = './data/frames'
  fmt = 'motchallenge'
  #sigma_l = 0.9
  sigma_l = 0.05
  #sigma_h = 0.98
  sigma_h = 0.05
  sigma_iou = 0.1
  #t_min = 23
  t_min = 1
  ttl = 8
  nms = 0.6
  
def input_data(vid_loc):
  '''open video, store all frames to data/img_frames'''
  path_output_dir = './data/img_frames'
  video = cv2.VideoCapture(vid_loc)
  count = 0
  while(video.isOpened()):
        flag, img = video.read()
	if (count > 100):
	  break
	else:
	  pass
        if flag:
          cv2.imwrite(os.path.join(path_output_dir, '%d.png') % count, img)
	  print('\t[-] Frame '+str(count))
          count += 1
        else:
          break
  cv2.destroyAllWindows()
  video.release()


def tracker(args,detections):
  '''runs a detection, object-oriented version of demo.py'''
  #might need to add nms to load_mot
  dets = load_mot(detections, with_classes = 0)
  print('\t[-] Track with Intersection over Union')
  tracks = track_iou(dets, args.sigma_l, args.sigma_h, args.sigma_iou, args.t_min)
  print('\t[-] Format Tracks')
  tracks = build_array2(tracks, fmt=args.fmt)
  return tracks

def detection(image,thresh,frame_num):
  '''runs a darknet detection.  Returns an array of form [(object, probability, (b.x, b.y, b.w, b.h)), (object2....]
  image should be the path (relative to root) showing the input image zoomed in on a track's bounding boxes'''
  print('\t[-] Calling Detection')
  detections = detect_img(image,thresh)
  dt2 = []
  print('[-] Detection Formatting Sequence')
  for dt in range(len(detections)):
	print('\t\t[-] Formatting Detection '+str(dt)+'/'+str(len(detections)))
        #take out info in each detection, reformat for tracker
        temp = []
        #frame, id, b.x,b.y,b.w,b.h,prob.
	#tried extend but python threw a fit
	'''temp.append(frame_num)
	temp.append(detections[dt][0])
	temp.append(detections[dt][2][0])
	temp.append(detections[dt][2][1])
	temp.append(detections[dt][2][2])
	temp.append(detections[dt][2][3])
	temp.append(detections[1])
        temp = np.asarray(temp)'''
	temp = np.array([frame_num,detections[dt][0],detections[dt][2][0],detections[dt][2][1],detections[dt][2][2],detections[dt][2][3],detections[dt][1]])
	dt2 = np.concatenate((dt2, temp),axis = 0)
  dt2 = dt2.reshape((len(detections),7))
  return dt2

def ev_thresh(len_ious,len_tracks):
  global FAR
  if(len_tracks == 0):
    FAR = FAR - .05
  elif(len_ious < len_tracks):
    FAR = FAR + .05
  else:
    pass
  return

def gui_feed():
  external_call(frames,detects)

def main():
  args = tracker_args()
  frame_count = 0
  vid_loc = './data/video.mov'
  print('Track-before-Detect with Neural Networks')
  print('[1] Creating Frame Data')
  input_data(vid_loc)
  #create bootstrap detection
  print('[2] Creating Bootstrap Detection')
  detections = detection('./data/img_frames/1'+'.png',FAR,0)
  #enter loop where tracker is fed detections, detector fed tracks, and threshold evaluated as this changes
  print('[3] Run T-b-D over frames')
  while(frame_count < 100):
        #grab a set amt. of frames from ./data/frames and move it to args.frames_path
        #delete args.frame_path first
	print('[*] Stage Frame Cluster')
        for root, dirs, files in os.walk(args.frames_path):
          for file in files:
            os.remove(os.path.join(root, file))
        #grab next 100 frames from ./data/img_frames offset by frame_count
        for i in range(100):
          src = './data/img_frames/'+str(i+frame_count)+'.png'
          copyfile(src,args.frames_path+'/'+str(i+frame_count)+'.png')
        frame_count += 100
        #call tracks now
	print('[*] Track Frame Cluster')
	#testing here
	print(detections)
        tracks = tracker(args,detections)
        #call detection() on last image in args.frames_path 
	print('[*] Detect Frame Cluster')
        detections = detection(args.frames_path+'/'+str(frame_count-1)+'.png',FAR,frame_count-1)
        #call detect and then mesh detect coord. over track coord. and compare, avoid detect() interepret time.
        #array of detection bounding boxes
	print('[*] Evaluate T-b-D Performance')
        dt_boxes = []
        for dt in range(len(detections)):
          temp = []
          temp.append(detections[dt][2])
	  temp.append(detections[dt][3])
	  temp.append(detections[dt][4])
	  temp.append(detections[dt][5])
	  dt_boxes.append(temp)
        ious = []
        if(len(tracks) == 0):
          print('There are no tracks')
        else:
          for track in range(len(tracks)):
            track_cmp = []
	    #track_cmp.append(tracks[track][2])
	    print tracks[track]
            track_cmp.append(tracks[track]['x'])
  	    track_cmp.append(tracks[track]['y'])
	    track_cmp.append(tracks[track]['w'])
	    track_cmp.append(tracks[track]['h'])
	  for dt in range(len(dt_boxes)):
            #compare current track against all boxes
            tx1,ty1,tx2,ty2 = track_cmp[0],track_cmp[1],track_cmp[0]+track_cmp[2],track_cmp[1]+track_cmp[3]
            bbox1 = [tx1,ty1,tx2,ty2]
            bbox1 = np.asarray(bbox1)
            dx1,dy1,dx2,dy2 = float(dt_boxes[dt][0]),float(dt_boxes[dt][1]),float(dt_boxes[dt][0])+float(dt_boxes[dt][2]),float(dt_boxes[dt][1])+float(dt_boxes[dt][3])
            bbox2 = [dx1,dy1,dx2,dy2]
            bbox2 = np.asarray(bbox2)
            intovunion = iou(bbox1,bbox2)
            if(intovunion > args.sigma_l):
              ious.append(intovunion)
            else:
              pass
        #call ev_thresh() to see if FAR shoud be updated
	print('[*] Update False Alarm Rate Threshold')
        ev_thresh(len(ious),len(tracks))
  print('Track-before-Detect Complete!')
        
if __name__ == '__main__':
	main()
