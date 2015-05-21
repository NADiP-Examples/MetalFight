import random
import math

from livewires import games, color


games.init(screen_width=1200, screen_height=600, fps=60)


class Wrapper(games.Sprite):
    def update(self):

        if self.top > games.screen.height:
            self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height

        if self.left > games.screen.width:
            self.right = 0

        if self.right < 0:
            self.left = games.screen.width

    def die(self):
        self.destroy()


class Collider1(games.Sprite):
    def update(self):
        super(Collider1, self).update()
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()


class Collider2(Wrapper):
    def update(self):
        super(Collider2, self).update()
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                HP1.value = HP1.value - 1
                if HP1.value <= 0:
                    self.die()


class Collider3(Wrapper):
    def update(self):
        super(Collider3, self).update()
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                HP2.value = HP2.value - 1
                if HP2.value <= 0:
                    self.die()


class Asteroid(Wrapper):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    SPAWN = 2
    images = {SMALL: games.load_image("modelasteroid2.gif"), MEDIUM: games.load_image("modelasteroid3.gif"),
              LARGE: games.load_image("modelasteroid1.jpg")}
    SPEED = 1

    def __init__(self, x, y, size):
        super(Asteroid, self).__init__(image=Asteroid.images[size], x=x, y=y,
                                       dx=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size,
                                       dy=random.choice([1, -1]) * Asteroid.SPEED * random.random() / size)
        self.size = size

    def die(self):
        if self.size != Asteroid.SMALL:
            for i in range(Asteroid.SPAWN):
                new_asteroid = Asteroid(x=self.x, y=self.y, size=self.size - 1)
                games.screen.add(new_asteroid)
        new_explosion = Explosion(x=self.x, y=self.y)
        games.screen.add(new_explosion)
        super(Asteroid, self).die()


class Missile(Collider1):
    image = games.load_image("missile.jpg")
    sound = games.load_sound("missile.wav")
    BUFFER = 80
    VELOCITY_FACTOR = 10
    LIFEТIME = 150

    def __init__(self, ship_x, ship_y, ship_angle):
        Missile.sound.play()
        angle = ship_angle * math.pi / 180
        buffer_x = Missile.BUFFER * math.sin(angle)
        buffer_y = Missile.BUFFER * -math.cos(angle)
        x = ship_x + buffer_x
        y = ship_y + buffer_y
        dx = Missile.VELOCITY_FACTOR * math.sin(angle)
        dy = Missile.VELOCITY_FACTOR * -math.cos(angle)
        super(Missile, self).__init__(image=Missile.image, x=x, y=y, dx=dx, dy=dy)
        self.lifetime = Missile.LIFEТIME

    def update(self):
        super(Missile, self).update()
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()
        if self.top > games.screen.height:
            self.destroy()

        if self.bottom < 0:
            self.destroy()

        if self.left > games.screen.width:
            self.destroy()

        if self.right < 0:
            self.destroy()

    def die(self):
        self.destroy()


