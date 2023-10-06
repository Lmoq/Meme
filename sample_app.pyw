import time, os
import random
import tkinter as tk
from pynput.keyboard import Listener
from pathlib import Path
from src import MemeWin
from pygame import mixer
from queue import Queue
from threading import Thread



class Meme(MemeWin):


    def __init__(self):
        """Randomly play meme videos\n
        Videos are set to my resolution 1366x768 and 24 fps"""
        super().__init__()
        
        self.text_queue = Queue()
        self.running = True
        self.timer_running = False
        self.display_time = True
        
        self.start_time = 0
        self.meme_start_time = 0
        self.timer_label = None
        self.key_pressed_time = time.time()
        self.key_pressed_time2 = time.time()
        self.key_pressed = []
        self.key_pressed2 = []

        self.media = Path(__file__).resolve().parent / 'media'
        
        # data
        self.w_collection = []
        self.vid_dict = {}
        
        # time trigger for playing memes
        self.meme_t = random.randint(3,4)

        # speedrun audio
        self.sound = None
        self.speed_music = str(self.media / 'spdrunmusic.mp3')

        self.place_timelabel()
        # load dictionary keys
        self.load_dict()
        self.load_collections()
        self.meme_start()
        
        mixer.init()
    

    def load_dict(self):
        # setup paths and label
        # self.vid_dic = {vid_path, audio_path, labeloffx, labeloffy}
        get_m = self.get_m
        self.vid_dict = {
            # 'cena' :       (get_m('bing_cleaned.mp4'),    get_m('bing.wav'),              0.4675, 0.533),
            # 'franku' :     (get_m('franku.mp4'),          get_m('franku.wav'),            0.80, 0.80),
            'shocked' :    (get_m('shocked.mp4'),         get_m('shocked.wav'),           0.50, 0.54),
            # 'cont' :       (get_m('continued.mp4'),       get_m('continued_cleaned.mp3'), 0.50, 0.50),
            # 'vergil' :     (get_m('vergil.mp4'),          get_m('vergil.mp3'),            0.50, 0.50),
            # 'speed' :      (get_m('speed.mp4'),           get_m('speed_cleaned.mp3'),     0.50, 0.50),
            'prettygood' : (get_m('prettygood.mp4'),      get_m('prettygood.mp3'),        0.50, 0.50),
            'eyebrow' :    (get_m('eyebrow.mp4'),         get_m('eyebrow.mp3'),           0.80, 0.50)
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
            inc = random.randint(30,2400)
            self.meme_t = self.play_meme(random_meme, self.meme_t, inc )
            pass
        
        self.root.after(20,self.run_meme_timer)


    def run_timer(self):
        # speedrun timer
        if not self.timer_running:
            self.sound.stop()
            return

        float = time.time() - self.start_time
        time_str = self.format_time(float)

        if self.display_time:
            self.timer_label.lift()
            self.timer_label['text'] = time_str

        self.root.after(20,self.run_timer)
    

    def play_meme(self, keyname:str, time_var : int, inc_time:int) -> int:
        """Returns incremented time trigger value -> inc_time : int = Increment time for next call
        keyname : str = Get data frame from dictionary key,
        time_var : int =  time referrence
        """
        # keep condition from executing more than once in instant
        if not self.playing_video:
            # unpack values from dictionary
            vid, audio, x, y = self.vid_dict[keyname]
            self.play_video(vid,audio,x,y)
            # increment time trigger
            time_var += inc_time
            time_var = random.randint(time_var, time_var+100) # 200

            return time_var


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
        self.sound =  mixer.Sound(self.speed_music)
        self.sound.play()
        self.root.deiconify()

    
    def meme_start(self):
        """start meme timer"""
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
            self.root.withdraw()
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
        collection_path = Path(__file__).resolve().parent / 'data/collection.txt'
        with open(collection_path,'r') as f:
            self.w_collection = f.read().split('\n')
        

    def add_hotkey(self):
        # my ugly logic for listening hotkeys and typed keys
        hotkeys = {
            (".","1") : self.toggle_timer,
            (".","2") : self.show_timer,
            (".","0") : self.exit_,
        }

        def check():
            for hotkey, callback in hotkeys.items():
                if tuple(self.key_pressed) == hotkey:
                    callback()
                    break
        
        def catch():
            # catch not safe typed words
            text = ''.join(self.key_pressed2).split()
            print(text)
            for i in text:
                if i.lower() in self.w_collection:
                    self.play_meme('vergil',0,0)
                    break

        def listen_(key):
            # listener for typed words
            interval = time.time() - self.key_pressed_time2
            self.key_pressed_time2 = time.time()

            if interval < 3:
                self.key_pressed2.append(key.strip("'") if 'Key' not in key else ' ')
                catch()
            else:
                self.key_pressed_time2 = time.time()
                self.key_pressed2.clear()
                self.key_pressed2.append(key.strip("'") if 'Key' not in key else '')

        def listen(key):
            # listener for hotkeys, pressed in right sequence
            # had problems with keyboard.add_hotkeys that's why im using pynput
            interval = time.time() - self.key_pressed_time
            self.key_pressed_time = time.time()

            if interval < 0.10:
                self.key_pressed.append(key.strip("'") if 'Key' not in key else ' ')
                check()
            else:
                self.key_pressed_time = time.time()
                self.key_pressed.clear()
                self.key_pressed.append(key.strip("'") if 'Key' not in key else '')

        def key_listener(key):
            key = str(key)
            listen(key)
            listen_(key)
            
        with Listener(on_press=key_listener) as listener:
            listener.join()

    
    def main(self):
        Thread(target=self.add_hotkey,daemon=True).start()
        self.root.mainloop()


    def exit_(self):
        self.running = False
        mixer.quit()
        self.root.destroy()
        exit(0)




if __name__=='__main__':
    app = Meme()
    app.main()

    pass