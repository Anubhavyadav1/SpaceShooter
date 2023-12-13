import pygame
import os
pygame.font.init()
pygame.mixer.init()


#  constant values
HEIGHT, WIDTH = 600,900
FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 3
SPACESHIP_HEIGHT, SPACESHIP_WIDTH  = 35,50

# RGB tuples for color
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# fonts used
HEALTH_FONT = pygame.font.SysFont('calibri', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# sounds used
BULLET_HIT_SOUND =  pygame.mixer.Sound(os.path.join('Resources','bullet_hit.mp3'))
BULLET_FIRE_SOUND =  pygame.mixer.Sound(os.path.join('Resources','bullet_fire.mp3'))

# constant modes and events
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
pygame.display.set_caption('Space Shooter')

IMG_YELLOW_SPACESHIP = pygame.image.load(
    os.path.join('Resources', 'spaceship_yellow.png')
    )
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(IMG_YELLOW_SPACESHIP, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90 )

IMG_RED_SPACESHIP = pygame.image.load(
    os.path.join('Resources', 'spaceship_red.png')
    ) 
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(IMG_RED_SPACESHIP, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)

YELLOW_HIT = pygame.USEREVENT+1
RED_HIT = pygame.USEREVENT+2

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Resources', 'space.png')), (WIDTH,HEIGHT))


def draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health):

    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    
    pygame.display.update()

def handle_yellow_movement(keys_pressed, yellow):
    if(keys_pressed[pygame.K_a] and yellow.x-VEL>0): #LEFT
        yellow.x -= VEL
    if(keys_pressed[pygame.K_d] and yellow.x+VEL+yellow.width+10<BORDER.x): #RIGHT
        yellow.x += VEL
    if(keys_pressed[pygame.K_w] and yellow.y-VEL>0): #UP
        yellow.y -= VEL
    if(keys_pressed[pygame.K_s] and yellow.y+yellow.height<HEIGHT): #DOWN
        yellow.y += VEL

def handle_red_movement(keys_pressed, red):
    if(keys_pressed[pygame.K_LEFT] and red.x-VEL-5>BORDER.x): #LEFT
        red.x -= VEL
    if(keys_pressed[pygame.K_RIGHT] and red.x+VEL+red.width+15<WIDTH): #RIGHT
        red.x += VEL
    if(keys_pressed[pygame.K_UP] and red.y-VEL>0): #UP
        red.y -= VEL
    if(keys_pressed[pygame.K_DOWN] and red.y+red.height<HEIGHT): #DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if(red.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif(bullet.x>WIDTH):
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if(yellow.colliderect(bullet)):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif(bullet.x<0):
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():

    red = pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(200,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True 
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                run = False
                pygame.quit()

            if(event.type == pygame.KEYDOWN):
                
                if(event.key == pygame.K_LSHIFT and len(yellow_bullets)<MAX_BULLETS):
                    bullet = pygame.Rect(yellow.x+yellow.width , yellow.y+yellow.height//2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                if(event.key == pygame.K_RSHIFT and len(red_bullets)<MAX_BULLETS):
                    bullet = pygame.Rect(red.x , red.y+red.height//2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if(event.type == RED_HIT):
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if(event.type == YELLOW_HIT):
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
            
        winner_text = ""

        if(red_health<=0):
            winner_text = "Yellow Wins!"
        
        if(yellow_health<=0):
            winner_text = "Red Wins!"

        if(winner_text != ""):
            draw_winner(winner_text)
            break
        
        keys_pressed = pygame.key.get_pressed()

        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, yellow_bullets, red_bullets, yellow_health, red_health) 
    
    main()

if __name__ == "__main__":
    main()

