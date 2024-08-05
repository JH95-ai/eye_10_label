#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/12
# @Author  : ThunderSOft
# @Email   : li@thundersoft.com
# @File    : landmark.py

import os
import tensorflow as tf
import numpy as np
import time
import cv2

head_pb='/home/ts-liqing/iwork/project/Face/Lamdmarks/head_detector.pb'
lm_pb='/home/ts-liqing/iwork/project/Face/Lamdmarks/landmarks.pb'


class LMEngine(object):
    def __init__(self):
        self.__head_model = None
        self.__lm_model = None
        self.input_size = 112

    def init(self, model1, model2):
        self.__head_model = model1
        self.__lm_model = model2

        with tf.Graph().as_default() as graph_head:
            with tf.gfile.FastGFile(self.__head_model, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                _ = tf.import_graph_def(graph_def, name='')

        with graph_head.as_default():
            self.input_head_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')  # "batch:1"
            self.output_head_tensor = {
                'scores': tf.get_default_graph().get_tensor_by_name('detection_scores:0'),
                'classes': tf.get_default_graph().get_tensor_by_name('detection_classes:0'),
                'boxes': tf.get_default_graph().get_tensor_by_name('detection_boxes:0'),
            }

        with tf.Graph().as_default() as graph_pose:
            with tf.gfile.FastGFile(self.__lm_model, 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                _ = tf.import_graph_def(graph_def, name='')

        with graph_pose.as_default():
            self.input = tf.get_default_graph().get_tensor_by_name('Placeholder:0')  # "batch:1"
            self.output = {
                'fully_connected': tf.get_default_graph().get_tensor_by_name(
                    'MobileNetV2/InferenceNet/fully_connected/BiasAdd:0'),
            }

        self.config = tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))
        self.sess1 = tf.Session(graph=graph_head, config=self.config)
        self.sess2 = tf.Session(graph=graph_pose, config=self.config)

    def run(self, file):
        #img = cv2.imread(file)
        img = cv2.imdecode(np.fromfile(file, dtype=np.uint8), cv2.IMREAD_COLOR)
        start = time.time()
        img_clone = np.copy(img)
        h, w, c = np.shape(img_clone)
        img = np.array(img).astype(np.float32)
        img = cv2.resize(img, (300, 300), interpolation=cv2.INTER_AREA)
        img = img[:, :, ::-1]
        img = np.expand_dims(img, axis=0)
        output_head = self.sess1.run(self.output_head_tensor,feed_dict={self.input_head_tensor:img})

        scores, classes, boxes = output_head['scores'], output_head['classes'], output_head['boxes']
        score = scores[0][0]
        classes = classes[0]
        box = boxes[0][0]
        time_head = time.time()

        x1,y1,x2,y2= self.getCropBox(img_clone,boxes,scores)
        img_crop = np.copy(img_clone[y1:y2, x1:x2, :]) #bgr
        # cv2.imwrite("./head.jpg", img_crop)
        h, w, c = np.shape(img_crop)

        img_landmarks = cv2.resize(img_crop,(self.input_size,self.input_size),interpolation=cv2.INTER_AREA)
        img_landmarks = (img_landmarks-127.5)/127.5
        img_landmarks = img_landmarks[:,:,::-1]  #rgb
        img_landmarks = np.expand_dims(img_landmarks, axis=0)
        output_landmarks = self.sess2.run(self.output, feed_dict={self.input: img_landmarks})
        # print(output_pose)
        fully_connected = output_landmarks['fully_connected']
        fully_connected = np.squeeze(fully_connected)
        landmarks_x = fully_connected[:106] * w + x1
        landmarks_y = fully_connected[106:] * h + y1
        # self.draw_landmarks(img_clone, landmarks_x, landmarks_y)
        lm_time = time.time()
        total_cost_time = (lm_time - start) * 1000
        head_cost_time = (time_head - start) * 1000
        lm_cost_time = (lm_time - time_head) * 1000
        print("inference time %d + %d = %d" % (head_cost_time, lm_cost_time, total_cost_time))
        return landmarks_x, landmarks_y
        # draw_hist(norm_landmark_x,norm_landmark_y)
        # cv2.rectangle(img_clone, (x1, y1), (x2, y2), (0, 255, 0), 10)
        # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        # isQuit = draw_landmarks(img_clone, landmarks_x, landmarks_y, time_sleep=1)
        # if isQuit == True:
        #     cv2.destroyAllWindows()
        #     break

    def draw_landmarks(self, img, landmarks_x, landmarks_y):
        isQuit = False
        for i, lx in enumerate(landmarks_x):
            # for i,(lx,ly) in enumerate(landmarks_x,landmarks_y):
            ly = landmarks_y[i]
            x, y = lx, ly
            #print("point(%.3f,%.3f)" % (x, y))
            cv2.circle(img, (int(x), int(y)), 3, (0, 255, 0), -1)
            # cv2.putText(img, str(i+1), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.imwrite("./lm.jpg", img)
        # cv2.imshow('img', img)
        # key = cv2.waitKey(time_sleep)
        # if key == ord('q'):
        #     isQuit = True
        return isQuit

    def getCropBox(self, img, boxes, scores, isEdge=True):
        # input the original img:640*480
        h, w, _ = np.shape(img)
        index = np.argmax(scores[0], axis=0)
        box = boxes[0][index]
        x1 = int(box[1] * w)
        y1 = int(box[0] * h)
        x2 = int(box[3] * w)
        y2 = int(box[2] * h)
        height = y2 - y1
        width = x2 - x1
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        center_y += center_y / 5
        # scale to 2 ratio
        min_side = min(height, width)
        if (isEdge):
            max_side = max(height, width)
            min_side = int(max_side * 0.9)
        # min_side=int(min_side*(-0.2))
        half_min_side = int(min_side / 2)
        new_x1 = center_x - half_min_side
        new_y1 = center_y - half_min_side
        new_x1 = new_x1 if new_x1 > 0 else 0
        new_y1 = new_y1 if new_y1 > 0 else 0
        new_x2 = center_x + half_min_side
        new_y2 = center_y + half_min_side
        new_x2 = new_x2 if new_x2 < w else w - 1
        new_y2 = new_y2 if new_y2 < h else h - 1
        return map(int, [new_x1, new_y1, new_x2, new_y2])

if __name__ == '__main__':
    path = "/home/ts-liqing/iwork/project/Face/Tool/Facial-Landmarks-Annotation-Tool/example/images/Angelina.jpg"
    lm_engine = LMEngine()
    lm_engine.init(head_pb, lm_pb)
    lm_engine.run(path)
