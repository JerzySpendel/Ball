import sdl2, sdl2.sdlgfx
from ctypes import *
import math
STANDARD_LENGTH = 1
class Vector:
    def __init__(self, x=None, y=None):
        if x==None and y==None:
            self.x, self.y = 1,0
        else:
            self.x, self.y = x,y

    def length(self):
        return math.sqrt(self.x**2+self.y**2)

    def current_angle(self):
        v = Vector()
        return Vector.angle_between(self, v)

    def reduce_me(self, to=STANDARD_LENGTH):
        if self.length()>to:
            sin = self.y/self.length()
            angr = math.asin(sin)
            sin_a = math.sin(angr)
            cos_a = math.cos(angr)
            if cos_a < 0:
                if self.x > 0:
                    self.x = -to*cos_a
                else:
                    self.x = to*cos_a
            elif cos_a >= 0:
                if self.x > 0:
                    self.x = to*cos_a
                else:
                    self.x = -to*cos_a
            if sin_a < 0:
                if self.y > 0:
                    self.y = -to*sin_a
                else:
                    self.y = to*sin_a
            else:
                if self.y > 0:
                    self.y = to*sin_a
                else:
                    self.y = -to*sin_a

    def update_to_angle(self, ang, dt):
        angr = math.radians(ang)
        v = (1,0)
        xp = v[0]*math.cos(angr) - v[1]*math.sin(angr)
        yp = v[0]*math.sin(angr) + v[1]*math.cos(angr)
        vp = (xp*dt*3, yp*dt*3)
        self.x += vp[0]
        self.y += vp[1]
        self.reduce_me()

    def set_angle(self, ang):
        l = self.length()
        ang = math.radians(ang)
        self.x = l*math.cos(ang)
        self.y = l*math.sin(ang)

    def imitate_resistance(self, dt):
        l = self.length()
        if l > 0:
            c_p = l/STANDARD_LENGTH #Aktualny procent dlugosci
            n_p = c_p - dt #Nowy
            if n_p < 0:
                self.reduce_me(0)
                return
            self.reduce_me(n_p*STANDARD_LENGTH)

    def collide(self, v):
        pass

    @staticmethod
    def angle_between(v1, v2=None):
        if v2 == None:
            v2 = Vector()
        i = v1.x*v2.x+v1.y*v2.y
        ii = v1.length()*v2.length()
        if ii != 0:
            cos = i/ii
            ang = math.acos(cos)
            return ang
        return None

    def __repr__(self):
        return '<class Vector=[{},{}]>'.format(self.x, self.y)

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

class Collision:
    @staticmethod
    def collide(b1,b2):
        v = b2.middle[0] - b1.middle[0], b2.middle[1] - b1.middle[1]
        v = Vector(v[0],v[1])
        b1.v.x *= -1
        b1.v.y *= -1
        print(Vector.angle_between(v))
