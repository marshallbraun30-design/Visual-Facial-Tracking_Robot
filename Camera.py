from time import time

import cv2 as cv
import serial 
import time

last_send = 0
send_interval = 0.033

message = serial.Serial('COM3', 9600)


def main():
    
    video = cv.VideoCapture(0)
    if not video.isOpened():
        raise SystemExit

    haar = open_ml()

    frame_x, frame_y = video_info(video)

    while True:
        success, pics = video.read()
        if not success:
            break

        faces = detect_faces(pics, haar)

        for (x, y, w, h) in faces: #made function forthis
            box_x, box_y = find_faces(pics, x, y, w, h)

            errorx, errory = get_error(box_x, box_y, frame_x, frame_y)
      
            send_error(errorx, errory)
    

        cv.imshow("cam video", pics)

        if cv.waitKey(1) & 0xFF == ord("q"):
            break
    video.release()
    cv.destroyAllWindows()
    message.close()

def find_faces(pics, x, y, w, h):
            cv.rectangle(pics, (x, y), (x + w, y + h), (0, 255, 0), 2)
            box_x = x + w // 2
            box_y = y + h // 2
            return box_x , box_y

def get_error(box_x,box_y, frame_x, frame_y):
    errorx = box_x - frame_x
    errory = box_y - frame_y
    return errorx, errory

def send_error(errorx, errory):
    time_current = time.monotonic()
    check = time_current - last_send
    if check > send_interval:
        last_send = time_current
        message.write(str("x{}y{}\n".format(errorx, errory)).encode())

def detect_faces(pics,haar):
        gray_video = cv.cvtColor(pics, cv.COLOR_BGR2GRAY)
        faces = haar.detectMultiScale(
            gray_video,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces

def open_ml():
    haar = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if haar.empty():
        print("Face cascade failed to load")
        raise SystemExit
    return haar

def video_info(video):

    og_width = video.get(cv.CAP_PROP_FRAME_WIDTH)
    og_height = video.get(cv.CAP_PROP_FRAME_HEIGHT)
    frame_x = og_width // 2
    frame_y = og_height // 2
    print("{},{}".format(og_width, og_height))
    return frame_x, frame_y

if __name__ == "__main__":
     main()