import pyglet
from pyglet.window import mouse
from pyglet.window import key

window = pyglet.window.Window()
window.set_caption("Pau frito")
window.set_size(640, 480)
window.set_mouse_visible(False)

# Soh declarando azibagem
image = pyglet.image.load('img/xicrinha.jpg')
image.opacity = .5
image.x = 320 - image.width/2
image.y = 240 - image.height/2
image2 = pyglet.image.load('img/frame.PNG')

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
	if symbol == key.LEFT: image.x += 10

# Tudo funciona ok
# soh que a droga do pyglet considera o canto esquerdo-abaixo como ponto
@window.event
def on_draw():
	window.clear()
	image2.blit(320 - image2.width/2, 240-image2.height/2)
	image.blit(image.x, image.y)

# Principalzinho =)
pyglet.app.run()