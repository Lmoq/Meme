import os
import time
import tkinter as tk
import cv2 as cv
from pygame import mixer
from threading import Thread
from PIL import Image, ImageTk



class MemeWin:


    def __init__(self):
        """Tkinter window that plays video frames"""
        self.root = None
        self.playing_video = False
        # green screen videos into solid black background
        self.win_bg = 'black'
        self.text_color = 'white'
        self.sac_color = self.win_bg
        # data
        self.frame_list = []
        self.videocapture = None
        self.create_window()
        mixer.init()


    def create_window(self):
        self.root = tk.Tk()
        self.root.config(bg = self.sac_color)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")#+{self.OFFSETX}+{self.OFFSETY}")
        self.root.lift()
        self.root.wm_attributes('-fullscreen',True)
        self.root.wm_attributes('-topmost',True)
        self.root.wm_attributes('-disabled', True)
        self.root.wm_attributes('-transparentcolor',self.sac_color)

        self.root.withdraw()


    def play_video(self,vid_path, aud_path, offx=0.50, offy=0.50):
        """Setup label and display video frames\n
        offx, offy = label offset, anchored to center"""
        if self.playing_video:
            print('currently playing video')
            return
        
        if not os.path.exists(vid_path):
            print('File not found')
            return
        # Setup
        video_label = tk.Label(
            self.root,
            font=(None,20),
            bg=self.sac_color)
        video_label.place(anchor='center', relx=offx, rely=offy)
        self.videocapture = cv.VideoCapture(vid_path)

        def play_():
            self.read_play(video_label,aud_path)

        if self.root.state() == 'withdrawn':
            self.root.deiconify()
        self.playing_video = True
        # use threading to not block mainloop
        Thread(target=play_,daemon=True).start()


    def read_play(self,label,audio=None):
        """Initial read and play video frames""" 
        # del self.frame_list
        frame_list = []
        for _ in range(20):
            ret, frames = self.videocapture.read()
            if ret:
                frame = cv.cvtColor(frames,cv.COLOR_BGR2RGB)
                # feed queue with chunks of pyimages
                frame_list.append(ImageTk.PhotoImage(image=Image.fromarray(frame)))
            else:
                self.videocapture.release()

        if audio:
            sound = mixer.Sound(audio)
            sound.play()

        self.display_frames(frame_list,label)
    

    def append_frames(self,frame_list):
        """Append video frames to newframe_list by 20""" 
        def append():    
            for _ in range(20):
                ret, frames = self.videocapture.read()
                if ret:
                    frame = cv.cvtColor(frames,cv.COLOR_BGR2RGB)
                    # feed queue with chunks of pyimages
                    frame_list.append(ImageTk.PhotoImage(image=Image.fromarray(frame)))
                else:
                    self.videocapture.release()
        Thread(target=append).start()
        

    def display_frames(self,frame_list,label):
        if not frame_list:
            self.playing_video = False
            label.destroy()
            self.root.withdraw()
            self.del_list(frame_list)
            return
        
        appended = False
        frame_displayed = 0
        new_framelist = []

        for i in frame_list:
            label.config(image=i)
            frame_displayed += 1

            if frame_displayed >= 10 and not appended:
                appended = True
                # read more frames halfway through for smoother playback
                self.append_frames(new_framelist)
            # adjust sleep to match framerate
            time.sleep(0.032)
        self.del_list(frame_list)
        self.display_frames(new_framelist,label)
        
       
    def del_list(self,list_):
        # deletes framelist with another thread
        def del_(list_):
            del list_
        Thread(target=del_,args=[list_]).start()


if __name__=='__main__':
    MemeWin().main()

    pass