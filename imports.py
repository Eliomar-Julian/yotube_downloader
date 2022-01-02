from os import system
import platform
try:
    from tkinter import *
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    from PIL import Image, ImageTk
    from tkinter import filedialog
    from ttkbootstrap.widgets import Meter
    from pytube import YouTube
    from threading import Thread
    from urllib import request
    from os import path
except ImportError:
    if platform.system == "linux":
        system("pip3 install pillow")
        system("pip3 install pytube")
        system("pip3 install ttkbootstrap")
        system("pip3 install urllib")
    else:
        system("pip install pillow")
        system("pip install pytube")
        system("pip install ttkbootstrap")
        system("pip install urllib")
finally:
    from tkinter import *
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    from PIL import Image, ImageTk
    from tkinter import filedialog
    from ttkbootstrap.widgets import Meter
    from pytube import YouTube
    from threading import Thread
    from urllib import request
    from os import path
