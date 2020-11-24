import  os, time,cv2
face_cascade = cv2.CascadeClassifier("static/haarcascade_frontalface_alt2.xml")
ds_factor = 0.6
class VideoCamera(object):
    def __init__(self, video_name):
        # self.video = cv2.VideoCapture(0)
        self.video = cv2.VideoCapture(video_name)

    def __del__(self):
        self.video.release()

    def reload(self):
        self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def get_frame_and_face_detector(self):
        success, image = self.video.read()
        if not success:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, image = self.video.read()
        image = cv2.resize(image, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in face_rects:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    def get_frame(self):
        success, image = self.video.read()
        if not success:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
