# Meme-inator
This app plays or interrupts you with memes, you can use this to annoy your friends or yourself. This uses tkinter and display video frames to a label. The video used are edited green screens.
## Usage 
- Clone this repo
- pip install requirements.txt
- Run the main.pyw
Memes will start displaying at 3 to 4 seconds. You can adjust it when initializing the class.
```
app = Meme(
    meme_start = (3, 4), 
    inc_time = (30, 2400), 
    hidden = True)
```
## Note
- This will only work on top of non fullscreen apps. 
- The fullscreen videos are only available in 1366x768, and the label offsets are based on this resolution.
- You can switch to memelite branch for slow network, or if you just want to test it out.
---
## Customization
- If you want to add more videos, edit a green screen video to a black background with the audio file separated.
- I used davinci resolve and did a basic green screen edit, that's why videos seems poorly edited and doesnt sync with audio. 
- Then modify the dictionary inside main.pyw and adjust the offset if the frames displayed are in wrong coordinates.
```
# self.vid_dic = {keyname, (vid_path, audio_path), labeloffx, labeloffy}
self.vid_dict = {
    'shocked' :    (get_m('shocked.mp4'),     get_m('shocked.wav'),           0.50, 0.54),
    'prettygood' : (get_m('prettygood.mp4'),  get_m('prettygood.mp3'),        0.50, 0.50),
    'added_video': (get_m('added_video.mp4),  get_m('added_video_audio_path')  labeloffset_x, labeloffset_y)
    }

```
---
## Features
- This application uses pynput keyboard listener for hotkeys and typed words, vergil will interrupt if you typed degen or not safe words, or asked for motivation. (*Available only at main branch*)

<img src="https://github.com/Lmoq/Meme/blob/master/assets/verg.gif" >


- You can have speedrun timer, with dream speedrun music playing.
Press the hotkey "." + "1" to toggle timer. Make sure to set hidden to False so window wont be withdrawn.
```
app = Meme(hidden = False)
```

<img src="https://github.com/Lmoq/Meme/blob/master/assets/timer.gif" >