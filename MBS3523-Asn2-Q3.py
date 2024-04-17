from ultralytics import YOLO
import time
import cv2

model = YOLO('yolov8m-seg.pt')

#results = model.predict(source=0, show=True)#範圍貼住目標物件
#results = model.predict(source=0, show=True, conf=0.85)

cam = cv2.VideoCapture(0)#在畫面

while cam.isOpened(): #開cam指令,可用True/isOpened開
    success, frame = cam.read()
    if success :
        frame = cv2.imread("WhatsApp Image 2024-04-16 at 13.29.09_fd1118fb.jpg")
        startTime = time.perf_counter()
        results = model(frame)
        print(results)
        frame1 = results[0].plot()
        endTime = time.perf_counter()
        fps = 1/(endTime-startTime)
        cv2.putText(frame1,f'FPS:{int(fps)}',(10,20),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),2)
        cv2.imshow('Inference',frame1)

        if cv2.waitKey(1) == 27:
            break
cam.release()
cv2.destroyAllWindows()
