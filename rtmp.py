import queue
import threading
import cv2
import subprocess as sp
import datetime


class Live(object):
    def __init__(self):
        self.frame_queue = queue.Queue()
        self.command = ""
        # 自行设置
        self.rtmpUrl = "rtmp://192.168.164.128/myapp/local"
        # http://192.168.164.128/live?app=myapp&stream=local
        # http://192.168.164.128:80/live?port=1935&app=myapp&stream=local
        # http://192.168.164.128:80/hls/local.m3u8
        # self.vedio_path = 0
        self.vedio_path = "test.mp4"
        self.flag = False

    def setCamera(self):
        cap = cv2.VideoCapture(self.vedio_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.command = ['ffmpeg',
                        '-y',
                        '-f', 'rawvideo',
                        '-vcodec', 'rawvideo',
                        '-pix_fmt', 'bgr24',
                        '-s', "{}x{}".format(width, height),
                        '-r', str(fps),
                        '-i', '-',
                        '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p',
                        '-preset', 'ultrafast',
                        '-f', 'flv',
                        self.rtmpUrl]

    def read_frame(self):
        print("开启推流")
        cap = cv2.VideoCapture(self.vedio_path)
        # Get video information
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # print(width, height)
        # ffmpeg command
        self.command = ['ffmpeg',
                        '-y',
                        '-f', 'rawvideo',
                        '-vcodec', 'rawvideo',
                        '-pix_fmt', 'bgr24',
                        '-s', "{}x{}".format(width, height),
                        '-r', str(fps),
                        '-i', '-',
                        '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p',
                        '-preset', 'ultrafast',
                        '-f', 'flv',
                        self.rtmpUrl]
        # read webcamera
        count = 0
        while True:
            if cap.isOpened():
                ret, frame = cap.read()
                # cv.imshow(frame)
                if not ret:
                    print('Opening camera is failed')
                    count += 1
                    cap.release()
                    cap = cv2.VideoCapture(self.vedio_path)
                # put frame into queue
                self.frame_queue.put(frame)
            else:
                print('推流已结束')
                cap.release()
                cap = cv2.VideoCapture(self.vedio_path)

    def push_frame(self):
        # 防止多线程时 command 未被设置
        while True:
            if len(self.command) > 0:
                # 管道配置
                p = sp.Popen(self.command, stdin=sp.PIPE)
                break
        font = cv2.FONT_HERSHEY_SIMPLEX
        while True:
            if self.frame_queue.empty() != True:
                frame = self.frame_queue.get()
                # process frame
                # 你处理图片的代码
                # write to pipe
                # frame = cv2.putText(frame, str(datetime.datetime.now()), (10, 50), font, 1.2, (255, 255, 255), 2)
                p.stdin.write(frame.tostring())
                if self.flag:
                    break

    def run(self):
        threads = [
            threading.Thread(target=Live.read_frame, args=(self,)),
            threading.Thread(target=Live.push_frame, args=(self,))
        ]
        [thread.setDaemon(True) for thread in threads]
        [thread.start() for thread in threads]
        while True:
            if self.flag:
                break


live = Live()
# while True:
live.run()
