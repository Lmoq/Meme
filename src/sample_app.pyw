import time, os
import random
import tkinter as tk
from pynput.keyboard import Listener
from pathlib import Path
from modules import MemeWin
from queue import Queue
from threading import Thread


class Meme(MemeWin):


    def __init__(self,*args,**kwargs):
        """ 
            Randomly play green scren meme videos

            This window uses black as sacrifical color.
            Videos should be in a solid black background
            for green screen effect to work.

            hotkeys = {
                (".","1") : self.toggle_timer, = start&stop spdrun timer\n
                (".","2") : self.show_timer,   = hide and reveal spdrun timer\n
                (".","0") : self.exit_,        = terminate app
                }\n

            Seting hidden to True will hide the window all the time until it plays video.
        """
        super().__init__(*args,**kwargs)
        self.running = True
        self.timer_running = False
        self.display_time = True
        
        self.start_time = 0
        self.meme_start_time = 0
        self.timer_label = None
        
        # data
        self.w_collection = []
        self.vid_dict = {}
        self.key_pressed_time = time.time()
        self.key_pressed_time2 = time.time()
        self.key_pressed = []
        self.key_pressed2 = []

        self.media = Path(__file__).resolve().parent.parent / 'media'
        
        self.meme_t = random.randint(5,6) # <--set your own time trigger for playing memes

        # dream speedrun audio
        self.speedm_path = str(self.media / 'spdrunmusic.mp3')
        self.spdrun_sound =  self.mixer.Sound(self.speedm_path)
        self.place_timelabel()
        
        # get paths and files
        self.load_dict()
        self.load_collections()

        self.meme_start()
    

    def load_dict(self):
        # setup paths and label offset here
        # self.vid_dic = {vid_path, audio_path, labeloffx, labeloffy}
        get_m = self.get_m
        self.vid_dict = {
            'cena' :       (get_m('bing.mp4'),        get_m('bing.wav'),        0.4675, 0.533),
            'franku' :     (get_m('franku.mp4'),      get_m('franku.wav'),      0.80, 0.80),
            'shocked' :    (get_m('shocked.mp4'),     get_m('shocked.wav'),     0.50, 0.54),
            'cont' :       (get_m('continued.mp4'),   get_m('continued.wav'),   0.50, 0.50),
            'vergil' :     (get_m('vergil.mp4'),      get_m('vergil.mp3'),      0.50, 0.50),
            'prettygood' : (get_m('prettygood.mp4'),  get_m('prettygood.mp3'),  0.50, 0.50),
            'eyebrow' :    (get_m('eyebrow.mp4'),     get_m('eyebrow.mp3'),     0.80, 0.50)
            }


    def get_m(self,filename):
        return str(self.media / filename)


    def run_meme_timer(self):
        # timer for playing meme videos
        if not self.running:
            return
        
        time_ = time.time() - self.meme_start_time

        if time_ > self.meme_t:
            random_meme = random.choice(list(self.vid_dict.keys()))
            inc = random.randint(30, 2400) # change time increment if desired
            self.meme_t = self.play_meme(random_meme, self.meme_t, inc )
            pass
        
        self.root.after(20,self.run_meme_timer)


    def play_meme(self, keyname:str, time_var : int, inc_time:int) -> int:
        """ Plays meme,also returns incremented time trigger value, 
            -> time_var += inc_time"""
        # keep condition from executing more than once in instant
        # by incrementing time trigger
        if not self.playing_video:
            # get keyname
            value = self.vid_dict.get(keyname)
            if value is None:
                print('Keyname not in dict')
                return
            vid, audio, offx, offy = value
            self.play_video(vid, audio, offx, offy)
            # increment time trigger
            time_var += inc_time
            time_var = random.randint(time_var, time_var+200) # 200

            return time_var
        
    
    def run_timer(self):
        # speedrun timer
        if not self.timer_running:
            self.spdrun_sound.stop()
            return

        float = time.time() - self.start_time
        time_str = self.format_time(float)

        if self.display_time:
            self.timer_label['text'] = time_str

        # loop music
        if not self.mixer.get_busy():
            self.spdrun_sound.play()

        self.root.after(20,self.run_timer)


    def format_time(self,time:float):
        # format float to str format
        hours = int(time / 3600) % 24
        mins = int(time / 60) % 60
        sec = time % 60
        
        return f'{hours:02d}:{mins:02d}:{sec:05.2f}'
    

    def timer_start(self):
        # starts speedrun timer with dream speedrun music
        self.start_time = time.time()
        self.run_timer()
        self.root.deiconify()

    
    def meme_start(self):
        # start meme timer
        self.meme_start_time = time.time()
        self.run_meme_timer()


    def toggle_timer(self):
        # start and stop speedrun timer
        self.timer_running = not self.timer_running
        if self.timer_running:
            self.timer_start()
        
    
    def show_timer(self):
        # reveal and hide timer
        self.display_time = not self.display_time
        if not self.display_time:
            self.timer_label['text']=" "


    def place_timelabel(self):
        # speedrun timer
        self.timer_label = tk.Label(
            text='',
            font=(None,28),
            fg=self.text_color,
            bg=self.sac_color)

        self.timer_label.place(x=1150,y=30)
    

    def load_collections(self):
        # collection of not safe words
        collection_path = Path(__file__).resolve().parent.parent / 'data/collection.txt'
        with open(collection_path,'r') as f:
            self.w_collection = f.read().split('\n')
        

    def add_hotkey(self):
        # listener for hotkeys and typed words
        # dont forget to cleanse eyes after looking at this ugly logic
        hotkeys = {
            (".","1") : self.toggle_timer,
            (".","2") : self.show_timer,
            (".","0") : self.exit_,
        }

        def check():
            # check pressed combination
            for hotkey, callback in hotkeys.items():
                if all(k in hotkey for k in self.key_pressed):
                    callback()
                    break
        
        def catch():
            # catch not safe typed words
            word_list = ''.join(self.key_pressed2).split()
            fullword = ' '.join(word_list)

            print(fullword)

            for i in word_list:
                if i.lower() in self.w_collection:
                    self.key_pressed2.clear()
                    self.play_meme('vergil',0,0)
                    return
            
            if fullword and fullword in self.w_collection:
                self.key_pressed2.clear()
                self.play_meme('vergil',0,0)
            

        def listen_(key, interval, callback, hotkeys = True, ):
            if hotkeys:
                time_var = self.key_pressed_time
                keylist = self.key_pressed
            else:
                time_var = self.key_pressed_time2
                keylist = self.key_pressed2
            
            interv_ = time.time() - time_var
            time_var = time.time()

            if interv_ < interval:
                keylist.append(key.strip("'") if 'Key' not in key else ' ')
                callback()
            else:
                time_var = time.time()
                keylist.clear()
                keylist.append(key.strip("'") if 'Key' not in key else '')
                return time_var
            return time_var

        def key_listener(key):
            key = str(key)
            self.key_pressed_time = listen_(key, 0.10, check) #hotkeys
            self.key_pressed_time2 = listen_(key, 1.5, catch, False) #typed words
            
        with Listener(on_press=key_listener) as listener:
            listener.join()

    
    def run(self):
        Thread(target=self.add_hotkey,daemon=True).start()
        self.root.mainloop()


    def exit_(self):
        self.running = False
        self.mixer.quit()
        self.root.destroy()
        exit(0)




if __name__=='__main__':
    app = Meme(hidden=True)
    app.run()

    pass