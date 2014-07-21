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
        return math.degrees(math.acos((self.x*v.x+self.y*v.y)/(self.length()*v.length())))

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

    @staticmethod
    def angle_between(v1, v2):
        i = v1.x*v2.x+v1.y*v2.y
        cos = i/(v1.length()*v2.length())
        return math.acos(cos)
class Ball:
    direction = 0b0000 # UP RIGHT DOWN LEFT
    v = Vector()
    speed = 100
    state = None
    tex = None
    pixels = []
    def __init__(self, win, rad=None, x=None, y=None):
        if rad == None:
            self.rad = 9
            self.w = self.rad*2+2
            self.h = self.rad*2+2
        else:
            self.rad = rad
            self.w = self.rad*2+2
            self.h = self.rad*2+2
        if x == None and y == None:
            self._x = 0
            self._y = 0
        else:
            self._x = x
            self._y = y
        self._pixels = []
        self.win = win
        self.ren = sdl2.SDL_GetRenderer(self.win.window)
        self._generateTexture()
        self._initPixels()

    @property
    def x(self):
        return int(self._x)

    @x.setter
    def x(self, v):
        self._x = v

    @property
    def y(self):
        return int(self._y)

    @y.setter
    def y(self, v):
        self._y = v

    @property
    def rect(self):
        r = sdl2.SDL_Rect()
        r.x, r.y, r.w, r.h = self.x, self.y, self.w, self.h
        return r

    @property
    def pixels(self):
        return self._pixels

    def pixels_in_rect(self, r):
        t=[(x,y) for x in range(r.x, r.x+r.w) for y in range(r.y, r.y+r.h)]
        n = []
        translated = self.translate_pixels()
        for (x,y) in t:
            if (x,y) in translated:
                n.append((x,y))
        return n

    def translate_pixels(self, rect=None):
        if rect==None:
            return [(self.x+xy[0], self.y+xy[1]) for xy in self.pixels]

    def _generateTexture(self):
        self.tex = sdl2.SDL_CreateTexture(self.ren, sdl2.SDL_PIXELFORMAT_RGBA8888, sdl2.SDL_TEXTUREACCESS_TARGET, self.w, self.h)
        sdl2.SDL_SetTextureBlendMode(self.tex, sdl2.SDL_BLENDMODE_BLEND)
        sdl2.SDL_SetRenderTarget(self.ren, self.tex)
        sdl2.sdlgfx.aacircleRGBA(self.ren, 10,10,self.rad,255,0,0,255)
        sdl2.SDL_SetRenderTarget(self.ren, None)

    def _initPixels(self):
        pixels = (c_void_p*(self.w*self.h))()
        sdl2.SDL_SetRenderTarget(self.ren, self.tex)
        sdl2.SDL_RenderReadPixels(self.ren, None, sdl2.SDL_PIXELFORMAT_RGBA8888, pixels, self.w*4)
        pixels = cast(pixels, POINTER(c_uint))
        for x,y in [(x,y) for x in range(self.w) for y in range(self.h)]:
            p = pixels[self.w*y + x]
            if (p & 0xFF000000) >> 24 > 30:
                pixel = (x,y)
                self._pixels.append(pixel)
        sdl2.SDL_SetRenderTarget(self.ren, None)

    def draw(self):
        r = sdl2.SDL_Rect()
        r.x = self.x
        r.y = self.y
        r.w = self.w
        r.h = self.h
        sdl2.SDL_RenderCopy(self.ren, self.tex, None, byref(r))

    def _update_vector(self, dt):
        d = self.direction
        if d == 0b1000:
            self.v.update_to_angle(90, dt)
        elif d == 0b1100:
            self.v.update_to_angle(45, dt)
        elif d == 0b0100:
            self.v.update_to_angle(0, dt)
        elif d == 0b0010:
            self.v.update_to_angle(270, dt)
        elif d == 0b0110:
            self.v.update_to_angle(315, dt)
        elif d == 0b0011:
            self.v.update_to_angle(225, dt)
        elif d == 0b0001:
            self.v.update_to_angle(180, dt)
        elif d == 0b1001:
            self.v.update_to_angle(135, dt)
        elif d == 0b0000:
            self.v.imitate_resistance(dt)

    def update(self, dt):
        self._update_vector(dt)
        self._x += self.v.x*dt*self.speed
        self._y -= self.v.y*dt*self.speed

    def collision(self, b):
        r1 = self.rect
        r2 = b.rect
        rr = sdl2.SDL_Rect()
        if sdl2.SDL_IntersectRect(byref(r1), byref(r2), byref(rr)) == sdl2.SDL_TRUE:
            p1 = self.pixels_in_rect(rr)
            p2 = b.pixels_in_rect(rr)
            for xy in p1:
                if xy in p2:
                    print('Kolizja')
                    break
class Player(Ball):
    angle = 0
    def __init__(self, win):
        Ball.__init__(self, win)
        self.win = win
        self.v = Vector()

    def handle_event(self, e):
        sym = e.key.keysym.sym
        if e.type == sdl2.SDL_KEYDOWN:

            if sym == sdl2.SDLK_UP:
                self.direction = self.direction | 0b1000
            elif sym == sdl2.SDLK_RIGHT:
                self.direction = self.direction | 0b0100
            elif sym == sdl2.SDLK_DOWN:
                self.direction = self.direction | 0b0010
            elif sym == sdl2.SDLK_LEFT:
                self.direction = self.direction | 0b0001

        elif e.type == sdl2.SDL_KEYUP:
            if sym == sdl2.SDLK_UP:
                self.direction = self.direction & 0b0111
            elif sym == sdl2.SDLK_RIGHT:
                self.direction = self.direction & 0b1011
            elif sym == sdl2.SDLK_DOWN:
                self.direction = self.direction & 0b1101
            elif sym == sdl2.SDLK_LEFT:
                self.direction = self.direction & 0b1110
        if self.direction == 0b1010 or self.direction == 0b0101:
            self.direction = 0b0000


