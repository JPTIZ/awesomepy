import pyglet
from pyglet import clock
from pyglet.gl import *
from pyglet.window import key
from pyglet.image.codecs.png import PNGImageDecoder

# Controle de Frame-rating
FPS = 60
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


class Window(pyglet.window.Window):
    def __init__(self, width, height, *args, **kwargs):
        super(Window, self).__init__(width=width, height=height,
                                     *args, **kwargs)
        self.x_proportion = 1
        self.y_proportion = 1

    def on_draw(self):
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


class SoundManager:
    def __init__(self):
        self.player = pyglet.media.Player()
        self.player.eos_action = pyglet.media.Player.EOS_LOOP

    def play(self, resource):
        self.player.next()
        self.player.queue(resource)
        self.player.play()


class Sprite:
    def __init__(self, filename):
        self.bitmap = pyglet.image.load(filename, decoder=PNGImageDecoder())
        self.x = 0
        self.y = 0
        self.angle = 0
        self.visible = True

    def update(self, window):
        if not self.visible:
            return
        trueX = self.x * window.x_proportion
        trueY = (SIZE[1] - (self.y+self.bitmap.height)) * window.y_proportion
        glTranslatef(self.x, self.y, 0)
        glRotatef(self.angle, 0, 0, 1)
        self.bitmap.blit(trueX,
                         trueY,
                         width=self.bitmap.width*window.x_proportion,
                         height=self.bitmap.height*window.y_proportion)
        glRotatef(-self.angle, 0, 0, 1)
        glTranslatef(-self.x, -self.y, 0)


class SceneBase:
    def on_key_press(self, symbol, modifiers):
        print("Pressionou tecla")
        print("Tecla: "+str(symbol))
