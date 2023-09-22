from pathlib import Path
from my import save_frames

base_folder = Path(r'C:\Users\Burac\Desktop\-\Time\main\test\edited').resolve()
shelf = str(Path(__file__).resolve().parent / 'data/frames.dat')




if __name__=='__main__':
    
    vid = str(base_folder/'bing_cleaned.mp4')
    audio = str(base_folder/'bing_cleaned.wav')
    
    save_frames(shelf, vid, audio, 'cena')
    pass