class Ship(Collider2):
    model1 = games.load_image("little.gif")
    model2 = games.load_image("little2.gif")
    model3 = games.load_image("little3.gif")
    model4 = games.load_image("little4.gif")
    model5 = games.load_image("little5.gif")
    model6 = games.load_image("little6.gif")
    model7 = games.load_image("little7.gif")
    image = random.choice([model1, model2, model3, model4, model5, model6, model7])
    ROTATION_STEP = 2
    VELOCITY_STEP = .05
    MISSILE_DELAY = 180
    VELOCITY_MAX = 3

    def __init__(self, x, y):
        super(Ship, self).__init__(image=Ship.image, x=x, y=y)
        self.missile_wait = 0

    def update(self):
        super(Ship, self).update()
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Ship.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Ship.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_UP):
            angle = self.angle * math.pi / 180
            self.dx += Ship.VELOCITY_STEP * math.sin(angle)
            self.dy += Ship.VELOCITY_STEP * -math.cos(angle)
            self.dx = min(max(self.dx, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)
            self.dy = min(max(self.dy, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)
        if games.keyboard.is_pressed(games.K_DOWN):
            angle = self.angle * math.pi / 180
            self.dx -= Ship.VELOCITY_STEP * math.sin(angle)
            self.dy -= Ship.VELOCITY_STEP * -math.cos(angle)
            self.dx = min(max(self.dx, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)
            self.dy = min(max(self.dy, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)
        if self.missile_wait > 0:
            self.missile_wait -= 1
        if games.keyboard.is_pressed(games.K_RCTRL) and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)
            self.missile_wait = Ship.MISSILE_DELAY

    def die(self):
        new_explosion = Explosion(x=self.x, y=self.y)
        games.screen.add(new_explosion)
        games.screen.add(end_message1)
        HP1.value = 0
        self.destroy()


class Ship1(Collider3):
    model1 = games.load_image("little.gif")
    model2 = games.load_image("little2.gif")
    model3 = games.load_image("little3.gif")
    model4 = games.load_image("little4.gif")
    model5 = games.load_image("little5.gif")
    model6 = games.load_image("little6.gif")
    model7 = games.load_image("little7.gif")
    image = random.choice([model1, model2, model3, model4, model5, model6, model7])
    ROTATION_STEP = 2
    VELOCITY_STEP = .05
    MISSILE_DELAY = 180
    VELOCITY_MAX = 3

    def __init__(self, x, y):
        super(Ship1, self).__init__(image=Ship1.image, x=x, y=y)
        self.missile_wait = 0

    def update(self):
        super(Ship1, self).update()
        if games.keyboard.is_pressed(games.K_a):
            self.angle -= Ship.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_d):
            self.angle += Ship.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_w):
            angle = self.angle * math.pi / 180
            self.dx += Ship.VELOCITY_STEP * math.sin(angle)
            self.dy += Ship.VELOCITY_STEP * -math.cos(angle)
            self.dx = min(max(self.dx, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)
            self.dy = min(max(self.dy, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)
        if games.keyboard.is_pressed(games.K_s):
            angle = self.angle * math.pi / 180
            self.dx -= Ship.VELOCITY_STEP * math.sin(angle)
            self.dy -= Ship.VELOCITY_STEP * -math.cos(angle)
            self.dx = min(max(self.dx, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)
            self.dy = min(max(self.dy, -Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)
        if self.missile_wait > 0:
            self.missile_wait -= 1
        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)
            self.missile_wait = Ship.MISSILE_DELAY

    def die(self):
        new_explosion = Explosion(x=self.x, y=self.y)
        games.screen.add(new_explosion)
        games.screen.add(end_message2)
        HP2.value = 0
        self.destroy()


class Explosion(games.Animation):
    sound = games.load_sound("explosion.wav")
    images = ["explosion1.jpg",
              "explosion2.jpg",
              "explosion3.jpg",
              "explosion4.jpg",
              "explosion5.jpg",
              "explosion6.jpg",
              "explosion7.jpg",
              "explosion8.jpg",
              "explosion9.jpg"]

    def __init__(self, x, y):
        super(Explosion, self).__init__(images=Explosion.images,
                                        x=x, y=y,
                                        repeat_interval=4, n_repeats=1,
                                        is_collideable=False)
        Explosion.sound.play()


class Music(object):
    def play(self):
        games.music.play(-1)


end_message2 = games.Message(value="Игрок 2 победил!",
                             size=90,
                             color=color.red,
                             x=games.screen.width / 2,
                             y=games.screen.height / 2,
                             lifetime=5 * games.screen.fps,
                             after_death=games.screen.quit,
                             is_collideable=False)
end_message1 = games.Message(value="Игрок 1 победил!",
                             size=90,
                             color=color.red,
                             x=games.screen.width / 2,
                             y=games.screen.height / 2,
                             lifetime=5 * games.screen.fps,
                             after_death=games.screen.quit,
                             is_collideable=False)
name = games.Message(value="Metal Fight!",
                     size=60,
                     color=color.yellow,
                     x=games.screen.width / 2,
                     y=70,
                     lifetime=5 * games.screen.fps,
                     is_collideable=False)
HP1 = games.Text(value=1000,
                 size=60,
                 color=color.white,
                 x=1100,
                 y=30,
                 is_collideable=False)
HP2 = games.Text(value=1000,
                 size=60,
                 color=color.white,
                 x=100,
                 y=30,
                 is_collideable=False)
control1 = games.load_image("control1.jpg")
cont1 = games.Sprite(image=control1, x=1125, y=535, is_collideable=False)
control2 = games.load_image("control2.jpg")
cont2 = games.Sprite(image=control2, x=75, y=535, is_collideable=False)


def main():
    wall_image1 = games.load_image("background1.jpg", transparent=False)
    wall_image2 = games.load_image("background2.jpg", transparent=False)
    wall_image3 = games.load_image("background3.jpg", transparent=False)
    wall_image4 = games.load_image("background4.jpg", transparent=False)
    wall_image5 = games.load_image("background5.jpg", transparent=False)
    games.screen.background = random.choice([wall_image1, wall_image2, wall_image3, wall_image4, wall_image5])
    games.music.load("maintheme.mp3")

    for i in range(20):
        x = random.randint(400, 800)
        y = random.randint(0, games.screen.height)
        size = random.choice([Asteroid.SMALL, Asteroid.MEDIUM, Asteroid.LARGE])
        new_asteroid = Asteroid(x=x, y=y, size=size)
        games.screen.add(new_asteroid)

    the_ship = Ship(x=1000, y=games.screen.height / 2)
    games.screen.add(the_ship)

    the_ship1 = Ship1(x=200, y=games.screen.height / 2)
    games.screen.add(the_ship1)

    games.screen.add(cont1)
    games.screen.add(cont2)

    games.screen.add(HP1)
    games.screen.add(HP2)
    games.screen.add(name)

    metalfight = Music()
    metalfight.play()

    games.mouse.is_visible = False
    games.screen.event_grab = True
    games.screen.mainloop()


main()