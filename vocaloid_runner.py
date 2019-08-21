#Import / Initialize
import pygame
import random
import vC
pygame.init()
pygame.mixer.init()

SCREENSIZE = (840,316)
VOLUME = 0.25
CHARNUM = 0
MOUSE = vC.Cursor()
BACKGROUND = pygame.image.load("titlescreen.png")
CLOCK = pygame.time.Clock()

def game():
    #Display
    screen = pygame.display.set_mode(SCREENSIZE)
    #Entities
    bg = pygame.Surface(SCREENSIZE)
    background = vC.Background(screen)
    player = vC.Miku(screen)
    obstacles = [vC.Obstacle(0,840),vC.Obstacle(0,1200),vC.Obstacle(0,1540)]
    obstacleGroup = pygame.sprite.Group(obstacles)
    scoreKeeper = vC.ScoreKeeper()
    #Sprites
    allSprites = pygame.sprite.OrderedUpdates(background,player,obstacleGroup,scoreKeeper,MOUSE)
    #Action - Assign
    run = True
    gameTick = 0

    #Loop
    while run:

        CLOCK.tick(60)

        gameTick += 1
        if gameTick == 500:
            gameTick = 0
            background.vel += 1
            scoreKeeper.gameSpeed = background.vel
            for obstacle in obstacles:
                obstacle.setVel(background.vel)
            player.goFaster()

        if not gameTick%10:
            scoreKeeper.score += scoreKeeper.gameSpeed
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not player.isJump:
            player.jump()
        if keys[pygame.K_DOWN]:
            player.slide()

        hit = pygame.sprite.spritecollide(player,obstacleGroup,False,pygame.sprite.collide_mask)
        if hit:
            pygame.time.delay(500)
            run = False

        allSprites.clear(screen,bg)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

    return scoreKeeper.score

def main():
    screen = pygame.display.set_mode(SCREENSIZE)
    #Entities
    optionButton = vC.Gear()
    playButton = vC.Play()

    char = vC.Char()
    title = vC.Title(SCREENSIZE)
    buttons = pygame.sprite.Group(optionButton,playButton)
    allSprites = pygame.sprite.OrderedUpdates(char,buttons,MOUSE,title)
    run = True
    pygame.mouse.set_visible(False)
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.set_volume(VOLUME)
    pygame.mixer.music.play(-1)

    while run:
        CLOCK.tick(30)

        hit = pygame.sprite.spritecollide(MOUSE,buttons,False,pygame.sprite.collide_mask)
        for button in hit:
            button.select = True
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if optionButton.select:
                    optionButton.select = False
                    if not options():
                        run = False
                elif playButton.select:
                    playButton.select = False
                    score = game()
                    if not score:
                        pygame.time.delay(500)
                        run = False

        screen.blit(BACKGROUND,(0,0))
        allSprites.clear(screen,BACKGROUND)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

    pygame.mixer.music.fadeout(2000)
    pygame.time.delay(2000)
    pygame.quit()

def options():
    #Display
    screen = pygame.display.set_mode(SCREENSIZE)
    #Entities
    global VOLUME
    volSlider = vC.VolSlider(VOLUME)
    back = vC.Back()
    buttons = [volSlider,back]

    allSprites = pygame.sprite.OrderedUpdates(buttons,MOUSE)
    #Assign
    run = True

    while run:
        CLOCK.tick(30)
        for button in buttons:
            button.select = False
        hit = pygame.sprite.spritecollide(MOUSE,buttons,False,pygame.sprite.collide_mask)
        for button in hit:
            button.select = True
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True

        if any(pygame.mouse.get_pressed()):
            if back.select:
                return True
            if volSlider.select:
                VOLUME = volSlider.setVol()
                pygame.mixer.music.set_volume(VOLUME)

        screen.blit(BACKGROUND,(0,0))
        allSprites.clear(screen,BACKGROUND)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
    return False

main()
