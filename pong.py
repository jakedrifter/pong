#setup
import pygame
import math
import random
pygame.init()
pygame.display.set_caption('pong')
screen = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()
running = True

#variables
line_width = 2
paddle_width = 15
paddle_height = 90
paddle_r_x = screen.get_width() - paddle_width * 2
paddle_r_y = (screen.get_height() / 2) - (paddle_height / 2)
paddle_l_x = paddle_width * 2
paddle_l_y = (screen.get_height() / 2) - (paddle_height / 2)
paddle_speed = 8.5
ball_size = 15
ball_x = (screen.get_width() / 2) - (ball_size / 2)
ball_y = (screen.get_height() / 2) - (ball_size / 2)
ball_speed = 6
ball_angle = random.randint(0,60) - 30
ball_x_vel = (ball_speed * math.cos(math.radians(ball_angle)))
ball_y_vel = (ball_speed * -math.sin(math.radians(ball_angle)))
l_score = 0
r_score = 0


#score
font=pygame.font.Font(None,50)
def l_score_text(l_score):
   l_score_disp=font.render(str(l_score), 1,(255,255,255))
   screen.blit(l_score_disp, ((screen.get_width() / 2 - 50), 10))
def r_score_text(r_score):
   r_score_disp=font.render(str(r_score), 1,(255,255,255))
   screen.blit(r_score_disp, ((screen.get_width() / 2 + 10), 10))

#loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle_r_y > 0:
        paddle_r_y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle_r_y + paddle_height < screen.get_height():
        paddle_r_y += paddle_speed
    if keys[pygame.K_w] and paddle_l_y > 0:
        paddle_l_y -= paddle_speed
    if keys[pygame.K_s] and paddle_l_y + paddle_height < screen.get_height():
        paddle_l_y += paddle_speed
    
    #see if ball hits left paddle
    if ball_x <= paddle_l_x + paddle_width and ball_x >= paddle_l_x - (paddle_width) and ball_y + ball_size > paddle_l_y and ball_y < paddle_l_y + paddle_height:
        ball_speed = 11
        ball_x_vel = (ball_speed * math.cos(math.radians(((ball_y + (ball_size / 2)) - (paddle_l_y + (paddle_height / 2))))))
        ball_y_vel = -(ball_speed * -math.sin(math.radians(((ball_y + (ball_size / 2)) - (paddle_l_y + (paddle_height / 2))))))

    #see if ball hits right paddle
    if ball_x + ball_size >= paddle_r_x and ball_x + ball_size <= paddle_r_x + (paddle_width) and ball_y + ball_size > paddle_r_y and ball_y < paddle_r_y + paddle_height:
        ball_speed = 11
        ball_x_vel = -(ball_speed * math.cos(math.radians(((ball_y + (ball_size / 2)) - (paddle_r_y + (paddle_height / 2))))))
        ball_y_vel = -(ball_speed * -math.sin(math.radians(((ball_y + (ball_size / 2)) - (paddle_r_y + (paddle_height / 2))))))
    
    #see if left paddle missed
    if ball_x < 0 - ball_size:
        ball_speed = 6
        ball_angle = random.randint(0,60) - 30
        ball_x_vel = (ball_speed * math.cos(math.radians(ball_angle)))
        ball_y_vel = (ball_speed * -math.sin(math.radians(ball_angle)))
        ball_x = (screen.get_width() / 2) - (ball_size / 2)
        ball_y = (screen.get_height() / 2) - (ball_size / 2)
        paddle_l_y = (screen.get_height() / 2) - (paddle_height / 2)
        paddle_r_y = (screen.get_height() / 2) - (paddle_height / 2)
        r_score += 1

    #see if right paddle missed
    if ball_x > screen.get_width():
        ball_speed = 6
        ball_angle = random.randint(0,60) - 30
        ball_x_vel = -(ball_speed * math.cos(math.radians(ball_angle)))
        ball_y_vel = -(ball_speed * -math.sin(math.radians(ball_angle)))
        ball_x = (screen.get_width() / 2) - (ball_size / 2)
        ball_y = (screen.get_height() / 2) - (ball_size / 2)
        paddle_r_y = (screen.get_height() / 2) - (paddle_height / 2)
        paddle_l_y = (screen.get_height() / 2) - (paddle_height / 2)
        l_score += 1
    
    #see if ball hit top or bottom of screen
    if ball_y <= 0 or ball_y >= screen.get_height() - ball_size:
        ball_y_vel *= -1

    #computer controls for left paddle. delete this code for 2 player mode.
    if ball_y + (ball_size / 2) + 30 < paddle_l_y + (paddle_height / 2) and paddle_l_y > 0 and ball_x_vel < 0:
        paddle_l_y -= paddle_speed * .7
    if ball_y + (ball_size / 2) - 30 > paddle_l_y + (paddle_height / 2) and paddle_l_y + paddle_height < screen.get_height() and ball_x_vel < 0:
        paddle_l_y += paddle_speed * .7
    
    #add ball vectors to ball coords
    ball_x += ball_x_vel
    ball_y += ball_y_vel

    #render
    screen.fill("black")
    pygame.draw.rect(screen, "white", pygame.Rect((screen.get_width() / 2) - (line_width / 2), 0, line_width, screen.get_height()))
    pygame.draw.rect(screen, "white", pygame.Rect(ball_x,ball_y, ball_size, ball_size))
    l_score_text(l_score)
    r_score_text(r_score)
    pygame.draw.rect(screen, "white", pygame.Rect(paddle_r_x,paddle_r_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, "white", pygame.Rect(paddle_l_x,paddle_l_y, paddle_width, paddle_height))
    pygame.display.flip()
    clock.tick(60) / 1000
pygame.quit()
