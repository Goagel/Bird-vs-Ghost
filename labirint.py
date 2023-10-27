from pygame import *
from pygame import mixer
from PyQt5.QtCore import Qt, QTimer, QTime, QLocale
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QFont
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QHBoxLayout, QVBoxLayout, QGridLayout, 
        QGroupBox, QRadioButton,
        QPushButton, QLabel, QListWidget, QLineEdit)
mixer.init()

mixer.music.load('shot.wav')
#mixer.music2.load('pixel.death.mp3')
#Set preferred volume
mixer.music.set_volume(0.2)
death_sound = mixer.Sound('death1.wav')
win_sound = mixer.Sound('win.wav')
game_over = mixer.Sound('game.over.wav')

#parent class for other sprites
class GameSprite(sprite.Sprite):
  # class constructor
  def __init__(self, player_image, player_x, player_y, size_x, size_y):
      # Calling the class constructor (Sprite):
      sprite.Sprite.__init__(self)
 
      # each sprite must store an image property
      self.image = transform.scale(image.load(player_image), (size_x, size_y))

      # each sprite must store the property rect - the rectangle in which it is inscribed
      self.rect = self.image.get_rect()
      self.rect.x = player_x
      self.rect.y = player_y
 
  # method that draws the hero on the window
  def reset(self):
      window.blit(self.image, (self.rect.x, self.rect.y))

#main player class
class Player(GameSprite):
  #a method that implements sprite control by keyboard arrow buttons
  def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
      # Calling the class constructor (Sprite):
      GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)

      self.x_speed = player_x_speed
      self.y_speed = player_y_speed
      self.flipped = False
  def update(self):
       ''' moves the character using the current horizontal and vertical speed'''
       # first move horizontally
       if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
         self.rect.x += self.x_speed
       # if we went behind the wall, then we will stand close to the wall
       platforms_touched = sprite.spritecollide(self, barriers, False)
       if self.x_speed > 0: # go to the right, the right edge of the character is close to the left edge of the wall
           for p in platforms_touched:
               self.rect.right = min(self.rect.right, p.rect.left) 
       elif self.x_speed < 0: # go to the left, put the left edge of the character close to the right edge of the wall
           for p in platforms_touched:
               self.rect.left = max(self.rect.left, p.rect.right) # if several walls are touched, then the left edge is the maximum
       if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
         self.rect.y += self.y_speed
       # if we went behind the wall, then we will stand close to the wall
       platforms_touched = sprite.spritecollide(self, barriers, False)
       if self.y_speed > 0: # go down
           for p in platforms_touched:
               self.y_speed = 0
               # Check which of the platforms from the bottom is the highest, align with it, remember it as our support:
               if p.rect.top < self.rect.bottom:
                   self.rect.bottom = p.rect.top
       elif self.y_speed < 0: # go up
           for p in platforms_touched:
               self.y_speed = 0  # when colliding with a wall, the vertical speed is extinguished
               self.rect.top = max(self.rect.top, p.rect.bottom) # align the top edge with the bottom edges of the walls that were run over
       if self.x_speed < 0 and not self.flipped:
           self.image = transform.flip(self.image, True, False)
           self.flipped = True
       elif self.x_speed > 0 and self.flipped:
           self.image = transform.flip(self.image, True, False)
           self.flipped = False


 
 
 
  # method "shot" (use the player's place to create a bullet there)
  def fire(self):
      bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 55, 40, 30)
      bullets.add(bullet)

#sprite-enemy class
class Enemy(GameSprite):
  side = "left"
  def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
      # Call the class constructor (Sprite):
      GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
      self.speed = player_speed
      self.flipped = False
   #movement of the enemy
  def update(self):
      if self.rect.x <= 600: 
          self.side = "right"
          self.image = transform.flip(self.image, True, False)
          self.flipped = True
      if self.rect.x >= win_width - 85:
          self.side = "left"
          self.image = transform.flip(self.image, True, False)
          self.flipped = False
      if self.side == "left":
          self.rect.x -= self.speed
      else:
          self.rect.x += self.speed
    


# bullet sprite class  
class Bullet(GameSprite):
  def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
      # Call the class constructor (Sprite):
      GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y) 
      self.speed = player_speed
  # enemy movement
  def update(self):
      self.rect.x += self.speed
      # disappears when it reaches the edge of the screen
      if self.rect.x > win_width+10:
          self.kill()

