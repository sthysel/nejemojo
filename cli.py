#!/usr/bin/python


import serial
from PIL import Image
from tkinter import filedialog
import tkinter as tk

# variables
version = "0.0.1"
usb_port = "/dev/ttyUSB0"
baund_rate = 57600

ser = serial.Serial(
    port=usb_port,
    baudrate=baund_rate,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

name_image = "img/apple.jpg"
im = Image.open(name_image)


def about():
    about.title("pyNeje " + version)
    label_about = Label(about, image="donation_img")
    about.mainloop()


def open_image():
    im = filedialog.askopenfile(parent=root, mode='rb', title='Choose a file')
    input = open('im', 'r')
    label_image.config = Label(image_tab, image=input)
    # print(im)
    # im = Image.open(name_image)


def convert_image():
    im = Image.open(name_image).convert("1")
    # im = Image.open(name_image)
    im = im.resize((512, 512))
    print((im.format, im.size, im.mode))


def engrave_memory():
    # set 60 ms
    ser.write("3c".decode("hex"))
    # engrave
    label_info.config(text="Engraving Memory...")
    ser.write("f1".decode("hex"))
    label_info.config(text="Engraving Memory done")


def engrave_pause():
    ser.write("f2".decode("hex"))
    label_info.config(text="Pause")


def engrave_preview():
    ser.write("f4".decode("hex"))
    label_info.config(text="Engraving preview")


def reset():
    ser.write("f9".decode("hex"))
    label_info.config(text="Reset")


def move_home():
    label_info.config(text="Move home")
    ser.write("f3".decode("hex"))


def move_center():
    label_info.config(text="Move Center")
    ser.write("fb".decode("hex"))


def send_image():
    a = 0
    while a < 8:
        a = a + 1
        print(("Erase EEPROM 8/" + str(a)))
        # erase eeprom
        ser.write("fe".decode("hex"))
    # upload to eeprom
    label_info.config(text="Uploading to EEPROM. please wait...")
    ser.write(im.getdata())
    label_info.config(text="Uploading to EEPROM. Done")


convert_image()



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        notebook = tk.Notebook(root)
        image_tab = tk.Frame(notebook)
        jog_tab = tk.Frame(notebook)
        prefs_tab = tk.Frame(notebook)
        notebook.add(image_tab, text='Image')
        notebook.add(jog_tab, text='jog')
        notebook.add(prefs_tab, text='Prefs')
        notebook.pack()

        # frames
        image_frame_button = tk.Frame(image_tab)

        # entrys
        entry_usb_port = tk.Entry(prefs_tab, textvariable=usb_port)

        # Sliders
        speed_slider = tk.Scale(prefs_tab, from_=0, to=255, orient=tk.HORIZONTAL)
        burn_time_slider = tk.Scale(prefs_tab, from_=0, to=255, orient=tk.HORIZONTAL)

        # labels
        # image preview
        tk_image = tk.PhotoImage(im)
        label_image = tk.Label(image_tab, image=tk_image)

        # info
        label_info = tk.Label(root, text=(im.format, im.size, im.mode))
        # entry_label
        serial_label = tk.Label(prefs_tab, text="serial ")
        # speed_label
        speed_label = tk.Label(prefs_tab, text="speed jog")
        # speed_label
        burn_time_label = tk.Label(prefs_tab, text="burn time")

        # buttons
        # image_frame_button
        engrave_memory_bt = tk.Button(image_frame_button, text="engrave", command=engrave_memory)
        engrave_pause_bt = tk.Button(image_frame_button, text="pause", command=engrave_pause)
        engrave_preview_bt = tk.Button(image_frame_button, text="preview", command=engrave_preview)
        send_image_bt = tk.Button(image_frame_button, text="upload", command=send_image)
        open_image_bt = tk.Button(image_frame_button, text='open', command=open_image)

        # jog_tab
        reset_bt = tk.Button(jog_tab, text="reset", command=reset)
        home_bt = tk.Button(jog_tab, text="home", command=move_home)
        center_bt = tk.Button(jog_tab, text="center", command=move_center)

        # grid root
        label_info.pack()
        # grid frame
        image_frame_button.grid(row=1, column=0)

        # grid image_tab
        label_image.grid(row=0, column=0)

        open_image_bt.grid(row=0, column=0)
        send_image_bt.grid(row=0, column=1)
        engrave_preview_bt.grid(row=0, column=2)
        engrave_memory_bt.grid(row=0, column=3)
        engrave_pause_bt.grid(row=0, column=4)

        # grid jog_tab
        reset_bt.pack()
        home_bt.pack()
        center_bt.pack()

        # grid prefs_tab
        serial_label.grid(row=0, column=0)
        entry_usb_port.grid(row=0, column=1)
        speed_label.grid(row=1, column=0)
        speed_slider.grid(row=1, column=1)
        burn_time_label.grid(row=2, column=0)
        burn_time_slider.grid(row=2, column=1)

        # menu
        menu = tk.Menu(root)
        root.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open...", command=open_image)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=root.quit)

        helpmenu = tk.Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=about)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
