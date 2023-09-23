import tkinter as tk
from pathlib import Path
from my import SaveVideo

def save_framedata():
    db_path = Path(__file__).resolve().parent / 'data/videos.db'
    db = SaveVideo(str(db_path))

    db.connect()




if __name__=='__main__':
    


    pass