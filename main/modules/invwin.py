import time
import tkinter as tk
import cv2 as cv
from my import InvWin
from pygame import mixer
from threading import Thread
from PIL import Image, ImageTk



class MemeWin(InvWin):


    def __init__(self):
        """InvWin that reads and plays video frames by chunks"""
        super().__init__()
        self.frame_list = []
        self.videocapture = None
       

    def play_video(self,keyname):
        """Setup label and display video frames\n
        dict[keyname] = vid, audio, offx ,offy"""
        # Get value from dictionary setup label and display frames
        vid_path, audio, x, y = self.dic_img[keyname]
        # Setup label
        video_label = tk.Label(
            self.root,
            font=(None,20),
            fg='white',
            bg=self.sac_color)
        video_label.place(anchor='center', relx=x, rely=y)

        self.videocapture = cv.VideoCapture(vid_path)
        def play_():
            self.read_play(video_label,audio)
            
        # use threading to not block mainloop
        Thread(target=play_,daemon=True).start()


    def read_play(self,label,audio=None):
        """Initial read and play video frames by chunks""" 
        del self.frame_list
        self.frame_list = []

        for i in range(20):
            ret, frames = self.videocapture.read()
            if ret:
                frame = cv.cvtColor(frames,cv.COLOR_BGR2RGB)
                # feed queue with chunks of pyimages
                self.frame_list.append(ImageTk.PhotoImage(image=Image.fromarray(frame)))
            else:
                self.videocapture.release()
        
        if audio:
            sound = mixer.Sound(audio)
            sound.play()
        
        self.display_frames(self.frame_list,label)
    

    def append_frames(self,frame_list):
        """Append video frames by a hundred chunks while still displaying frames""" 
        def append():    
            for i in range(20):
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
            print('destroyed')
            label.destroy()
            del frame_list
            return
        
        appended = False
        frame_displayed = 0
        new_framelist = []

        for i in frame_list:
            label.config(image=i)
            frame_displayed += 1

            if frame_displayed >= 10 and not appended:
                appended = True
                self.append_frames(new_framelist)

            time.sleep(0.03)    
        self.free_resource(frame_list)
        self.display_frames(new_framelist,label)
        
       
    def free_resource(self,list_):
        """Deletes framelist"""
        def del_(list_):
            del list_
        Thread(target=del_,args=[list_]).start()


if __name__=='__main__':
    MemeWin().main()

    pass