import cv2
import datetime

cap = cv2.VideoCapture("D:/Users/xiang/Downloads/Video/video.flv")

count = 0
font = cv2.FONT_HERSHEY_SIMPLEX
while count < 721:
    success, frame = cap.read()  # 读取视频流（successs代表读取成功，为True；frame为读取图片）
    if success:
        frame = cv2.putText(frame, str(datetime.datetime.now()), (10, 50), font, 1.2, (255, 255, 255), 2)
        cv2.imshow('rea', frame)
        cv2.waitKey(5)
        if count % 24 == 1:  # 每24帧取一次图片
            img_name = str(id) + '_' + str(count) + '.jpg'  # 对输出的图片加入每个id名字命名
            # cv2.imwrite(os.path.join(save_path, img_name), frame)
    count += 1
cap.release()
