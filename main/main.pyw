import time
import random
import tkinter as tk
import keyboard as keyb
from pathlib import Path
from modules.invwin import MemeWin
from pygame import mixer
from queue import Queue



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

        self.media = Path(r'C:\Users\Burac\Desktop\-\Time\main\test\edited').resolve()
        self.audio = Path(r'C:\Users\Burac\Desktop\-\Time\main\test\audio').resolve()

        # templates
        self.cena_vid = self.get_m('bing_cleaned.mp4')
        self.cena_audio = self.get_m('bing_cleaned.wav')
        self.cena = random.randint(3,4)

        self.franku_vid = self.get_m('franku.mp4')
        self.franku_audio = self.get_m('franku.wav')
        self.franku = random.randint(20,23)

        self.shok_vid = self.get_m('shocked_cleaned.mp4')
        self.shok_audio = self.get_m('shocked_cleaned.wav')
        self.shok = random.randint(500,600)

        self.cont_vid = self.get_m('continued.mp4')
        self.cont_audio = self.get_m('continued_cleaned.wav')
        self.cont = random.randint(300,400)

        self.vergil_vid = self.get_m('cut.mp4')
        self.vergil_audio = self.get_m('cut_cleaned.mp3')
        self.vergil = random.randint(3,4)

        self.speed_vid = self.get_m('speed.mp4')
        self.speed_audio = self.get_m('speed_cleaned.mp3')
        self.speed = random.randint(3,4)

        # audio
        self.sound = None
        self.speed_music = str(self.audio / 'spdrunmusic.mp3')

        self.place_timelabel()
        # load dictionary keys
        self.load_dict()
        self.meme_start()
        mixer.init()
    

    def load_dict(self):
        # configure video setup
        self.dic_img = {
            'cena' :   (self.cena_vid, self.cena_audio, 0.4675, 0.533),
            'franku' : (self.franku_vid, self.franku_audio, 0.80, 0.80),
            'shocked' :(self.shok_vid, self.shok_audio, 0.50, 0.54),
            'cont' :   (self.cont_vid, self.cont_audio, 0.50, 0.50),
            'vergil' : (self.vergil_vid, self.vergil_audio, 0.50, 0.50),
            'speed' :  (self.speed_vid, self.speed_audio, 0.50, 0.50),
        }
        keyb.add_hotkey('z', lambda : self.play_video('vergil'))
        keyb.add_hotkey('a', lambda : self.play_video('cont'))
        keyb.add_hotkey('q', lambda : self.play_video('speed'))


    def get_m(self,filename):
        return str(self.media / filename)


    def run_meme_timer(self):
        if not self.running:
            print('returned')
            return
        
        time_ = time.time() - self.meme_start_time
        # if time_ > self.cena:
        #     self.cena = self.play_meme('cena', self.cena, 40 )
        #     pass
        
        # if time_ > self.franku:
        #     print('playing ')
        #     self.franku = self.play_meme('franku', self.franku, 30)
        #     print(self.franku)

        if time_ > self.shok:
            self.shok = self.play_meme('shocked', self.shok, 2600)
            
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
            time_var = random.randint(time_var, time_var+200) # 200
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

        keyb.add_hotkey('.+1', self.toggle_timer)
        keyb.add_hotkey('.+0', self.exit_)
        keyb.add_hotkey('.+2', self.show_timer)
    

    def exit_(self):
        self.running = False
        mixer.quit()
        self.root.destroy()
        exit(0)




if __name__=='__main__':
    app = Meme()
    app.main()

    pass