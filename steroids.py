# Imports
import pyglet
from pyglet import clock
import game


#-----------------------------------------------------------------------------
# Material para estruturação do jogo
#-----------------------------------------------------------------------------

fps_display = clock.ClockDisplay()

class Window(pyglet.window.Window):
    def on_draw(self):
        self.clear()
        fps_display.draw()

    def on_close(self):
        self.close()
        exit(0)

class SoundManager:
    def __init__(self):
        self.player = pyglet.media.Player()

    def play(self, resource):
        self.player.next()
        self.player.queue(resource)
        self.player.play()

#-----------------------------------------------------------------------------
# Processo principal do jogo
#-----------------------------------------------------------------------------

# 1 - Criação da janela de jogo
window = Window(game.SIZE[0], game.SIZE[1])
window.set_caption(game.TITLE)
window.set_mouse_visible(False)

# 2 - Instanciação do que for necessário (elementos globais)
music_player = SoundManager()

# 3 - Definição das configurações principais
clock.set_fps_limit(game.FPS)

# 4 - Definição do loop principal
while 1:
    pyglet.clock.tick()

    for window in pyglet.app.windows:
        window.switch_to()
        window.dispatch_events()
        window.dispatch_event('on_draw')0
====================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================


+========7        window.flip
        window.set_caption(game.TITLE + " - " + str(int(clock.get_fps()))+" FPS")

    game.frame_count += 1
