# Imports externos
import pyglet
from pyglet import clock
from pyglet.gl import *
from pyglet.window import key
# Imports internos
import game
from game import Window
from game import SoundManager
from game import Sprite
from game import keys

pyglet.options['audio'] = ('alsa', 'openal', 'silent')

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
        self.fadeTime = 120
        music_player.play(pyglet.media.load('bgm/title.mp3'))

    def update(self):
        self.background.update(window)
        self.logo.update(window)
        self.pressStart.update(window)
        if self.fadeTime == 0:
            game.scene = SceneStage1()
        if self.fadeTime < 120:
            self.fadeTime -= 1
            print("Remaining fade delay: "+str(self.fadeTime))
            if self.fadeTime % 5 == 0:
                self.pressStart.visible = not self.pressStart.visible

    def on_key_press(self, symbol, modifiers):
        print("Pressou tecla!")
        if symbol == key.RETURN and self.fadeTime >= 120:
            self.fadeTime -= 1
            pyglet.media.load('snd/confirm.wav', streaming=False).play()


class SceneStage1(game.SceneBase):
    # Primeiro estágio
    def __init__(self):
        self.background = Sprite('img/titleBackground.png')
        self.player = Sprite('img/player.png')
        music_player.play(pyglet.media.load('bgm/stage1.mp3'))
        print("Iniciou primeiro estágio")

    def update(self):
        if str(key.RIGHT) in keys:
            self.player.angle += 1
        if str(key.LEFT) in keys:
            self.player.angle -= 1
        if str(key.UP) in keys:
            self.player.y -= 1
        if str(key.DOWN) in keys:
            self.player.y += 1
        self.background.update(window)
        self.player.update(window)

    def on_key_press(self, symbol, modifiers):
        print("Pressou teclinha")
        if symbol == key.RIGHT:
            self.player.x += 1
        if symbol == key.LEFT:
            self.player.x -= 1
        if symbol == key.UP:
            self.player.y -= 1
        if symbol == key.DOWN:
            self.player.y += 1

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