#Creating window
win_width = 1400
win_height = 800
display.set_caption("Bird vs Ghost")
window = display.set_mode((win_width, win_height))
#back = image.load('back.jpg')
back = image.load('back.jpg')
#window.blit(transform.scale(back, (win_width, win_height)), (0, 0))
#create a group for the walls
barriers = sprite.Group()

# create a group for bullets
bullets = sprite.Group()

#create a group for monsters
monsters = sprite.Group()

#create wall pictures
w1 = GameSprite('platform2.png',win_width / 2 - win_width / 2.9, win_height / 100, 220, 50)
w2 = GameSprite('platform2_v.png', 140, 400, 70, 400)
w3 = GameSprite('platform2_v.png', 140, 150, 70, 250)
w4 = GameSprite('platform2.png',win_width / 2 - win_width / 2, win_height / 100, 220, 50)
w5 = GameSprite('platform2_v.png', 360, 60, 70, 340)
w6 = GameSprite('platform2_v.png', 360, 400, 70, 280)
w7 = GameSprite('platform2.png',win_width / 2 - win_width / 5.2, win_height / 100, 220, 50)
w8 = GameSprite('platform2.png',win_width / 2 - win_width /26, win_height / 100, 220, 50)
w9 = GameSprite('platform2_v.png', 580, 400, 70, 400)
w10 = GameSprite('platform2_v.png', 580, 150, 70, 250)


# add walls to the group
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
barriers.add(w7)
barriers.add(w8)
barriers.add(w9)
barriers.add(w10)
# create sprites
packman = Player('pac-10.png', 5, win_height - 90, 90, 90, 0, 5)
monster2 = Enemy('cyborg.png', win_width - 80, 285, 140, 130, 14)
monster3 = Enemy('cyborg.png', win_width - 80, 190, 140, 130, 7)
monster = Enemy('cyborg.png', win_width - 80, 380, 140, 130, 7)
monster4 = Enemy('cyborg.png', win_width - 80, 475, 140, 130, 14)
monster5 = Enemy('cyborg.png', win_width - 80, 570, 140, 130, 7)
final_sprite = GameSprite('pac-1.png', win_width - 85, win_height - 100, 80, 80)

#add a monster to the group
monsters.add(monster)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)
# variable responsible for how the game ended
finish = False
#game loop
run = True
while run:
  #loop runs every 0.05 seconds
  time.delay(50)
   #iterate through all the events that could have happened
  for e in event.get():
       if e.type == QUIT:
           run = False
       elif e.type == KEYDOWN:
           if e.key == K_LEFT:
               packman.x_speed = -20
           elif e.key == K_RIGHT:
               packman.x_speed = 20
           elif e.key == K_UP:
               packman.y_speed = -20
           elif e.key == K_DOWN:
               packman.y_speed = 20
           elif e.key == K_SPACE:
              packman.fire()
              mixer.music.play()

       elif e.type == KEYUP:
           if e.key == K_LEFT:
               packman.x_speed = 0
           elif e.key == K_RIGHT:
               packman.x_speed = 0 
           elif e.key == K_UP:
               packman.y_speed = 0
           elif e.key == K_DOWN:
               packman.y_speed = 0

#check if the game is not finished yet
  if not finish:
      #update the background every iteration
      #window.fill((back))
      window.blit(transform.scale(back, (win_width, win_height)), (0, 0))
      # start sprite movements
      packman.update()
      bullets.update()

       #update them in a new location on each iteration of the loop
      packman.reset()
      #drawing walls 2
      #w1.reset()
      #w2.reset()
      bullets.draw(window)
      barriers.draw(window)
      final_sprite.reset()

      if sprite.groupcollide(monsters, bullets, True, True):
        death_sound.play()
      monsters.update()
      monsters.draw(window)
      sprite.groupcollide(bullets, barriers, True, False)

      #Checking the hero's collision with the enemy and walls
      if sprite.spritecollide(packman, monsters, False):
          game_over.play()
          finish = True
          #calculate ratio
          img = image.load('game-over_1.jpg')
          window.fill((255, 255, 255))
          window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

      if sprite.collide_rect(packman, final_sprite):
          win_sound.play()
          finish = True
          img = image.load('thumb.jpg')
          window.fill((255, 255, 255))
          window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
 
  display.update()