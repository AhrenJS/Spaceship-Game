import pygame
import os
import sys
pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game")

Ship_WIDTH, Ship_HEIGHT = 55, 40

BORDER = pygame.Rect(WIDTH/2-5, 0, 10, HEIGHT)

Health_Font = pygame.font.SysFont("comicsans", 40)
Winner_Font = pygame.font.SysFont("comicsans", 100)
Score_Font = pygame.font.SysFont("comicsans", 40)

VELO = 3
Bullet_VELO = 10
Max_Bullet = 3

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

HEALTH = 10

Yellow_hit = pygame.USEREVENT + 1
Red_hit = pygame.USEREVENT + 2

Yellow_Spaceship_Image = pygame.image.load(os.path.join("Assets","spaceship_yellow.png"))
yellow_victory = pygame.transform.scale(Yellow_Spaceship_Image, (Ship_WIDTH*4, Ship_HEIGHT*4))
Yellow_Ship = pygame.transform.rotate(
    pygame.transform.scale(Yellow_Spaceship_Image, (Ship_WIDTH,Ship_HEIGHT)), 90)

Red_Spaceship_Image = pygame.image.load(os.path.join("Assets","spaceship_red.png"))
red_victory = pygame.transform.scale(Red_Spaceship_Image, (Ship_WIDTH*4, Ship_HEIGHT*4))
Red_Ship = pygame.transform.rotate(
    pygame.transform.scale(Red_Spaceship_Image, (Ship_WIDTH,Ship_HEIGHT)), 270)

Space = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

def Yellow_Movement_Control(keys_pressed, yellow_pos):
    if keys_pressed[pygame.K_SPACE]:
        yellow_VELO = 8
    else:
        yellow_VELO = VELO
    if keys_pressed[pygame.K_a] and yellow_pos.x - VELO > 0:  # Left
        yellow_pos.x -= yellow_VELO
    if keys_pressed[pygame.K_d] and yellow_pos.x + VELO + yellow_pos.width < BORDER.x:  # Right
        yellow_pos.x += yellow_VELO
    if keys_pressed[pygame.K_w] and yellow_pos.y - VELO > 0:  # Up
        yellow_pos.y -= yellow_VELO
    if keys_pressed[pygame.K_s] and yellow_pos.y + VELO + yellow_pos.height < HEIGHT - 15:  # Down
        yellow_pos.y += yellow_VELO

def Red_Movement_Control(keys_pressed, red_pos):
    if keys_pressed[pygame.K_SLASH]:
        red_VELO = 8
    else:
        red_VELO = VELO
    if keys_pressed[pygame.K_LEFT] and red_pos.x - VELO > BORDER.x + BORDER.width:  # Left
        red_pos.x -= red_VELO
    if keys_pressed[pygame.K_RIGHT] and red_pos.x + red_pos.height + VELO < WIDTH:  # Right
        red_pos.x += red_VELO
    if keys_pressed[pygame.K_UP] and red_pos.y - VELO > 0:  # Up
        red_pos.y -= red_VELO
    if keys_pressed[pygame.K_DOWN] and red_pos.y + VELO + red_pos.height < HEIGHT - 15:  # Down
        red_pos.y += red_VELO

def handle_bullet(yellow_bullet, red_bullet, yellow_pos, red_pos):
    for bullet in yellow_bullet:
        bullet.x += Bullet_VELO
        if red_pos.colliderect(bullet):
            pygame.event.post(pygame.event.Event(Red_hit))
            yellow_bullet.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullet.remove(bullet)
    for bullet in red_bullet:
        bullet.x -= Bullet_VELO
        if yellow_pos.colliderect(bullet):
            pygame.event.post(pygame.event.Event(Yellow_hit))
            red_bullet.remove(bullet)
        elif bullet.x < 0:
            red_bullet.remove(bullet)

def draw_window(yellow_pos, red_pos, yellow_bullet, red_bullet, yellow_health, red_health, yellow_score, red_score):
    WIN.blit(Space, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    yellow_health_text = Health_Font.render("Health : " + str(yellow_health), True, WHITE)
    red_health_text = Health_Font.render("Health : " + str(red_health), True, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(Yellow_Ship, (yellow_pos.x,yellow_pos.y))
    WIN.blit(Red_Ship, (red_pos.x,red_pos.y))

    draw_score_yellow = Score_Font.render("Yellow : " + str(yellow_score), True, WHITE)
    WIN.blit(draw_score_yellow, (10, HEIGHT - draw_score_yellow.get_height()))
    draw_score_red = Score_Font.render("Red : " + str(red_score), True, WHITE)
    WIN.blit(draw_score_red, (WIDTH - draw_score_red.get_width() - 10, HEIGHT - draw_score_red.get_height()))

    for bullet in yellow_bullet:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullet:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()

def draw_winner(win_text, win_image):
    draw_text = Winner_Font.render(win_text, True, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2 - 40))
    if win_image=="yellow":
        WIN.blit(yellow_victory, (WIDTH/2 - yellow_victory.get_width()/2, HEIGHT/2))
    elif win_image=="red":
        WIN.blit(red_victory, (WIDTH/2 - red_victory.get_width()/2, HEIGHT/2))
    pygame.display.update()
    pygame.time.delay(3000)

def maingame():
    global yellow_score, red_score
    yellow_pos = pygame.Rect(200, 300, Ship_WIDTH, Ship_HEIGHT)
    red_pos = pygame.Rect(700,300, Ship_WIDTH, Ship_HEIGHT)
    red_bullet = []
    yellow_bullet = []

    red_health = HEALTH
    yellow_health = HEALTH

    in_clock = pygame.time.Clock()
    run = True
    while run:
        in_clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_r and len(yellow_bullet) < Max_Bullet:
                    bullet = pygame.Rect(yellow_pos.x + yellow_pos.width, yellow_pos.y + yellow_pos.height/2 - 2, 10, 4)
                    yellow_bullet.append(bullet)

                if event.key == pygame.K_m and len(red_bullet) < Max_Bullet:
                    bullet = pygame.Rect(red_pos.x, red_pos.y + red_pos.height/2 - 2, 10, 4)
                    red_bullet.append(bullet)
            if event.type==Red_hit:
                red_health -= 1
            if event.type==Yellow_hit:
                yellow_health -= 1
        winner = ""
        win_image = ""
        if red_health <= 0:
            winner = "Yellow Wins!"
            yellow_score += 1
            win_image = "yellow"
        if yellow_health <= 0:
            winner = "Red Wins!"
            red_score += 1
            win_image = "red"
        if winner != "":
            draw_winner(winner, win_image)
            break

        keys_pressed = pygame.key.get_pressed()

        Yellow_Movement_Control(keys_pressed, yellow_pos)
        Red_Movement_Control(keys_pressed, red_pos)

        handle_bullet(yellow_bullet, red_bullet, yellow_pos, red_pos)

        draw_window(yellow_pos, red_pos, yellow_bullet, red_bullet, yellow_health, red_health, yellow_score, red_score)
    maingame()

if __name__ == "__main__":
    yellow_score = 0
    red_score = 0
    maingame()
