import cv2
import dlib
from random import random, randint
import datetime

detector = dlib.get_frontal_face_detector()
new_path ='./faces/'

def save(img,name, bbox, width=180,height=227):
    x, y, w, h = bbox
    imgCrop = img[y:h, x: w]
    imgCrop = cv2.resize(imgCrop, (width, height))#we need this line to reshape the images
    rand_num = randint(1, 1000)
    my_time = datetime.datetime.now()
    my_time = my_time.strftime("%Y-%m-%d-%H-%M-%S-%f")
    cv2.imwrite(f"{name}-{my_time}.jpg", imgCrop)

def faces(frame):
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    faces = detector(frame)
    xfit = 20
    yfit = 50
    # detect the face
    for counter,face in enumerate(faces):
        x1, y1 = abs(face.left()), abs(face.top())
        x2, y2 = abs(face.right()), abs(face.bottom())
        save(frame,new_path+str(counter),(abs(x1-xfit),abs(y1-yfit),x2+xfit,y2+yfit))
        save(frame, new_path + str(counter), (x1, y1 , x2 , y2))

    #frame = cv2.resize(frame,(800,800))
    #cv2.waitKey(0)
    #print("done saving")

