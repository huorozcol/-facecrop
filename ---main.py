import tkinter as tk
from PIL import Image, ImageTk
from faceDetect import *

class VideoStream:
    def __init__(self, rtsp_url):
        self.rtsp_url = rtsp_url
        self.vid = cv2.VideoCapture(self.rtsp_url)

    def get_frame(self):
        ret, frame = self.vid.read()
        if ret:
            # Convertir el frame de BGR a RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame
        return None

    def release(self):
        self.vid.release()

class App:
    def __init__(self, root, rtsp_url):
        self.root = root
        self.root.title("Reconocimiento facial")
        #self.video_stream = VideoStream(rtsp_url)
        self.label_vid_str = tk.Label(root)
        self.label_vid_str.place(x=10,y=250)
        self.bt_conect_camera = tk.Button(root, text="Conectar con la Cámara IP")
        self.bt_conect_camera.place(x=670, y=46)
        self.bt_conect_camera.bind("<Button-1>", lambda _: self.update())
        self.lb_connection_cam = tk.Label(root, text="")
        self.lb_connection_cam.place(x=10, y=80)
        rtsp_url = txb_ip_cam.get()
        self.video_stream = VideoStream(rtsp_url)
        #self.update()

    def update(self): #update the label at tk, containing the frame

        frame = self.video_stream.get_frame() # get next frame
        if frame is not None:
            # Convertir el frame a imagen de PIL
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.label_vid_str.config(image=self.photo)
            self.label_vid_str.image = self.photo
            faces(frame) # identify the faces in frame,
        self.root.after(10, self.update)

    def on_closing(self):
        self.video_stream.release()
        self.root.destroy()

if __name__ == "__main__":
    #rtsp_url = "./v1.mp4"  # Reemplaza con tu URL RTSP
    #rtsp_url = "http://192.168.1.172"
    root = tk.Tk()
    root.geometry("1600x900")

    fr = tk.Frame(root, width=900, height=200, borderwidth=2, relief="groove")
    fr.place(x=10, y=10)

    title_fr = tk.Label(fr,text="Por favor inserte la información para conectar con la cámara")
    title_fr.place(x=10, y=10)

    txb_ip_cam = tk.Entry(fr, width=80)
    #txb_ip_cam.insert(0, "rtsp://admin:admin@192.168.1.201:1935/camera")
    #txb_ip_cam.insert(0, "./v5.mp4")
    txb_ip_cam.place(x=10, y=50)

    app = App(root, txb_ip_cam.get())
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
