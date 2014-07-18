import sdl2, sdl2.sdlgfx
from ctypes import *
class SpeedVector:
    w = 100
    h = 100
    def __init__(self, player):
        self.player = player
        self.tex = None
        self.rect = sdl2.SDL_Rect()
        self.rect.x = self.player.win.w - self.w
        self.rect.y = 0
        self.rect.w, self.rect.h = self.w, self.h
        self.tex = sdl2.SDL_CreateTexture(self.player.ren, sdl2.SDL_PIXELFORMAT_RGBA8888,
                sdl2.SDL_TEXTUREACCESS_TARGET, self.w, self.h)
        sdl2.SDL_SetTextureBlendMode(self.tex, sdl2.SDL_BLENDMODE_BLEND)
    def _calculate_vector(self):
        ''' Calculate the speed vector's offsets '''
        pz = self.w//2
        return (self.w//2, self.h//2, self.player.v.x*self.player.speed//2+pz, -self.player.v.y*self.player.speed//2+pz)

    def generateTexture(self):
        sdl2.SDL_SetRenderTarget(self.player.ren, self.tex)
        sdl2.SDL_RenderClear(self.player.ren)
        sdl2.sdlgfx.filledCircleRGBA(self.player.ren, self.w//2, self.h//2, 3, 0,0,255,255)

        line1 = [self.w//2, 0, self.w//2, self.h]
        line2 = [0, self.h//2, self.w, self.h//2]
        speed = self._calculate_vector()
        sdl2.sdlgfx.lineRGBA(self.player.ren, line1[0], line1[1], line1[2], line1[3], 0,0,255,255)
        sdl2.sdlgfx.lineRGBA(self.player.ren, line2[0], line2[1], line2[2], line2[3], 0,0,255,255)
        sdl2.sdlgfx.lineRGBA(self.player.ren, speed[0], speed[1], int(speed[2]), int(speed[3]), 0,0,255,255)
        sdl2.SDL_SetRenderTarget(self.player.ren, None)

    def draw(self):
        self.generateTexture()
        sdl2.SDL_RenderCopy(self.player.ren, self.tex, None, byref(self.rect))
        sdl2.SDL_RenderPresent(self.player.ren)
