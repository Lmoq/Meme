import tkinter as tk
from pathlib import Path
from my import FrameData

def save_framedata():
    db_path = Path(__file__).resolve().parent / 'data/videos.dat'
    db = FrameData(str(db_path))

    vid_folder = Path(r'C:\Users\Burac\Desktop\-\Time\main\test\images').resolve()

    db.save_frames(vid_folder)



if __name__=='__main__':
    save_framedata()



    pass