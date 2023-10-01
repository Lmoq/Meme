import time
import re
import random
import tkinter as tk
import keyboard as keyb
from pynput.keyboard import Listener
from pathlib import Path
from modules.invwin import MemeWin
from pygame import mixer
from queue import Queue
from threading import Thread



class Meme(MemeWin):


    def __init__(self):
        super().__init__()
        self.text_queue = Queue()
        self.running = True
        self.timer_running = False
        self.display_time = True
        self.playing_video = False

        self.start_time = 0
        self.meme_start_time = 0
        self.timer_label = None
        self.key_pressed_time = None
        self.key_pressed_time2 = None
        self.key_pressed = []
        self.key_pressed2 = []

        self.media = Path(r'C:\Users\Burac\Desktop\-\Time\main\test\edited').resolve()
        self.audio = Path(r'C:\Users\Burac\Desktop\-\Time\main\test\audio').resolve()
        # data
        self.collection = Path(__file__).resolve().parent / 'modules/data'
        self.collection_path = ''
        self.w_collection = []

        # templates
        self.cena_vid = self.get_m('bing_cleaned.mp4')
        self.cena_audio = self.get_m('bing_cleaned.wav')
        self.cena = random.randint(300,410)

        self.franku_vid = self.get_m('franku.mp4')
        self.franku_audio = self.get_m('franku.wav')
        self.franku = random.randint(20,23)

        self.shok_vid = self.get_m('shocked_cleaned.mp4')
        self.shok_audio = self.get_m('shocked_cleaned.wav')
        self.shok = random.randint(1200,1300)

        self.cont_vid = self.get_m('continued.mp4')
        self.cont_audio = self.get_m('continued_cleaned.wav')
        self.cont = random.randint(6,7)

        self.vergil_vid = self.get_m('cut.mp4')
        self.vergil_audio = self.get_m('cut_cleaned.mp3')
        self.vergil = random.randint(6100,6400)

        self.speed_vid = self.get_m('speed.mp4')
        self.speed_audio = self.get_m('speed_cleaned.mp3')
        self.speed = random.randint(300,910)

        self.meme_t = random.randint(3,4)

        # audio
        self.sound = None
        self.speed_music = str(self.audio / 'spdrunmusic.mp3')

        self.place_timelabel()
        # load dictionary keys
        self.load_dict()
        self.load_collections()
        # self.meme_start()
        mixer.init()
    

    def load_dict(self):
        # configure video setup
        self.dic_img = {
            # 'cena' :     (self.cena_vid, self.cena_audio,   0.4675, 0.533),
            # 'franku' : (self.franku_vid, self.franku_audio, 0.80, 0.80),
            'shocked' :  (self.shok_vid, self.shok_audio,   0.50, 0.54),
            'cont' :     (self.cont_vid, self.cont_audio,   0.50, 0.50),
            'vergil' : (self.vergil_vid, self.vergil_audio, 0.50, 0.50),
            'speed' :   (self.speed_vid, self.speed_audio,  0.50, 0.50),
        }
        # keyb.add_hotkey('z', lambda : self.play_video('vergil'))
        # keyb.add_hotkey('a', lambda : self.play_video('cont'))
        # keyb.add_hotkey('-', lambda : self.play_video('franku'))
        # keyb.add_hotkey('x', lambda : self.play_video('shocked'))

    def load_collections(self):
        self.collection_path = str(self.collection / 'mainmodulesdata.txt')
        with open(self.collection_path,'r') as f:
            self.w_collection = f.read().split('\n')


    def get_m(self,filename):
        return str(self.media / filename)


    def run_meme_timer(self):
        if not self.running:
            print('returned')
            return
        
        time_ = time.time() - self.meme_start_time

        if time_ > self.meme_t:
            random_meme = random.choice(list(self.dic_img.keys()))
            # if random_meme == 'shocked': inc = 3
            # elif random_meme == 'cont' : inc = 12
            # elif random_meme == 'vergil': inc = 25
            # elif random_meme == 'speed' : inc = 18
            inc = random.randint(30,3600)
            print(inc)
            self.meme_t = self.play_meme(random_meme, self.meme_t, inc )
            pass
        

        self.root.after(20,self.run_meme_timer)


    def run_timer(self):
        if not self.timer_running:
            self.sound.stop()
            return

        float = time.time() - self.start_time
        time_str = self.format_time(float)

        if self.display_time:
            self.timer_label.lift()
            self.timer_label['text'] = time_str

        self.root.after(20,self.run_timer)
    

    def play_meme(self, keyname:str, time_var : object, inc_time:int) -> int:
        """Returns incremented int value -> inc_time : int = Increment time for next call
        keyname : str = Get data frame from dictionary key,
        audio : str = Audio path,
        time_var : object =  class attr time referrence
        offx, offy : int = Label offset anchored to center,
        """
        if not self.playing_video:
            # keep condition from executing more than once in instant
            self.playing_video = True
            self.play_video(keyname)
            # increment time trigger
            time_var += inc_time
            time_var = random.randint(time_var, time_var+2) # 200
            # reset
            self.playing_video = False

            return time_var


    def format_time(self,time:float):
        # format float to str format
        hours = int(time / 3600) % 24
        mins = int(time / 60) % 60
        sec = time % 60
        
        return f'{hours:02d}:{mins:02d}:{sec:05.2f}'
    

    def timer_start(self):
        # starts timer
        self.start_time = time.time()
        self.run_timer()
        self.sound =  mixer.Sound(self.speed_music)
        self.sound.play()

    
    def meme_start(self):
        """start meme timer"""
        self.meme_start_time = time.time()
        self.run_meme_timer()


    def toggle_timer(self):
        self.timer_running = not self.timer_running
        if self.timer_running:
            self.timer_start()
        
    
    def show_timer(self):
        self.display_time = not self.display_time
        if not self.display_time:
            self.timer_label['text']=" "


    def place_timelabel(self):
        self.timer_label = tk.Label(
            text='00:00:00',
            font=(None,24),
            fg=self.text_color,
            bg=self.sac_color)

        self.timer_label.place(x=1150,y=30)
    

    def listener_(self,key):
        # listener with longer time interval
        if self.key_pressed_time2 is not None:
            interval = time.time() - self.key_pressed_time2
            self.key_pressed_time2 = time.time()

            if interval < 3:
                self.key_pressed2.append(key.strip("'") if 'Key' not in key else ' ')
                self.catch()
            else:
                self.key_pressed_time2 = time.time()
                self.key_pressed2.clear()
                self.key_pressed2.append(key.strip("'") if 'Key' not in key else '')
        else:
            self.key_pressed_time2 = time.time()
            self.key_pressed2.append(key.strip("'") if 'Key' not in key else '')

    
    def catch(self):
        text = ''.join(self.key_pressed2).split()
        print(text)
        for i in text:
            if i in self.w_collection:
                self.play_video('vergil')
                break


    def add_hotkey(self):

        hotkeys = {
            (".","1") : self.toggle_timer,
            (".","2") : self.show_timer,
            (".","0") : self.exit_,
        }

        def parse_hotkeys():
            for hotkey, callback in hotkeys.items():
                if tuple(self.key_pressed) == hotkey:
                    callback()
                    break


        def key_listener(key):
            key = str(key)
            if self.key_pressed_time is not None:
                interval = time.time() - self.key_pressed_time
                self.key_pressed_time = time.time()

                if interval < 0.10:
                    self.key_pressed.append(key.strip("'") if 'Key' not in key else ' ')
                    parse_hotkeys()
                else:
                    self.key_pressed_time = time.time()
                    self.key_pressed.clear()
                    self.key_pressed.append(key.strip("'") if 'Key' not in key else '')
            else:
                self.key_pressed_time = time.time()
                self.key_pressed.append(key.strip("'") if 'Key' not in key else '')
            # listener with longer time interval
            self.listener_(key)
            
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