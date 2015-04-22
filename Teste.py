import pyglet
from pyglet.window import mouse
from pyglet.window import key

window = pyglet.window.Window(640, 480)
window.set_caption("Steroids")
window.set_mouse_visible(False)

# Soh declarando azibagem
image = pyglet.image.load('img/xicrinha.png')
image.x = 320 - image.width/2
image.y = 240 - image.height/2
image2 = pyglet.image.load('img/frame.PNG')
frame = image2.get_region(0, 0, 109, 321)
xas = 0

# Sonzinhos
porrada = pyglet.media.load('snd/punchVladimir.wav', streaming=False)


class SoundManager:
    def __init__(self):
        self.player = pyglet.media.Player()

    def play(self, resource):
        self.player.next()
        self.player.queue(resource)
        self.player.play()
        # player = pyglet.media.Player()
        # player.queue(resource)
        # player.play()


sfxplayer = SoundManager()
musicplayer = SoundManager()

def sumx():
    global xas
    xas = (xas + 1) % 5


# Testes com muzisquinha
music = pyglet.media.load('bgm/Johnny.mp3')
musicplayer.play(music)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    on_mouse_motion(x,y,dx,dy)

# sei la o que eh "dx" e "dy"
@window.event
def on_mouse_motion(x, y, dx, dy):
    image.x = x
    image.y = y - image.height


# Ver quais modifiers existem
@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        image.x = x


# Aqui ta legal
@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.LEFT:
        image.x += 10
        # porrada.play()
        sfxplayer.play(porrada)

# Tudo funciona ok
# soh que a droga do pyglet considera o canto esquerdo-abaixo como ponto
@window.event
def on_draw():
    window.clear()
    sumx()
    frame = image2.get_region(109 * xas, 0, 109, 321)
    frame.blit(320 - image2.width/2, 240-image2.height/2)
    image.blit(image.x, image.y)


@window.event
def on_close():
    exit(0)


# Principalzinho =)
pyglet.app.run()
