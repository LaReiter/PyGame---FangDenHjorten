# -*- coding: utf-8 -*- 

### Lars Nørtoft Reiter (Lars Reiter Nielsen)
### Creation date: 2013
### Title: Fang den Hjorten

# THINGS TO FIX:
# player.update() removed from game-loop (check to see if it influences)

import pygame, os
from random import shuffle,randint

pygame.init()


# colors
grey = (192,192,192)
white = (255,255,255)
blue = (0,0,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)


### ENVIRONMENT CLASS

class Enviroment(pygame.sprite.Sprite):
    
    def __init__(self,filename):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image(filename,-1)

### BUSH CLASS

class Bush(pygame.sprite.Sprite):
    
    def __init__(self,row,column):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image('bush.png',-1)
        self.rect = pygame.Rect(row * 35, column * 35,30,30)

### PLAYER CLASS

class Player(pygame.sprite.Sprite):
    
    # player direction
    direction = 'down'
    
    # This is a frame counter used to determing which image to draw
    frame = 0
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        for i in range (1,11):
            img = pygame.image.load("player"+str(i)+".png").convert()
            img.set_colorkey(white)
            self.images.append(img)
    
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = 10, 10  # 10, 10 default
        
    def move(self, dx, dy):
        
        if dx != 0 or dy != 0:
            self.moveit(dx,dy)
        
    
    def moveit(self,dx,dy):

        if (self.rect.x + dx) >= 0 and (self.rect.x + dx) <= 968 and (self.rect.y + dy) >= 0 and (self.rect.y + dy) <= 758:
            self.rect.x += dx
            self.rect.y += dy
        
        # If we are moving down
        if dy > 0:
           
            # Update our frame counter
            self.frame += 1
            self.direction = 'down'
        
            # We go from 0...3. If we are above image 3, reset to 0
            # Multiply by 4 because we flip the image every 4 frames        
            if self.frame > 2*4:
                self.frame = 0
            
            # Grab the image, do floor division by 4 because we flip
            # every 4 frames.
            # Frames 0...3 -> image[0]
            # Frames 4...7 -> image[1]
            # etc.
            self.image = self.images[self.frame//4]
        
        # Moving up. About the same as before, but use
        # images 4...7 instead of 0...3. Note that we add 4 in the last
        # line to do this.        
        
        if dy < 0:
            self.frame += 1
            self.direction = 'up'
            if self.frame > 2*4:
                self.frame = 0
            self.image = self.images[self.frame//4+3]
        
        # Moving right    
        if dx > 0:
            self.direction = 'right'
            self.frame += 1
            if self.frame > 1*4:
                self.frame = 0
            self.image = self.images[self.frame//4+6]
        
        # Moving left
        if dx < 0:
            self.direction = 'left'
            self.frame += 1
            if self.frame > 1*4:
                self.frame = 0
            self.image = self.images[self.frame//4+8]
        
        for bush in bush_sprites:
            if self.rect.colliderect(bush.rect):
                tree_sound.play()
                if dx > 0:
                    self.rect.right = bush.rect.left
                if dx < 0:
                    self.rect.left = bush.rect.right
                if dy > 0:
                    self.rect.bottom = bush.rect.top
                if dy < 0:
                    self.rect.top = bush.rect.bottom
        
        for env in env_sprites:
            if self.rect.colliderect(env.rect):
                if dx > 0:
                    self.rect.right = env.rect.left
                if dx < 0:
                    self.rect.left = env.rect.right
                if dy > 0:
                    self.rect.bottom = env.rect.top
                if dy < 0:
                    self.rect.top = env.rect.bottom
                    
    def interaction(self):
        
        discovery_font = pygame.font.Font(None, 28)
        alfa = 0
        
        for person in env_sprites:
            if (person.rect.x - self.rect.x) < 20 and abs(person.rect.y - self.rect.y) <= 5 and self.direction == 'right':
                position = self.pos()
                if position == (12,9):
                    if persons['ml'] != 1:
                        message_rect = pygame.Rect(385,12, 185, 20)
                        pygame.draw.rect(screen,black,(380,10,200,25))
                        pygame.draw.rect(screen,red,(380,10,200,25),2)
                        while alfa < 255:
                            message = discovery_font.render('Marie-Louise fundet!',1,(alfa,0,255-alfa))
                            screen.blit(message, message_rect)
                            pygame.display.update(pygame.Rect(380,10,200,25))
                            alfa += 17
                            pygame.time.delay(500)
                        persons['ml'] = 1
                elif position == (16,13):
                    if persons['ingrid'] != 1:
                        message_rect = pygame.Rect(385,12, 185, 20)
                        pygame.draw.rect(screen,black,(380,10,150,25))
                        pygame.draw.rect(screen,red,(380,10,150,25),2)
                        while alfa < 255:
                            message = discovery_font.render('Ingrid fundet!',1,(alfa,0,255-alfa))
                            screen.blit(message, message_rect)
                            pygame.display.update(pygame.Rect(380,10,150,25))
                            alfa += 17
                            pygame.time.delay(500)                   
                        persons['ingrid'] = 1
                elif position == (26,1):
                    if persons['vibeke'] != 1:
                        message_rect = pygame.Rect(385,12, 185, 20)
                        pygame.draw.rect(screen,black,(380,10,160,25))
                        pygame.draw.rect(screen,red,(380,10,160,25),2)
                        while alfa < 255:
                            message = discovery_font.render('Vibeke fundet!',1,(alfa,0,255-alfa))
                            screen.blit(message, message_rect)
                            pygame.display.update(pygame.Rect(380,10,160,25))
                            alfa += 17
                            pygame.time.delay(500)                      
                        persons['vibeke'] = 1
    
    def pos(self):
        return self.rect.x // (30 + margin), self.rect.y // (30 + margin)    


# Hjort class 
class Hjort(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('hjorten.png',-1)
        
        # FIX: Ensure the image is properly converted for transformations
        if self.image.get_flags() & pygame.SRCALPHA:
            self.image = self.image.convert_alpha()
        else:
            self.image = self.image.convert()
            
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = (423,100)
        self.home_center = self.rect.center  # store the "home" center for shaking

        self.image_alt, _ =  load_image('burning_hjort.png', -1)
        self.image_defeat, _  = load_image('hjort_defeat.png',-1)
        self.move = 2
        self.dizzy = 0
        self.health = 5          # REMINDER: set hjort health (to 10)
         
    def update(self):
        if self.ball_collide() and self.dizzy:
            self.spin()
        else:
            self.walk()
    
    def walk(self):
        newpos = self.rect.move((self.move, 0))
        if self.rect.left < self.area.left or self.rect.right > self.area.right:
            self.move = -self.move
            newpos = self.rect.move((self.move, 0))
            
            # FIX: Ensure the flipped image is also properly converted
            flipped = pygame.transform.flip(self.image, 1, 0)
            if flipped.get_flags() & pygame.SRCALPHA:
                self.image = flipped.convert_alpha()
            else:
                self.image = flipped.convert()
                
        self.rect = newpos    

    def spin(self):
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
            self.health -= 1
        else:
            rotate = pygame.transform.rotate
            rotated = rotate(self.original, self.dizzy)
            # FIX: Ensure rotated image is properly converted
            if rotated.get_flags() & pygame.SRCALPHA:
                self.image = rotated.convert_alpha()
            else:
                self.image = rotated.convert()
        self.rect = self.image.get_rect(center=center) 
        
    def kicked(self):
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image
    
    def shake(self, magnitude=3):
        """ Shake/jitter the hjort. Call this each frame during your intro/animation loop. """
        dx = randint(-magnitude, magnitude)
        dy = randint(-magnitude, magnitude)
        self.rect.center = (self.home_center[0] + dx,
                            self.home_center[1] + dy)

    def unshake(self):
        """Reset the hjort back to its exact home_center."""
        self.rect.center = self.home_center
        
    def ball_collide(self):
        """ check for ball-'hjort' collision """
        for ball in ball_sprites:
            if self.rect.colliderect(ball.rect):
                ball.image = ball.hitimage
                return True
        return False
        
    def rage(self):
        for i in range(30):
            self.image,self.image_alt = self.image_alt,self.image
            castle_sprites.draw(screen)
            clock.tick(20)
            pygame.display.flip()
    
    def defeat(self):
        self.spin()

class Castle_player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image('C_player.png',-1)
        self.kick_image, self.kick_rect = load_image('C_player_kicking.png',-1)
        self.kicking = False
        self.rect.topleft = (423,600)
        self.ball_on_foot = False
        
    def update(self):
        
        x = pygame.mouse.get_pos()[0]
        self.rect.midtop = (x,self.rect.y)
            
            
    def kick(self):
        
        if not self.kicking:
            self.kicking = True
            self.image, self.original = self.kick_image, self.image
    
    def unkick(self):
        
        self.kicking = False
        self.image = self.original


# class BALL for the CASTLE

class Ball(pygame.sprite.Sprite):
    
    def __init__(self,topleft):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = load_image('fodboldmini.png',-1)
        self.rect.x, self.rect.y = topleft
        self.hitimage, self.hitrect = load_image('fodboldmini_hit.png',-1)
        self.direction = 'down'
        self.stuck = False
        
    def update(self):
        
        if self.rect.y > 775 or self.rect.y < 0:
            ball_sprites.remove(self)
        if self.stuck:
            x = pygame.mouse.get_pos()[0]
            self.rect.midtop = (x,self.rect.y)
        if not self.rect.colliderect(C_player.rect) or (self.rect.top - C_player.rect.top) != 115:
            self.move()
        elif self.rect.colliderect(C_player.rect) and (self.rect.top - C_player.rect.top) == 115 and not C_player.ball_on_foot:
            C_player.ball_on_foot = True
            self.stuck = True
            
        # check to see if player is kicking if ball is on foot and if the CURRENT ball
        # is stuck on the foot (avoids new balls being created and fired back on kick)
        if C_player.kicking and C_player.ball_on_foot:
            if self.stuck:
                self.move(True)
            self.stuck = False
            C_player.ball_on_foot = False            

    
    def move(self,hit=False):
        if hit:
            self.rect.y -= 1
            self.direction = 'up'
        if self.direction == 'up':
            self.rect.y -= 2
        else:
            self.rect.y += 1


### FUNCTIONS

# image load function (neglects background color)
def load_image(path, colorkey=None, force_colorkey=False):
    """
    Load an image and return (Surface, Rect).
    force_colorkey: If True, strip alpha channel and use colorkey instead
    """
    fullname = os.path.join(os.getcwd(), path)
    try:
        img = pygame.image.load(fullname)
    except pygame.error as e:
        print("Cannot load image:", fullname)
        raise SystemExit(e)

    #print(f"Loading {path}: has alpha = {img.get_alpha() is not None}")
    
    # Force colorkey mode even if alpha exists
    if force_colorkey and colorkey is not None:
        img = img.convert()  # Strip alpha channel FIRST
        if colorkey == -1:
            colorkey = img.get_at((0, 0))  # Now this will be RGB only
            #print(f"  → Auto-detected colorkey: {colorkey}")
        #print(f"  → Setting colorkey to: {colorkey}")
        img.set_colorkey(colorkey, pygame.RLEACCEL)
    elif img.get_alpha() is not None:
        img = img.convert_alpha()
        #print(f"  → Using alpha channel")
    else:
        img = img.convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = img.get_at((0, 0))
                #print(f"  → Auto-detected colorkey: {colorkey}")
            #print(f"  → Setting colorkey to: {colorkey}")
            img.set_colorkey(colorkey, pygame.RLEACCEL)
    return img, img.get_rect()

# music load function
def load_music(name):
    class NoneMusic:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneMusic()
    fullname = os.path.join(os.getcwd(), name)
    try:
        music = pygame.mixer.music.load(fullname)
    except pygame.error as message:
        print('Cannot load music:', fullname)
        raise SystemExit(message)
 
# sound load function
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(os.getcwd(), name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', fullname)
        raise SystemExit(message)
    return sound

# map draw function
def draw_map(grid):
    """Draws the appropriate map, consulting the grid-code"""
    pixel_y = 0
    for row in range(22):
        pixel_x = 0
        for column in range(28):
            color = green
            if grid[row][column] == 1:
                screen.blit(road_vert,(pixel_x+margin,pixel_y + margin))
            elif grid[row][column] == 2:
                screen.blit(road_hori,(pixel_x+margin,pixel_y + margin))
            elif grid[row][column] == 3:
                screen.blit(road_tkryds_0,(pixel_x+margin,pixel_y + margin))
            elif grid[row][column] == 4:
                screen.blit(road_tkryds_1,(pixel_x+margin,pixel_y + margin))
            elif grid[row][column] == 5:
                screen.blit(road_tkryds_2,(pixel_x+margin,pixel_y + margin))
            elif grid[row][column] == 6:
                screen.blit(road_lower_right,(pixel_x+margin,pixel_y + margin))
            elif grid[row][column] == 7:
                screen.blit(road_upper_left,(pixel_x+margin,pixel_y + margin))
            elif grid[row][column] == 8:
                screen.blit(road_upper_right,(pixel_x+margin,pixel_y + margin))
            elif grid[row][column] == 9:
                screen.blit(road_lower_left,(pixel_x+margin,pixel_y + margin))
            elif grid[row][column] == 10:
                screen.blit(bush_env,(pixel_x+margin,pixel_y+margin))
            elif grid[row][column] == 11:
                screen.blit(grass_env,(pixel_x+margin,pixel_y+margin))
            pixel_x += width + margin
        pixel_y += height + margin    
    

def fade(unfade=False):
    """flarring rects - screenflip flow animation"""
    grid_rects = []
    for i in range(28):
        for j in range(22):
            grid_rects.append((i*35,j*35,35,35))
    shuffle(grid_rects)
    
    
    if unfade:
        for rect in grid_rects:
            pygame.display.update(rect)
            pygame.time.delay(5)
    else:
        for rect in grid_rects:
            pygame.draw.rect(screen,black,rect)
            pygame.display.flip()





# adjust screen and set icon
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
width,height = 1000,600
screen = pygame.display.set_mode((width,height))

# load music and sound
load_music('boxcat.mp3')
pygame.mixer.music.play(-1,0.0)

# load backgground, aswell as background rect (frame rect) and taskbar icon
background_intro,background_rect = load_image('forrest.jpg')
pygame.display.set_caption('Fang Den Hjorten')

# resize background
background_intro = pygame.transform.scale(background_intro,(1000,600))

# load the ball
ball, ball_rect = load_image('fodbold.png',-1)

# load the stag
hjort,hjort_rect = load_image('hjort.png',-1)

# instruction trigger
instructions = True

# set fontheader and fontstandard
fontObj_start = pygame.font.Font(None,48)
fontObj_start.set_bold(True)
text_start = fontObj_start.render('START',True,green)
fontObj = pygame.font.Font('freesansbold.ttf', 16)
fontObj.set_bold(True)
header = fontObj.render('FANG DEN HJORTEN!', True, green)
fontObj_std = pygame.font.Font(None,20)
text_header = fontObj_std.render('Velkommen til',True,green)


# blinking button
blink = True
blink2 = False

# initialize
done = False
clock = pygame.time.Clock()
BLINKEVENT = pygame.USEREVENT + 1 
pygame.time.set_timer(BLINKEVENT,1000)





# INTRODUCTION-LOOP

while done == False and instructions:
    
    screen.blit(background_intro,(0,0))    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            done = True
        if event.type == BLINKEVENT:
            if blink == True:
                blink = False
            else:
                blink = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x,y = pos[0],pos[1]
            if x >= 400 and y >= 68 and x <= 560 and y <= 118:
                instructions = False
                
    pos = pygame.mouse.get_pos()
    x,y = pos[0],pos[1]
    if x >= 400 and y >= 68 and x <= 560 and y <= 118:
        pygame.draw.rect(screen,black,[400,68,160,50])
        pygame.draw.rect(screen,green,[400,68,160,50],3)
        pygame.draw.rect(screen,green,[400,68,160,50],6)
        screen.blit(text_start,(420,78))
        
    if blink == True:
        pygame.draw.rect(screen,black,[400,68,160,50])
        pygame.draw.rect(screen,green,[400,68,160,50],3)
        screen.blit(text_start,(420,78))
    
    screen.blit(hjort,(500,260))
    screen.blit(ball,(560,490))
    pygame.draw.rect(screen,black,[350,8,300,50])
    pygame.draw.rect(screen,green,[350,8,300,50],3)
    screen.blit(text_header,(430,15))
    screen.blit(header,(400,35))
    
    clock.tick(20)
    
    pygame.display.flip()
 
 
 
 

# stop intro music
pygame.mixer.music.stop()

# load sound
tree_sound = load_sound('bump.wav')

# Game initialization
size = (985,775)      # gridsize 985x775 pixels
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Fang Den Hjorten')
width,height,margin = 30,30,5
IN_castle = False

# setting the dynamic GRID and the GRID_MAP with the enviroment details (enviroment/object codes) ! see drawmap function !
grid = [[10 for i in range(28)] for i in range(22)]
grid_map = [[1, 0, 0, 1, 0, 8, 2, 2, 7, 0, 0, 0, 0, 0, 0, 0, 0, 8, 2, 7, 0, 8, 0, 0, 0, 11, 11, 11], 
            [3, 2, 2, 9, 0, 1, 0, 0, 3, 2, 2, 2, 4, 2, 2, 2, 2, 9, 0, 6, 2, 5, 2, 2, 2, 11, 11, 11], 
            [1, 0, 0, 0, 0, 1, 0, 8, 9, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 11, 11], 
            [3, 2, 2, 2, 2, 9, 0, 1, 0, 0, 8, 2, 5, 2, 2, 7, 0, 8, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [1, 0, 8, 2, 4, 2, 2, 5, 7, 0, 1, 0, 0, 0, 0, 3, 2, 5, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [1, 0, 1, 0, 1, 0, 0, 0, 6, 2, 9, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 9, 0, 2, 2, 2, 2, 2, 2, 2, 2], 
            [1, 0, 1, 0, 6, 2, 7, 0, 0, 0, 0, 11, 11, 11, 0, 1, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2],
            [3, 2, 9, 0, 0, 0, 3, 2, 2, 4, 2, 11, 11, 11, 0, 1, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2], 
            [1, 0, 0, 0, 8, 2, 9, 0, 0, 1, 0, 11, 11, 11, 0, 6, 2, 2, 2, 7, 0, 0, 0, 0, 1, 0, 0, 0], 
            [1, 0, 8, 2, 9, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 6, 2, 7, 0],
            [1, 0, 1, 0, 0, 8, 2, 7, 0, 3, 7, 0, 0, 0, 0, 11, 11, 11, 0, 1, 0, 8, 2, 7, 0, 0, 1, 0], 
            [1, 0, 3, 2, 4, 9, 0, 1, 0, 6, 5, 2, 4, 2, 2, 11, 11, 11, 0, 1, 0, 3, 0, 1, 0, 0, 1, 0],
            [3, 2, 9, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 11, 11, 11, 0, 1, 0, 1, 0, 6, 7, 0, 1, 0], 
            [1, 0, 0, 0, 0, 0, 0, 0, 8, 2, 7, 0, 6, 4, 0, 0, 0, 0, 0, 1, 0, 6, 7, 0, 1, 0, 1, 0], 
            [1, 0, 8, 2, 7, 0, 0, 0, 1, 0, 1, 0, 0, 6, 4, 2, 7, 0, 8, 5, 7, 0, 1, 0, 6, 2, 9, 0], 
            [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 6, 2, 7, 0, 1, 0, 3, 2, 9, 0, 1, 0, 6, 7, 0, 0, 0, 0], 
            [1, 0, 1, 0, 3, 11, 11, 0, 1, 0, 0, 0, 6, 4, 9, 0, 0, 0, 0, 0, 1, 0, 0, 6, 2, 2, 2, 7], 
            [1, 0, 1, 0, 1, 0, 11, 0, 1, 0, 0, 0, 0, 3, 2, 7, 0, 8, 7, 0, 1, 0, 0, 0, 0, 0, 0, 1], 
            [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 6, 2, 9, 0, 1, 0, 0, 1, 0, 6, 2, 2, 2, 7, 0, 0, 1], 
            [6, 2, 9, 0, 6, 2, 2, 2, 9, 0, 0, 0, 0, 0, 2, 5, 2, 2, 9, 0, 0, 0, 0, 0, 6, 2, 2, 9]]
grid[0][0] = grid_map[0][0]
for column in range(21,28):
            grid[9][column] = 0

# create SPRITES
player_sprite = pygame.sprite.Group()
env_sprites = pygame.sprite.Group()
castle_sprite = pygame.sprite.Group()
bush_sprites = pygame.sprite.Group()
ing_sprite = pygame.sprite.Group()
ml_sprite = pygame.sprite.Group()
vib_sprite = pygame.sprite.Group()

# loading graphics
road_vert,road_vert_rect = load_image('vert_road.png')
road_hori,road_hori_rect = load_image('hori_road.png')
road_tkryds_0,road_tkryds_0_rect = load_image('tkryds_vejen_0.png')
road_tkryds_1,road_tkryds_1_rect = load_image('tkryds_vejen_1.png')
road_tkryds_2,road_tkryds_2_rect = load_image('tkryds_vejen_2.png')
road_lower_right,road_lower_right_rect = load_image('lowerturn_road_right.png')
road_lower_left,road_lower_left_rect = load_image('lowerturn_road_left.png')
road_upper_right,road_upper_right_rect = load_image('upperturn_road_right.png')
road_upper_left,road_upper_left_rect = load_image('upperturn_road_left.png')
castle_env,castle_env_rect = load_image('palace.png',-1)
bush_env,bush_env_rect = load_image('bush.png',-1)
bubble, bubble_rect = load_image('bubble.png',-1)
grass_env,grass_env_rect = load_image('grass.png')

# create castle and player-objects
castle = Enviroment('palace.png')
castle.rect.x,castle.rect.y = 705,150
ml = Enviroment('ml.png')
ml.rect.x,ml.rect.y = 450,320
vib = Enviroment('vibeke.png')
vib.rect.x,vib.rect.y = 940,40
ing = Enviroment('ingrid.png')
ing.rect.x,ing.rect.y = 590,465

# create PLAYER
player = Player()

# Add to relevant sprite groups
castle_sprite.add(castle)
vib_sprite.add(vib)
ing_sprite.add(ing)
ml_sprite.add(ml)
env_sprites.add(ml)
env_sprites.add(vib)
env_sprites.add(ing)
env_sprites.add(castle)
player_sprite.add(player)

# get bush index and add to sprites
for row in range(22):
    for column in range(28):
        if grid_map[row][column] == 0:
            grid[row][column] = 0
            bush_sprite = Bush(column,row)
            bush_sprites.add(bush_sprite)

# set player speed
speed = 3

# backgrounc color
darkgreen = road_vert.get_at((0,0))

# font for speech balloons
fontobj = pygame.font.Font(None, 16)
message = fontobj.render('Lad os så fange Den hjorten!',True,black)
message2 = fontobj.render('Han har stjålet min fodbold!',True,black)
message3 = fontobj.render('Vi skal finde hans slot i skoven.',True,black)
message4 = fontobj.render('Jeg tror jeg kan se det. Afsted! ',True,black)
message_rect = pygame.Rect((22,60,50,50))
message_rect_2 = pygame.Rect((22,80,50,50))
message_rect_3 = pygame.Rect((22,100,50,50))
message_rect_4 = pygame.Rect((22,120,50,50))

# persons found
persons = {'ingrid':0,'ml':0,'vibeke':0}
vibeke_found = False
ingrid_found = False
ml_found = False

# short-intro trigger
intro = True




# GAME-LOOP

while done == False and IN_castle == False:
    
    if intro:
        pygame.event.set_allowed(None)
    
    # get player GRID-position for easy player-tracking
    column,row = player.pos()
       
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if (column,row) == (24,10) and player.direction == 'up':
                    fade()    # rect-blackout for when entering castles
                    IN_castle = True                    
                else:
                    player.interaction()    # check to see if we interact with something

         
    pressed = pygame.key.get_pressed()
        
    if pressed[pygame.K_LEFT]:
        player.move(-speed, 0)
    if pressed[pygame.K_RIGHT]:
        player.move(speed, 0)
    if pressed[pygame.K_UP]:
        player.move(0, -speed)
    if pressed[pygame.K_DOWN]:
        player.move(0, speed)
     
                
    screen.fill(darkgreen)
    draw_map(grid)
    bush_sprites.draw(screen)
    player_sprite.draw(screen)
    
    if ingrid_found:
        ing_sprite.draw(screen)
    if vibeke_found:
        vib_sprite.draw(screen)
    if ml_found:
        ml_sprite.draw(screen)
       
    if not intro:
        castle_sprite.draw(screen)

    if intro:      
        pygame.display.update()
        pygame.time.delay(1000)
        screen.blit(bubble,(15,25))
        pygame.display.update((0,0,500,500))
        pygame.time.delay(1000)
        screen.blit(message,message_rect)
        pygame.display.update((0,0,500,500))
        pygame.time.delay(3000)
        screen.blit(message2,message_rect_2)
        pygame.display.update((0,0,500,500))
        pygame.time.delay(3000)
        screen.blit(message3,message_rect_3)
        pygame.display.update((0,0,500,500))
        pygame.time.delay(3000)
        screen.blit(castle_env,(705,150))
        pygame.display.update((705,150,300,300))       
        pygame.time.delay(1000)
        screen.blit(message4,message_rect_4)
        pygame.display.update((0,0,500,500))
        pygame.time.delay(4000)
        pygame.event.set_blocked(None)
        pygame.event.set_allowed(pygame.QUIT)
        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
        pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.event.set_allowed(pygame.KEYUP)
        intro = False
        
    # the below code checks to see if we found the fields where
    # the persons are located and if so, reports them as "drawable"
    # and updates the grid with the respective field
    if (column,row) == (24,1) and not vibeke_found:
        vibeke_found = True
        for i in range(row-1,row+2):
            for j in range(column+1,column+4):
                grid[i][j] = grid_map[i][j]
    elif (column,row) == (10,9) and not ml_found:
        ml_found = True
        for i in range(row-1,row+2):
            for j in range(column+1,column+4):
                grid[i][j] = grid_map[i][j]
    elif (column,row) == (14,13) and not ingrid_found:
        ingrid_found = True
        for i in range(row-1,row+2):
            for j in range(column+1,column+4):
                grid[i][j] = grid_map[i][j]  
                               
    # updates the map with the player position (row,column)
    if grid[row][column] != grid_map[row][column]:
        grid[row][column] = grid_map[row][column]          
    
    clock.tick(20)
    pygame.display.flip()
 
 


# reinitialize
intro = True
hjort_defeated = False
ball_frame = 0  # used to slow down the NEWBALL events
health_rect_width = 10
health_rect_height = 20
health_rect_margin = 4

# checks if hjort is RAGING
hjort_rage = False

# load new graphics
castle_back = pygame.image.load('ThroneRoom.jpg').convert()

# load the hjort, the player and the ball
hjort = Hjort()
C_player = Castle_player()

# set score
scorefont = pygame.font.Font(None,32)
score = scorefont.render('Hjortens Liv: ',True,black)


# create sprite groups and add sprites
castle_sprites = pygame.sprite.Group(hjort,C_player)
ball_sprites = pygame.sprite.Group()

# controls the NEWBALL frequency
BALLFREQ = 80





# IN_castle - GAME-LOOP goes below here

while done == False:
    
    if ball_frame == 0:
        NEWBALL = randint(0,1)
        ball_frame += 1
    else:
        NEWBALL = 0
        ball_frame += 1
        if ball_frame == BALLFREQ: 
            ball_frame = 0
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            done = True      
        elif event.type == pygame.MOUSEBUTTONDOWN:
            C_player.kick()
        elif event.type == pygame.MOUSEBUTTONUP:
            hjort.kicked()
            C_player.unkick()

    if intro:
        screen.fill(black) 
        pygame.display.flip()
        screen.blit(castle_back,(0,0))
        castle_sprites.draw(screen)
        ball_sprites.draw(screen)
        fade(True)    # True --> unfade
        
    
        hjort.home_center = hjort.rect.center
        for _ in range(10):
            hjort.shake(magnitude=3)                    # jitter
            castle_sprites.draw(screen)
            pygame.display.update((432, 100, 130, 180))
            clock.tick(20)

        hjort.unshake()                                 # back to home
        intro = False
    
    
    screen.blit(castle_back,(0,0))

    screen.blit(score,(0,0))
    for i in range(hjort.health):
        pygame.draw.rect(screen,red,(145+(health_rect_width + health_rect_margin) * i, 0,health_rect_width,health_rect_height))
    
    if C_player.ball_on_foot:
        BOLD_status = 'Ja'
    else:
        BOLD_status = 'Nej'
    ball_loaded = scorefont.render('Bold på fod: %s'% BOLD_status,True,black)
    screen.blit(ball_loaded, (815,0))        
    
    if NEWBALL:
        ball = Ball(hjort.rect.bottomleft)
        ball_sprites.add(ball)    
    
    
    if hjort.health == 0 and not hjort_rage:
        hjort.rage()
        hjort.move = 3
        BALLFREQ -= 20
        hjort.image = hjort.image_alt
        hjort.health = 1         # REMINDER: change to 20
        hjort_rage = True 
    
    castle_sprites.update()
    ball_sprites.update()
    ball_sprites.draw(screen)
    castle_sprites.draw(screen)
    
    # Hjort-defeat animation
    if hjort.health == 0 and hjort_rage:
        for spin in range(30):
            hjort.defeat()
            castle_sprites.draw(screen)
            pygame.display.update(hjort.rect)
            clock.tick(20)
        done = True
        hjort_defeated = True
        
    pygame.display.flip()
    clock.tick(100) # set frame?




# Initialization for END-GAME loop
game_over = False
hjort.image = hjort.image_defeat
hjort.move = 0

# END-GAME font
endtext = pygame.font.Font(None,36)
endtext.set_bold(True)


# END-GAME loop

while not game_over and hjort_defeated:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            game_over = True         
    
    color_red = randint(0,255)
    color_green = randint(0,255)
    color_blue = randint(0,255)
    
    endtext_coords_x = randint(20,650)
    endtext_coords_y = randint(20,750)
    
    endmessage = endtext.render('Hjorten er blevet besejret!',True,(color_red,color_green,color_blue))    
    
    
    screen.fill(black)
    castle_sprites.draw(screen)
    screen.blit(endmessage,(endtext_coords_x,endtext_coords_y))
    
    clock.tick(3)
    
    pygame.display.flip()

pygame.quit()