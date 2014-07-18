import sdl2
import sdl2.ext
import sdl2.sdlgfx
import time
from ctypes import *
from timer import Timer
from ball import Ball, Player
from vector import SpeedVector


class Window:
    w = 640
    h = 480
    def __init__(self):
        sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
        self.window = sdl2.SDL_CreateWindow(c_char_p(b"Haxball"), 100, 100, self.w, self.h, sdl2.SDL_WINDOW_SHOWN)
        self.ren = sdl2.SDL_CreateRenderer(self.window, -1, sdl2.SDL_RENDERER_ACCELERATED)

w = Window()
p = Player(w)
b = Ball(w, rad=9,x=100,y=100)
s = SpeedVector(p)
sdl2.SDL_RenderClear(w.ren)
e = sdl2.SDL_Event()
quit = False
timer = Timer()
while not quit:
    sdl2.SDL_SetRenderDrawColor(w.ren, 0,0,0,255)
    sdl2.SDL_RenderClear(w.ren)
    while(sdl2.SDL_PollEvent(byref(e))):
            if e.type == sdl2.SDL_QUIT:
                quit = True
            p.handle_event(e)
    dt = timer.tick()
    p.update(dt)
    p.draw()
    b.draw()
    s.draw()
    p.collision(b)
    sdl2.SDL_RenderPresent(w.ren)
    print(dt)
    sdl2.SDL_Delay(2)
