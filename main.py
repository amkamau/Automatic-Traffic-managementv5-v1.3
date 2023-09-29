import cv2
import build_model as buildmodel
import object_process as objectprocess

vid_src = ["videos/test1.mp4","videos/test2.mp4","videos/test3.mp4",0,1]

net = buildmodel.buildModel()

capture = cv2.VideoCapture(vid_src[0])

while True:    
    _ , frame = capture.read()
    if frame is None:
        break

    frameout = objectprocess.processFrame(cv2.resize(frame, (1200,800)),net)

    cv2.imshow("output", frameout)
    if cv2.waitKey(1) > -1:
        break

