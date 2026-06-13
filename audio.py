import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self._load_sound("rain", "assets/rain.wav", volume=0.5)
        self._load_sound("grow", "assets/grow.wav", volume=0.7)
        self._load_sound("snap", "assets/snap.wav", volume=0.8)
        self._load_sound("bloom", "assets/bloom.wav", volume=0.6)
        self._load_sound("click", "assets/click.wav", volume=0.4)
    def play_background_music(self, filepath="assets/background.mp3", volume=0.2):
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
        except pygame.error:
            print(f"Warning: Could not load background music at '{filepath}'.")
            
    def _load_sound(self, name, filepath, volume=1.0):
        try:
            sound = pygame.mixer.Sound(filepath)
            sound.set_volume(volume)
            self.sounds[name] = sound
        except FileNotFoundError:
            print(f"Warning: Audio file '{filepath}' not found. Audio disabled for '{name}'.")
            self.sounds[name] = None

    def play(self, name):
        """Plays the requested sound if it successfully loaded."""
        if name in self.sounds and self.sounds[name] is not None:
            self.sounds[name].play()
    
