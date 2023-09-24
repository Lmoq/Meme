import tkinter as tk
from pathlib import Path
from my import FrameData

def save_framedata():
    db_path = Path(__file__).resolve().parent / 'data/videos.dat'
    db = FrameData(str(db_path))

    vid_folder = Path(r'C:\Users\Burac\Desktop\-\Time\main\test\edited').resolve()
    video = str(vid_folder / 'bing_cleaned.mp4')
    audio = str(vid_folder / 'bing_cleaned.wav')

    db.save_frames('cena', video, audio)



if __name__=='__main__':
    save_framedata()



    pass