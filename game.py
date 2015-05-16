import math
from enum import Enum
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

def radial(angle):
    return angle*math.pi/180

# -----------------------------------------------------------------------------
# Material para estruturação do jogo
# -----------------------------------------------------------------------------


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, point):
        if isinstance(point, Point):
            self.x += point.x
            self.y += point.y
            return self
        else:
            print("--------Não é ponto =T--------")

    def __sub__(self, point):
        if isinstance(point, Point):
            self.x -= point.x
            self.y -= point.y
            return self
        else:
            print("--------Não é ponto =T--------")


class Rect:
    def __init__(self, left, top, right, bottom, angle = 0):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.angle = angle

    #--------------------------------------------------------------------------
    # COLISÃO DE RETÂNGULOS ROTACIONADOS
    #--------------------------------------------------------------------------
    #
    # >>> colisao = min(Proj.B) <= max(Proj.A) or max(Proj.B) >= min(Proj.A)
    #
    #--------------------------------------------------------------------------
    # Algoritmo:
    #
    # 1. Identificar os eixos nos quais projetaremos os vértices;
    #   1.1. Axis.(x,y) = A.UpRight(x,y) - A.UpLeft(x,y)
    #
    # 2. Projetar os vetores representando os quatro cantos de cada retângulo;
    #   2.1. Proj.AUR/Axis = (A.UpRight * Axis / ||Axis||^2)*Axis.(x, y)
    #   --- Para X da projeção:
    #   2.2. A.UpRight * Axis = A.UpRight.x * Axis.x + A.UpRight.y * Axis.y
    #   2.3. ||Axis||^2 = Axis.x^2 + Axis.y^2
    #   2.4. Axis = Axis.x
    #   --- Para Y da projeção:
    #   2.2. A.UpRight * Axis = A.UpRight.x * Axis.x + A.UpRight.y * Axis.y
    #   2.3. ||Axis||^2 = Axis.x^2 + Axis.y^2
    #   2.4. Axis = Axis.y
    #
    # 3. Calcular os valores escalares;
    #   3.1. Val.Escalar.(Ponto p) = P.x * Axis.x + P.y + Axis.y
    #
    # 4. Verificar os maiores e menores valores escalares de cada retângulo;
    #
    # 5. Condicional da colisão.
    #
    #--------------------------------------------------------------------------

    def val_escalar(self, point, axis_vector):
        # print(point)
        # print("val_escalar - rect_b => "+str(axis_vector))
        return point.x * axis_vector.x + point.y * axis_vector.y

    def intersects_side(self, axis_vector, rect_b):
        # Retângulo A
        # print("intersects_side - rect_b => "+str(rect_b))
        val_escalar11 = self.val_escalar(self.upleft(), axis_vector)
        val_escalar12 = self.val_escalar(self.upright(), axis_vector)
        val_escalar13 = self.val_escalar(self.bottomleft(), axis_vector)
        val_escalar14 = self.val_escalar(self.bottomright(), axis_vector)
        # Retângulo B
        val_escalar21 = self.val_escalar(rect_b.upleft(), axis_vector)
        val_escalar22 = self.val_escalar(rect_b.upright(), axis_vector)
        val_escalar23 = self.val_escalar(rect_b.bottomleft(), axis_vector)
        val_escalar24 = self.val_escalar(rect_b.bottomright(), axis_vector)
        # Vetorização:
        min_a = min(val_escalar11, val_escalar12, val_escalar13, val_escalar14)
        min_b = min(val_escalar21, val_escalar22, val_escalar23, val_escalar24)
        max_a = max(val_escalar11, val_escalar12, val_escalar13, val_escalar14)
        max_b = max(val_escalar21, val_escalar22, val_escalar23, val_escalar24)
        return min_b <= max_a or max_b <= min_a

    def intersects(self, rect_b):
        side1 = (self.upright() - self.upleft())
        side2 = (self.upleft() - self.bottomleft())
        side3 = (self.bottomleft() - self.bottomright())
        side4 = (self.bottomright() - self.upright())
        return (self.intersects_side(side1, rect_b) and
                self.intersects_side(side2, rect_b) and
                self.intersects_side(side3, rect_b) and
                self.intersects_side(side4, rect_b))
        #----------------------------------------------------------------------
        # axis = self.upright() - self.upleft();
        # proj_aur_axis = (self.upright() * axis / axis**2)*axis
        # val_escalar =
        #----------------------------------------------------------------------
        # return not ((self.right < rect.left) or
        #             (self.left > rect.right) or
        #             (self.top > rect.bottom) or
        #             (self.bottom < rect.top))

    def rotated_point(self, point):
        cx = self.left + self.width()/2
        cy = self.top + self.height()/2
        dx = (point.x - cx)
        dy = (point.y - cy)
        angle = radial(self.angle)
        x = dx * math.cos(angle) - dy * math.sin(angle)
        y = dx * math.sin(angle) + dy * math.cos(angle)
        return Point(x+cx, y+cy)

    def upright(self):
        return self.rotated_point(Point(self.right, self.top))

    def upleft(self):
        return self.rotated_point(Point(self.left, self.top))

    def bottomleft(self):
        return self.rotated_point(Point(self.left, self.bottom))

    def bottomright(self):
        return self.rotated_point(Point(self.right, self.bottom))

    def width(self):
        return self.right - self.left

    def height(self):
        return self.bottom - self.top


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
        #if (self.angle != 0): print("trueXY = ("+str(trueX)+", "+str(trueY)+")")
        glTranslatef(trueX, trueY, 0)
        glRotatef(-self.angle, 0, 0, 1)
        self.bitmap.blit(-self.ox*window.x_proportion,
                         -self.oy*window.y_proportion,
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
            super(SpaceObject, self).__init__('img/stronda_okay.png')
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
