from pygame import mixer

class Mixer:
    def __init__(self) -> None:
        mixer.init()
        
        self.soundtracks = [
            "assets/sounds/soundtrack/minecraft.wav",
            "assets/sounds/soundtrack/subwoofer_lullaby.wav",
        ]
        self.current_soundtrack = 0
        
        self.harvest_sound = mixer.Sound("assets/sounds/harvest.wav")
        self.harvest_sound.set_volume(1)
        self.put_sound = mixer.Sound("assets/sounds/put.wav")
        self.put_sound.set_volume(1)

    def play_soundtrack(self) -> None:
        if not mixer.music.get_busy():
            mixer.music.load(self.soundtracks[self.current_soundtrack])
            mixer.music.play()
            self.current_soundtrack = (self.current_soundtrack + 1) % len(self.soundtracks)
