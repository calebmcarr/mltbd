FAR = 0.05

def input_data(data):
  if(data == file):
    open_file()
    return file_handle
  elif(data == stream):
    open_buffer()
    return buffer_handle


def track(detections,frames):
  tracks = iou_track(detections,frames)
  return tracks

def detection(frames):
  detects = darknet(frames)
  detects = detects_csv()
  return detects

def ev_thresh(tracks,detects):
  tr = len(frames)
  det = len(detects)
  if(tr>det):
    FAR = FAR + .05

def gui_feed():
  external_call(frames,detects)

def main():
