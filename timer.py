import sdl2

class Timer:
    def __init__(self):
        self.ts = sdl2.SDL_GetTicks()

    def tick(self):
        new = sdl2.SDL_GetTicks()
        dt = new - self.ts
        self.ts = new
        return dt/1000
