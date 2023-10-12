## Usage 
- Clone this repo
- Run the main.pyw

This will only work on top of non fullscreen apps. Memes will start displaying at 3 to 4 seconds. You can customize it when initializing the class.
```
app = Meme(
    meme_start = (3, 4), 
    inc_time = (30, 2400), 
    hidden = True)
```
You can switch so memelite branch for slow network, and if you just want to test it out.
---
## Customization
You can add more videos, just use black background and remove green screen. I used davinci resolve and did a basic green screen edit. Just modify the dictionary inside main.pyw, adjust the offset if the frames displayed are in wrong coordinates.
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

<img src="https://github.com/Lmoq/Meme/blob/master/assets/faceindark.png" >

>hello
>how are you
>if name :
>    func()








