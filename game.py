from enum import Enum
import pyglet
from pyglet import clock
from pyglet.gl import *
from pyglet.window import key
from pyglet.image.codecs.png import PNGImageDecoder

# Controle de Frame-rating
FPS = 61
frame_count = 0

# Janela
TITLE = "Steroids"
SIZE = (640, 480)

scene = None
fps_display = clock.ClockDisplay()
keys = []

# -----------------------------------------------------------------------------
# Material para estruturação do jogo
# -----------------------------------------------------------------------------


class Rect:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def intersects(self, rect):
        return not ((self.right < rect.left) or
                    (self.left > rect.right) or
                    (self.top > rect.bottom) or
                    (self.bottom < rect.top))


class Window(pyglet.window.Window):
    def __init__(self, width, height, *args, **kwargs):
        super(Window, self).__init__(width=width, height=height,
                                     *args, **kwargs)
        self.x_proportion = 1
        self.y_proportion = 1

    def on_draw(self):
        return
        self.clear()

    def on_close(self):
        self.close()
        exit(0)

    def on_key_press(self, symbol, modifiers):
        keys.append(str(symbol))
        scene.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        keys.remove(str(symbol))

    def on_resize(self, width, height):
        self.x_proportion = width/SIZE[0]
        self.y_proportion = height/SIZE[1]
        super(Window, self).on_resize(width, height)
        self.on_draw()


# TENTA ISSO:

#import subprocess

#subprocess.call(["afplay","music_file.mp3"])


class SoundManager:
    # Media Player para BGMs
    def __init__(self):
        self.player = pyglet.media.Player()
        self.player.eos_action = pyglet.media.Player.EOS_LOOP

    def play(self, resource):
        # print("play")
        self.player.next()
        self.player.queue(resource)
        self.player.play()


class Sprite:
    # Gráfico com propriedades alteradas na exibição e
    # método próprio de desenho
    def __init__(self, filename):
        self.bitmap = pyglet.image.load(filename, decoder=PNGImageDecoder())
        self.x = 0
        self.y = 0
        self.width = self.bitmap.width
        self.height = self.bitmap.height
        self.ox = 0
        self.oy = 0
        self.angle = 0
        self.visible = True

    def update(self, window):
        if not self.visible:
            return
        trueX = (self.x) * window.x_proportion
        trueY = (SIZE[1] - (self.y + self.bitmap.height)) * window.y_proportion
        glTranslatef(trueX, trueY, 0)
        glRotatef(-self.angle, 0, 0, 1)
        self.bitmap.blit(-self.ox,
                         -self.oy,
                         width=self.bitmap.width*window.x_proportion,
                         height=self.bitmap.height*window.y_proportion)
        glRotatef(+self.angle, 0, 0, 1)
        glTranslatef(-trueX, -trueY, 0)


class SpaceObjectType(Enum):
    asteroid = 0
    speedUp = 1
    powerUp = 2


class SpaceObject(Sprite):
    # Objetos que interagem com o jogador ou com os tiros.
    # Podem ser
    #   - Asteróides que se dividirão ao serem acertados e
    # darão dano ao jogador quando nele tocar;
    #   - Itens que surgem a cada X frames, dando algum bônus ao jogador.
    def __init__(self, x, y, obj_type, dx=0, dy=0):
        self.x = x
        self.y = y
        self.obj_type = obj_type
        if obj_type == SpaceObjectType.asteroid:
            super(SpaceObject, self).__init__('img/stronda.png')
        self.dx = dx
        self.dy = dy

    def update(self, window):
        self.x += self.dx
        self.y += self.dy
        if self.x - self.ox > SIZE[0]:
            self.x = -(self.ox+self.width)
        if self.y - self.ox > SIZE[1]:
            self.y = -(self.oy+self.height)
        if self.x + self.width + self.ox < 0:
            self.x = SIZE[0]
        if self.y + self.height + self.ox < 0:
            self.y = SIZE[1]
        super(SpaceObject, self).update(window)

    def on_collide_with_player(self):
        print("Colidiu com jogador")

    def on_collide_with_shot(self):
        print("Colidiu com tiro")


class SceneBase:
    def on_key_press(self, symbol, modifiers):
        pass
