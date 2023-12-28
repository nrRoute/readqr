import cv2
import tkinter as tk
import PIL.Image
import PIL.ImageTk


class ReadQR(tk.Frame):
    def __init__(self, master=None):
        self.delay = 30
        self.qr_code_data = ""
        self.camera_id = -1
        self.qr_code_detector = cv2.QRCodeDetector()

        super().__init__(master)
        try:
            self.create_root_window()
        except BaseException as be:
            print(be)

    def create_root_window(self):
        self.master.title("Read QR Code")
        self.master.geometry("800x600")
        self.master.resizable(False, False)

        # LabelFrame for QR
        self.frame_qr = tk.LabelFrame(
            self.master, text='QR CODE', width="375", height="375", bg="#e3fab4")
        self.frame_qr.place(x=25, y=185)

        # Canvas
        self.canvas_qr = tk.Canvas(
            self.frame_qr, width="360", height="360")
        self.canvas_qr.grid(column=0, row=0, padx=5, pady=5)

        self.qr_label = tk.Label(self.frame_qr, width=25, font=("Segoe UI", 15))
        self.qr_label.place(x=45, y=325)

        self.set_camera()
        self.camera_update()

    def set_camera(self):
        self.vcap = cv2.VideoCapture(self.camera_id)

    def switch_camera(self):
        if self.camera_id == -1:
            self.camera_id = 0
        else:
            self.camera_id = -1
        self.set_camera()

    def camera_update(self):
        _, frame = self.vcap.read()
        retval, decoded_info, points, _ = self.qr_code_detector.detectAndDecodeMulti(frame)
        if retval:
            cv2.polylines(frame, points.astype(int), True, (0, 255, 0), 5)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = PIL.Image.fromarray(frame)
        pil_image = PIL.ImageOps.pad(pil_image, (360, 360))
        self.photo = PIL.ImageTk.PhotoImage(image=pil_image)

        if len(decoded_info) > 0:
            self.qr_label['text'] = decoded_info[0]
            self.qr_code_data = decoded_info[0]
            self.qr_label.config(text=decoded_info)
        else:
            self.qr_label['text'] = ''

        self.canvas_qr.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.master.after(self.delay, self.camera_update)


if __name__ == "__main__":
    root = tk.Tk()
    readqr = ReadQR(master=root)
    try:
        readqr.mainloop()
    except:
        root.destroy()
