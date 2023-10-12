## Usage 
- Clone this repo
- Run the main.pyw
This will only work on top of non fullscreen apps. Memes will start displaying at 3 to 4 seconds. You can customize it when initializing the class
```
app = Meme(
    meme_start = (3, 4), 
    inc_time = (30, 2400), 
    hidden = True)
```


## Features

This application also has a keyboard listener, vergil will interrupt if you typed degen words, nsfw, or asked for motivation.

<img src="https://github.com/Lmoq/Meme/blob/master/assets/verg.gif" >


You can have speedrun timer, with dream speedrun music playing.
Press the hotkey "." + "1" to toggle timer.

<img src="https://github.com/Lmoq/Meme/blob/master/assets/timer.gif" >

<img src="https://github.com/Lmoq/Meme/blob/master/assets/faceindark.png" >

>hello
>how are you
>if name :
>    func()

You can add your own videos then add them to dictionary, inside main.pyw

```
self.vid_dict = {
    'shocked' :    (get_m('shocked.mp4'),     get_m('shocked.wav'),           0.50, 0.54),
    'prettygood' : (get_m('prettygood.mp4'),  get_m('prettygood.mp3'),        0.50, 0.50),
    'added_video': (get_m('added_video.mp4),  get_m('added_video_audio_path')  labeloffset_x, labeloffset_y)
    }
```




