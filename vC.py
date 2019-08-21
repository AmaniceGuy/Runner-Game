import pygame
import random
pygame.init()


class Miku(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.runImages, self.jumpImages = [],[]
        text = "miku_run_"
        for i in range(8):
            self.runImages.append(pygame.image.load(text+str(i)+".png"))
        self.stand = []
        self.slideImage = pygame.image.load("miku_slide.png")
        text = "miku_jump_"
        for i in range(12):
            self.jumpImages.append(pygame.image.load(text+str(i)+".png"))
        self.images = self.runImages
        self.image = self.images[0]
        self.screen = screen
        self.mask = pygame.mask.from_surface(self.image,0)
        self.isJump = False
        self.rect = self.image.get_rect()
        self.rect.right = 150
        self.rect.bottom = 250
        self.imageCount = 0
        self.speed = 4
        self.isSlide = False
        self.slideCount = 0

    def jump(self):
        self.isJump = True
        self.isSlide = False
        self.neg = 1
        self.jumpCount = 12

    def slide(self):
        self.isSlide = True
        self.isJump = False
        self.image = self.slideImage
        self.rect = self.image.get_rect()
        self.rect.bottom = 250

    def goFaster(self):
        if self.speed > 1:
            self.speed -= 1

    def update(self):
        self.imageCount += 1
        if not self.isSlide:
            if not self.isJump:
                self.rect = self.image.get_rect()
                if self.imageCount >= len(self.images) * self.speed:
                    self.imageCount = 0
                self.image = self.images[self.imageCount//self.speed]
                self.rect = self.image.get_rect()
                self.rect.top = 186

            else:
                self.image = self.jumpImages[int(10-self.jumpCount)//2]
                self.jumpCount -= 0.5
                if not self.jumpCount%1:
                    self.rect.bottom -= self.jumpCount ** 2 * 0.15 * self.neg
                if self.jumpCount == 0:
                    self.neg = -1
                elif self.jumpCount == -12:
                    self.rect = self.image.get_rect()
                    self.rect.bottom = 250
                    self.isJump = False
        
        self.rect.left = 150-self.image.get_width()
        self.mask = pygame.mask.from_surface(self.image)
        self.isSlide = False


class Obstacle(pygame.sprite.Sprite):
    def __init__(self,num,x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("box_0.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = 240
        self.rect.left = x
        self.vel = 2
    
    def setVel(self,speed):
        self.vel = speed

    def makeFly(self):
        if random.randrange(2):
            self.image = pygame.image.load("box_1.png")
            self.rect.bottom = 225
        else:
            self.rect.bottom = 240
            self.image = pygame.image.load("box_0.png")

    def update(self):
        self.rect.left -= self.vel
        if self.rect.right <= 0:
            self.rect.left = 1300
            self.makeFly()


class Background(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1680,316))
        self.image.blit(pygame.image.load("background.png"),(0,0))
        self.image.blit(pygame.image.load("background.png"),(840,0))
        self.ground = pygame.Surface((1980,66))
        self.ground.fill((191,112,6))
        self.image.blit(self.ground,(0,250))
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        self.vel = 2

    def update(self):
        self.rect.left -= self.vel
        if self.rect.centerx <= 0:
            self.rect.left = 0


class ScoreKeeper(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("emulogic.ttf",30) 
        self.score = 0
        self.image = self.font.render(str(self.score),True,(0,0,0))
        self.rect = self.image.get_rect()
        self.gameSpeed = 2
    
    def update(self):
        self.image = self.font.render(str(self.score),True,(0,0,0))
        self.rect.topleft = (830 - self.image.get_width(),10)


class Title(pygame.sprite.Sprite):
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("Thundergood.ttf",50)
        self.image = self.font.render("Lightspeed Miku",True,(0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = screen[0]//2
        self.rect.top = 30


class Button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.image0
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.select = False
    
    def update(self):
        if self.select: self.image,self.select = self.image1,False
        else: self.image = self.image0


class Play(Button):
    def __init__(self):
        self.image0, self.image1 = pygame.image.load("play.png"), pygame.image.load("hi_play.png")
        Button.__init__(self)
        self.rect.center = (420,210)


class Gear(Button):
    def __init__(self):
        self.image0, self.image1 = pygame.image.load("gear.png"), pygame.image.load("hi_gear.png")
        Button.__init__(self)
        self.rect.center = (180,210)


class Cursor(Button):
    def __init__(self):
        self.image0 = pygame.image.load("c1_blue.png")
        Button.__init__(self)
    
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.mask = pygame.mask.from_surface(self.image)


class VolSlider(pygame.sprite.Sprite):
    def __init__(self,vol):
        pygame.sprite.Sprite.__init__(self)
        self.vol = vol
        self.image = pygame.Surface((20,316))
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.slider = pygame.Surface((10,200))
        self.slider.fill((100,100,100))
        self.select = False
        self.level = pygame.image.load("speaker.png")
        self.rect = self.image.get_rect()
        self.rect.center = (600,158)
    
    def setVol(self):
        x,y = pygame.mouse.get_pos()
        if y in range(58,258):
            self.vol = (258 - y )/200
        elif y < 58:
            self.vol = 1.0
        elif y > 258:
            self.vol = 0
        return self.vol

    def update(self):
        self.volIndicator = pygame.Surface((10,self.vol*200))
        self.volIndicator.fill((0,255,255))
        self.image.blit(self.slider,(5,58))
        self.image.blit(self.volIndicator, (5,58+200-(self.vol*200)))
        self.image.blit(self.level,(4,281))
        self.mask = pygame.mask.from_surface(self.image)


class Char(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("miku_stand.png")
        self.rect = self.image.get_rect()
        self.rect.center = (660,210)


class Back(Button):
    def __init__(self):
        self.image0 = pygame.image.load("back.png")
        self.image1 = pygame.image.load("hi_back.png")
        Button.__init__(self)
        self.rect.center = (100,100)
