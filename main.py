#! /usr/bin/env python
# -*- coding: utf-8 -*-

#from __future__ import division, print_function, absolute_import
import os
import datetime
from timeit import time
import warnings
import cv2
import numpy as np
import argparse
from PIL import Image
from yolo import YOLO
from deep_sort import preprocessing
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
from deep_sort.detection import Detection as ddet
from collections import deque
from keras import backend
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import datetime
import pycurl, json, re

backend.clear_session()
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input",help="path to input video", default = "./6.mp4")
ap.add_argument("-c", "--class",help="name of class", default = "person")
args = vars(ap.parse_args())

pts = [deque(maxlen=30) for _ in range(9999)]
warnings.filterwarnings('ignore')

# initialize a list of colors to represent each possible class label
np.random.seed(100)
COLORS = np.random.randint(0, 255, size=(200, 3),
	dtype="uint8")
dirlist=[]
tokens=[]
print("DIRlist created, token list created")
print('inside token_count')
cred = credentials.Certificate("./ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)
store = firestore.client()
doc_ref = store.collection(u'testy')

try:
    docs = doc_ref.stream()
    for doc in docs:
        print(u'Doc Data:{}'.format(doc.to_dict()))
        if doc.to_dict() not in tokens:
            tokens.append(doc.to_dict())
            print('*********tokens:{}*********'.format(tokens))

except google.cloud.exceptions.NotFound:
    print(u'Missing data')
tokensnew='{}'.format(tokens)
print(tokensnew)

x=re.sub("token", "", tokensnew)
x=re.sub("]", "", x)
x=re.sub('\[', "", x)
x=re.sub("'", "", x)
x=re.sub("{", "", x)
x=re.sub("}", "", x)
x=re.sub(",", "", x)
x=re.split(" ",x)
x = list(filter(None, x))
x=[tokeni for tokeni in x if tokeni!=':']
print(x)


def notify(class_name,trackid):
    
    now=datetime.datetime.now()
    time=now.strftime("%H:%M")
    print(time)
    doc_ref = store.collection(u'objects')
    doc_ref.add({u'name': u'testframe{clas},{id}.jpg'.format(clas=class_name,id=trackid), u'added': time})
    for tokeni in x:
        c = pycurl.Curl()
        c.setopt(pycurl.URL, 'https://fcm.googleapis.com/fcm/send')
        c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json','Authorization: key=AAAAP1gySWk:APA91bEJogPOykWMPEc4hoFer2QXo0uOijVODd2AHrb0qHsIWFRLAFGEDw-YZfEVi0oC9G_zh2j2dZ4RIvMyJi-cf3kvo2gZMRHN8PFvYDMwzAFVk4qlLmo5NyQNXhZNvzlqP7w6pG20'])
        print('======================{}'.format(tokeni))
        data = json.dumps({"notification":{"title":"GTFO","body":"frame{clas},{id}.jpg" .format(clas=class_name,id=trackid),"icon":"/itwonders-web-logo.png",}, "to":"{}".format(tokeni)})
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, data)
        c.setopt(pycurl.VERBOSE, 1)
        c.perform()
        print(c.getinfo(pycurl.RESPONSE_CODE))
        certinfo = c.getinfo(pycurl.INFO_CERTINFO)
        print(certinfo)
        c.close()
    return

