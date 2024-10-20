import tkinter as tk
from tkinter import Label, Entry, Frame
import cv2
from PIL import Image, ImageTk


camera_source = None

class Camera:
    def __init__(self, masterWind):
        self.master =  masterWind
        self.master.title("Detección  de rostros.")
        self.camera = camera_source
        self.title_fr = Label(text="Por favor inserte la información para conectar con la cámara")
        self.title_fr.place(x=10,y=10)
        self.fr = Frame(self.master,width=900, height=200, borderwidth=2, relief="groove")
        self.fr.place(x=10, y=30)
        self.label_ip_cam = Label(self.fr, text="Ingrese la  IP de la cámara")
        self.label_ip_cam.place(x=10, y=10)
        self.txb_ip_cam = Entry(self.fr, width=80)
        self.txb_ip_cam.insert(0,"rtsp://admin:admin@192.168.1.201:1935/camera")
        self.txb_ip_cam.place(x=10, y=50)
        self.bt_conect_camera = tk.Button(self.fr, text="Conectar con la Cámara IP")
        self.bt_conect_camera.place(x=670, y=46)
        self.bt_conect_camera.bind("<Button-1>", lambda _: self.get_ip_camera())
        self.lb_connection_cam = Label(self.fr, text="")
        self.lb_connection_cam.place(x=10, y=80)
        self.fr_vid = Frame(self.master, width=905, height=455, borderwidth=2, relief="groove")
        self.fr_vid.place(x=10, y=250)
        self.lb_frame_video = Label(self.fr_vid, text="Video de la Cámara")
        self.lb_frame_video.place(x=0, y=0)

    def get_ip_camera(self):

        ip_camera = self.txb_ip_cam.get()
        if len(ip_camera) > 0:

            self.video_source = ip_camera
            self.cap = cv2.VideoCapture(self.video_source)
            if not self.cap.isOpened():
                print("Error opening video")
            #print(ret)
            if self.cap.isOpened():
                self.ret, self.frame = self.cap.read()
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.frame = cv2.resize(self.frame, (900, 450))
                # Convertir a imagen de PIL
                img = Image.fromarray(self.frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.lb_frame_video.imgtk = imgtk
                self.lb_frame_video.configure(image=imgtk)
                self.lb_frame_video.after(10, self.get_ip_camera)
                #cv2.waitKey(1)
                self.lb_connection_cam.config(text=f"Conectado a la cámara {ip_camera}", fg='green')
                if self.ret:
                    print('ok')
                    #self.vid = cv2.VideoCapture(self.video_source)
                    #ret, self.frame = self.vid.read()
                    #print('[INFO] trying to reach ip camera...')
                    # Convertir el frame a formato RGB

            else:
                self.lb_connection_cam.config(text=f"Algo salió mal conectando la cámara {ip_camera}", fg='red')
                self.lb_frame_video.after(100, self.get_ip_camera)

        else:
            print("[ERROR] The ip camera value, can't be empty")


if __name__ == '__main__':
    root = tk.Tk()
    Camera(root)
    root.geometry("1600x900")
    root.mainloop()
