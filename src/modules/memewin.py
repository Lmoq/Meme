import os
import time
import tkinter as tk
import cv2 as cv
from pygame import mixer
from threading import Thread
from PIL import Image, ImageTk



class MemeWin:


    def __init__(self,hidden=False):
        """
        This window uses black as sacrifical color.
        Videos should be in a solid black background
        for green screen effect to work.
        """
        self.hidden = hidden
        self.root = None
        self.playing_video = False
        self.win_bg = 'black'
        self.text_color = 'white'
        self.sac_color = self.win_bg
        self.frame_list = []
        self.videocapture = None
        self.create_window()
        self.mixer = mixer
        self.mixer.init()


    def create_window(self):
        # create an invisible window
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
        # Sets up label then display frames
        # offx, offy = label offset anchored to 'center'
        if self.playing_video:
            print('currently playing video')
            return
        
        if not os.path.exists(vid_path) or not os.path.exists(aud_path):
            print('Missing files')
            return
    
        video_label = tk.Label(self.root, bg=self.sac_color)
        video_label.place(anchor = 'center', relx=offx, rely=offy)
        self.videocapture = cv.VideoCapture(vid_path)

        def play_():
            self.playing_video = True
            self.read_play(video_label,aud_path)

        if self.hidden and self.root.state() == 'withdrawn':
            self.root.deiconify()
        
        # use threading to not block mainloop
        Thread(target=play_,daemon=True).start()

    
    def fill_frames(self,frame_list):
        # convert frames to pyimages
        for _ in range(20):
            ret, frames = self.videocapture.read()
            if ret:
                frame = cv.cvtColor(frames,cv.COLOR_BGR2RGB)
                frame_list.append(ImageTk.PhotoImage(image=Image.fromarray(frame)))
            else:
                self.videocapture.release()


    def read_play(self,label,audio=None):
        # Lazy load frames, this spawns another lists to read next batch
        # of frames after displaying half of the previous batch
        def play_():
            frame_list = []
            self.fill_frames(frame_list)

            if audio:
                sound = self.mixer.Sound(audio)
                sound.play()
            display_frames(frame_list,label)

        def display_frames(frame_list,label):
            if not frame_list:
                self.playing_video = False
                label.destroy()
                # delete list
                self.del_list(frame_list)
                if self.hidden:
                    self.root.withdraw()
                return
            
            appended = False
            frame_displayed = 0
            new_framelist = []

            for i in frame_list:
                label.config(image=i)
                frame_displayed += 1

                if not appended and frame_displayed >= 10 :
                    # read more frames halfway through for continuous playback
                    appended = True
                    Thread(target=self.fill_frames,args=[new_framelist]).start()
                # tweak sleep to match framerate
                time.sleep(0.032)

            self.del_list(frame_list)
            # continuously display video frames until done
            display_frames(new_framelist,label)

        play_()

        
    def del_list(self,list_):
        # delete list in other thread
        def del_(list_):
            del list_
        Thread(target=del_,args=[list_]).start()

    
    def run(self):
        self.root.mainloop()

    
    def exit_(self):
        self.mixer.quit()
        self.root.destroy()
        exit(0)


if __name__=='__main__':
    # Testing
    video = input("Enter video path : ")
    audio = input("Enter audio path : ")

    if not os.path.exists(video) or not os.path.exists(audio):
        print('Missing Files')
        exit(0)

    win = MemeWin(hidden=False)
    win.after(1000, lambda : win.play_video(video,audio))
    win.after(10000,win.exit_)
    win.run()
    pass