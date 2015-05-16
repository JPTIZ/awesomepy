# Imports externos
import pyglet
from pyglet import clock
from pyglet.gl import *
from pyglet.window import key
import math
# Imports internos
import game
from game import keys
from game import Rect
from game import Sprite
from game import Window
from game import SpaceObject
from game import SoundManager
from game import SpaceObjectType
from game import radial
from game import Point

pyglet.options['audio'] = ('directsound', 'alsa', 'openal', 'silent')

# -----------------------------------------------------------------------------
# Cenas do jogo
# -----------------------------------------------------------------------------


class SceneTitle(game.SceneBase):
    # Tela de título
    def __init__(self):
        self.background = Sprite('img/titleBackground.png')
        self.logo = Sprite('img/steroidsLogo.png')
        self.logo.x = 20
        self.logo.y = 20
        self.pressStart = Sprite('img/pressStart.png')
        self.pressStart.x = 320-(self.pressStart.bitmap.width/2)
        self.pressStart.y = 320
        self.fadeTime = 30
        music_player.play(pyglet.media.load('bgm/title.mp3'))

    def update(self):
        self.background.update(window)
        self.logo.update(window)
        self.pressStart.update(window)
        if self.fadeTime == 0:
            game.scene = SceneStage1()
        if self.fadeTime < 30:
            self.fadeTime -= 1
            #print("Remaining fade delay: "+str(self.fadeTime))
            if self.fadeTime % 5 == 0:
                self.pressStart.visible = not self.pressStart.visible

    def on_key_press(self, symbol, modifiers):
        print("Pressou tecla!")
        if symbol == key.RETURN and self.fadeTime >= 30:
            self.fadeTime -= 1
            pyglet.media.load('snd/confirm2.wav', streaming=False).play()


class SceneStage1(game.SceneBase):
    # Primeiro estágio
    def __init__(self):
        self.background = Sprite('img/titleBackground.png')
        self.player = Sprite('img/player.png')
        self.player.x = 320
        self.player.y = 240
        self.player.ox = self.player.bitmap.width/2
        self.player.oy = self.player.bitmap.height/2
        self.player_speed = 5
        self.steroid = SpaceObject(0, 0, SpaceObjectType.asteroid, 2, 2)
        self.steroid.ox = self.steroid.width/2
        self.steroid.oy = self.steroid.height/2
        self.steroid.angle = 45
        self.player_life = 640
        music_player.play(pyglet.media.load('bgm/stage1.mp3'))
        print("Iniciou primeiro estágio")

    def update(self):
        pass
        spd = self.player_speed
        if str(key.RIGHT) in keys:
            self.player.angle += spd
        if str(key.LEFT) in keys:
            self.player.angle -= spd
        if str(key.UP) in keys:
            self.player.x -= spd*math.sin(-radial(self.player.angle))
            self.player.y -= spd*math.cos(-radial(self.player.angle))
        if str(key.DOWN) in keys:
            self.player.x += spd*math.sin(-radial(self.player.angle))
            self.player.y += spd*math.cos(-radial(self.player.angle))
        if str(key.Y) in keys:
            self.player_life = 640
        self.background.update(window)
        self.player.update(window);
        # Checa interseção do jogador com o asteróide
        r1 = Rect(self.player.x,
             self.player.y,
             self.player.x + self.player.width,
             self.player.y + self.player.height,
             self.player.angle)
        r2 = Rect(self.steroid.x - self.steroid.width/2,
             self.steroid.y + self.steroid.height/2,
             self.steroid.x + self.steroid.width,
             self.steroid.y + self.steroid.height,
             self.steroid.angle)
        # p1_1 = r1.upleft()      + Point(-self.player.ox, self.player.oy)
        # p1_2 = r1.bottomleft()  + Point(-self.player.ox, self.player.oy)
        # p1_3 = r1.bottomright() + Point(-self.player.ox, self.player.oy)
        # p1_4 = r1.upright()     + Point(-self.player.ox, self.player.oy)
        # p2_1 = r2.upleft()      + Point(-self.steroid.ox, self.steroid.oy)
        # p2_2 = r2.bottomleft()  + Point(-self.steroid.ox, self.steroid.oy)
        # p2_3 = r2.bottomright() + Point(-self.steroid.ox, self.steroid.oy)
        # p2_4 = r2.upright()     + Point(-self.steroid.ox, self.steroid.oy)
        # pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
        #     ('v2f',
        #         (
        #             p1_1.x*window.x_proportion, (480.0 - p1_1.y)*window.y_proportion,
        #             p1_2.x*window.x_proportion, (480.0 - p1_2.y)*window.y_proportion,
        #             p1_3.x*window.x_proportion, (480.0 - p1_3.y)*window.y_proportion,
        #             p1_4.x*window.x_proportion, (480.0 - p1_4.y)*window.y_proportion
        #         )
        #     ),
        #     ('c3B',
        #         (
        #             255, 0, 0,
        #             0, 250, 0,
        #             0, 0, 250,
        #             255, 0, 250
        #         )
        #     )
        # )
        # pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
        #     ('v2f',
        #         (
        #             p2_1.x*window.x_proportion, (480.0 - p2_1.y)*window.y_proportion,
        #             p2_2.x*window.x_proportion, (480.0 - p2_2.y)*window.y_proportion,
        #             p2_3.x*window.x_proportion, (480.0 - p2_3.y)*window.y_proportion,
        #             p2_4.x*window.x_proportion, (480.0 - p2_4.y)*window.y_proportion
        #         )
        #     ),
        #     ('c3B',
        #         (
        #             0, 0, 255,
        #             0, 0, 255,
        #             0, 0, 255,
        #             0, 0, 255
        #         )
        #     )
        # )
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
            ('v2f',
                (
                    0, 480,
                    self.player_life, 480,
                    self.player_life, 480-32,
                    0, 480-32

                )
            ),
            ('c3B',
                (
                    0, 0, 255,
                    0, 0, 255,
                    0, 0, 128,
                    0, 0, 128
                )
            )
        )
        if r1.intersects(r2):
           self.steroid.on_collide_with_player()
           self.player_life -= 10
        self.steroid.angle += 5
        self.steroid.update(window)

    def on_key_press(self, symbol, modifiers):
        pass

# -----------------------------------------------------------------------------
# Processo principal do jogo
# -----------------------------------------------------------------------------

# 1 - Criação da janela de jogo
window = Window(width=game.SIZE[0], height=game.SIZE[1], resizable=True)
window.set_caption(game.TITLE + " - Initializing...")
window.set_mouse_visible(False)

# 2 - Instanciação do que for necessário (elementos globais)
music_player = SoundManager()                       # Tocador de músicas
game.scene = SceneTitle()                           # Cena inicial do jogo

# 3 - Definição das configurações principais
clock.set_fps_limit(game.FPS)
glEnable(GL_BLEND)                                  # Habilitar canal alpha #1
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)   # Habilitar canal alpha #2

# 4 - Definição do loop principal
while 1:
    pyglet.clock.tick()

    for window in pyglet.app.windows:
        window.switch_to()
        window.dispatch_events()
        game.scene.update()  # Atualização principal da cena atual do jogo
        window.dispatch_event('on_draw')
        window.flip()
        window.set_caption(game.TITLE + " - " +
                           str(int(clock.get_fps()))+" FPS")

    game.frame_count += 1
