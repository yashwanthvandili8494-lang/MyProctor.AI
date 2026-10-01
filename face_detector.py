import cv2
import numpy as np

def get_face_detector(modelFile=None,
                      configFile=None,
                      quantized=False):
    import os
    caffe_file = modelFile or "models/res10_300x300_ssd_iter_140000.caffemodel"
    if quantized or not os.path.exists(caffe_file):
        if modelFile == None:
            modelFile = "models/opencv_face_detector_uint8.pb"
        if configFile == None:
            configFile = "models/opencv_face_detector.pbtxt"
        try:
            model = cv2.dnn.readNetFromTensorflow(modelFile, configFile)
        except Exception:
            # Fallback to Haar Cascade if file issue
            model = None
    else:
        if configFile == None:
            configFile = "models/deploy.prototxt"
        model = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    return model

def find_faces(img, model):
    if model is None:
        try:
            cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
            rects = cascade.detectMultiScale(gray, 1.3, 5)
            return [[x, y, x + w, y + h] for (x, y, w, h) in rects]
        except Exception:
            return []
    h, w = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0,
	(300, 300), (104.0, 177.0, 123.0))
    model.setInput(blob)
    res = model.forward()
    faces = []
    for i in range(res.shape[2]):
        confidence = res[0, 0, i, 2]
        if confidence > 0.5:
            box = res[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x1, y1) = box.astype("int")
            faces.append([x, y, x1, y1])
    return faces