def main(yolo):

    #start = time.time()
    #Definition of the parameters
    max_cosine_distance = 0.5#0.9 余弦距离的控制阈值
    nn_budget = None
    nms_max_overlap = 0.3 #非极大抑制的阈值

    counter = []
    #deep_sort
    model_filename = 'model_data/market1501.pb'
    encoder = gdet.create_box_encoder(model_filename,batch_size=1)

    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    tracker = Tracker(metric)

    writeVideo_flag = True
    #video_path = "../../yolo_dataset/1.mp4"
    video_capture = cv2.VideoCapture(args["input"])

    if writeVideo_flag:
    # Define the codec and create VideoWriter object
        w = int(video_capture.get(3))
        h = int(video_capture.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter('./output/'+args["input"][43:57]+ "_" + args["class"] + '_output.avi', fourcc, 15, (w, h))
        list_file = open('detection.txt', 'w')
        frame_index = -1

    fps = 0.0

    while True:

        ret, frame = video_capture.read()  # frame shape 640*480*3
        if ret != True:
            break
        t1 = time.time()

       # image = Image.fromarray(frame)
        image = Image.fromarray(frame[...,::-1]) #bgr to rgb
        boxs,class_names = yolo.detect_image(image)
        features = encoder(frame,boxs)
        # score to 1.0 here).
        detections = [Detection(bbox, 1.0, feature) for bbox, feature in zip(boxs, features)]
        # Run non-maxima suppression.
        boxes = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        indices = preprocessing.non_max_suppression(boxes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]

        # Call the tracker
        tracker.predict()
        tracker.update(detections)

        i = int(0)
        indexIDs = []
        c = []
        boxes = []
        for det in detections:
            bbox = det.to_tlbr()
            cv2.rectangle(frame,(int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,255,255), 1)
        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                
                continue
            #boxes.append([track[0], track[1], track[2], track[3]])
            indexIDs.append(int(track.track_id))
            counter.append(int(track.track_id))
            bbox = track.to_tlbr()
            color = [int(c) for c in COLORS[indexIDs[i] % len(COLORS)]]

            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(color), 1)
            cv2.putText(frame,str(track.track_id),(int(bbox[0]), int(bbox[1] -50)),2, 5e-3 * 150, (color),1)
            crop_img = frame[int(bbox[1])-20:int(bbox[3])+20,int(bbox[0])-20:int(bbox[2])+20]
            
            print('imwrite done')
            if len(class_names) > 0:
               class_name = class_names[0]
               cv2.putText(frame, str(class_names[0]),(int(bbox[0]), int(bbox[1] -20)),0, 5e-3 * 100, (color),1)
            try:
                a="frame{clas},{id}.jpg" .format(clas=class_names[0],id=int(track.track_id))
                cv2.imwrite(a , crop_img)
                if a not in dirlist:
                    dirlist.append(a)
                    print(dirlist)
                    print("calling curl function")
                    notify(class_names[0],int(track.track_id))
                
            except:
                cv2.imwrite("frame{clas},{id}.jpg" .format(clas=class_names[0],id=int(track.track_id)) , frame)
            i += 1
            #bbox_center_point(x,y)
            center = (int(((bbox[0])+(bbox[2]))/2),int(((bbox[1])+(bbox[3]))/2))
            #track_id[center]
            pts[track.track_id].append(center)
            thickness = 1
            #center point
            cv2.circle(frame,  (center), 1, color, thickness)

	    #draw motion path
            for j in range(1, len(pts[track.track_id])):
                if pts[track.track_id][j - 1] is None or pts[track.track_id][j] is None:
                   continue
                thickness = int(np.sqrt(64 / float(j + 1)) * 2)
                cv2.line(frame,(pts[track.track_id][j-1]), (pts[track.track_id][j]),(color),thickness)
                
                #cv2.putText(frame, str(class_names[j]),(int(bbox[0]), int(bbox[1] -20)),0, 5e-3 * 150, (255,255,255),2)

        count = len(set(counter))
        cv2.putText(frame, "Total Counter: "+str(count),(int(20), int(80)),2, 5e-3 * 160, (0,255,0),1)
        cv2.putText(frame, "Current Counter: "+str(i),(int(20), int(55)),2, 5e-3 * 160, (0,255,0),1)
        cv2.putText(frame, "FPS: %f"%(fps),(int(20), int(30)),2, 5e-3 * 160, (0,255,0),1)
        cv2.putText(frame, "TEST FOOTAGE",(int(20), int(110)),2, 5e-3 * 160, (0,255,0),1)
        cv2.namedWindow("YOLO3_Deep_SORT", 0);
        cv2.resizeWindow('YOLO3_Deep_SORT', 1024, 768);
        cv2.imshow('YOLO3_Deep_SORT', frame)

        if writeVideo_flag:
            #save a frame
            out.write(frame)
            frame_index = frame_index + 1
            list_file.write(str(frame_index)+' ')
            if len(boxs) != 0:
                for i in range(0,len(boxs)):
                    list_file.write(str(boxs[i][0]) + ' '+str(boxs[i][1]) + ' '+str(boxs[i][2]) + ' '+str(boxs[i][3]) + ' ')
            list_file.write('\n')
        fps  = ( fps + (1./(time.time()-t1)) ) / 2
        #print(set(counter))

        # Press Q to stop!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print(" ")
    print("[Finish]")
    end = time.time()

    if len(pts[track.track_id]) != None:
       print(args["input"][43:57]+": "+ str(count) + " " + str(class_name) +' Found')

    else:
       print("[No Found]")

    video_capture.release()

    if writeVideo_flag:
        out.release()
        list_file.close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(YOLO())
'''

'''