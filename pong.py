import pygame
import math
import random

pygame.init()
pygame.display.set_caption("pong")
screen = pygame.display.set_mode((650, 480))
clock = pygame.time.Clock()
running = True

ball_size = 15
ball_speed = 12
slow_ball_speed = 6
ball_angle = random.randint(-35,35)
paddle_width = 15
paddle_height = 15 * 5
paddle_speed = 8
l_score = 0
r_score = 0
paddle_l_y_vel = 0
line_width = 2

def l_score_text(l_score):
   l_score_disp=pygame.font.Font(None,60).render(str(l_score), 1,(255,255,255))
   screen.blit(l_score_disp, ((screen.get_width() / 4), 10))
def r_score_text(r_score):
   r_score_disp=pygame.font.Font(None,60).render(str(r_score), 1,(255,255,255))
   screen.blit(r_score_disp, ((screen.get_width() / 1.5), 10))

# sprite classes
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ball_size,ball_size))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, "white", pygame.Rect(0, 0, ball_size, ball_size))
        self.rect.x = x
        self.rect.y = y
        self.x_vel = (slow_ball_speed * math.cos(math.radians(ball_angle)))
        self.y_vel = (slow_ball_speed * math.sin(math.radians(ball_angle)))
    def update(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((paddle_width, paddle_height))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, "white", pygame.Rect(0, 0, paddle_width, paddle_height))
        self.rect.x = x
        self.rect.y = y
    def move(self,y):
        if self.rect.y >= 0 and self.rect.y + paddle_height <= screen.get_height():
            self.rect.y += y
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y + paddle_height > screen.get_height():
            self.rect.y = screen.get_height() - paddle_height
    
# sprite groups
ball = Ball((screen.get_width() / 2) - (ball_size / 2),(screen.get_height() / 2) - (ball_size / 2))
ball_group = pygame.sprite.Group(ball)
paddle_l = Paddle(paddle_width * 2,(screen.get_height() / 2) - (paddle_height / 2))
paddle_r = Paddle(screen.get_width() - (paddle_width * 2),(screen.get_height() / 2) - (paddle_height / 2))
paddle_group = pygame.sprite.Group(paddle_l,paddle_r)

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ball_group.update()
    paddle_group.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        paddle_r.move(-paddle_speed)
    if keys[pygame.K_DOWN]:
        paddle_r.move(paddle_speed)

    for paddle in pygame.sprite.spritecollide(ball,paddle_group,False):
        left = (ball.rect.x + ball_size) - paddle.rect.x
        right = (paddle.rect.x + paddle_width) - ball.rect.x
        bottom = (paddle.rect.y + paddle_height) - ball.rect.y
        top = (ball.rect.y + ball_size) - paddle.rect.y
        place = (ball.rect.y + (ball_size / 2)) - (paddle.rect.y + (paddle_height / 2))
        if left < right and left < top and left < bottom:
            ball.x_vel = -(ball_speed * math.cos(math.radians((place) * 1.3)))
            ball.y_vel = (ball_speed * math.sin(math.radians((place) * 1.3)))
        if right < left and right < top and right < bottom:
            ball.x_vel = (ball_speed * math.cos(math.radians((place) * 1.3)))
            ball.y_vel = (ball_speed * math.sin(math.radians((place) * 1.3)))
        if top < bottom and top < left and top < right and ball.y_vel > 0:
            ball.y_vel *= -1
        if bottom < top and bottom < left and bottom < right and ball.y_vel < 0:
            ball.y_vel *= -1
    if ball.rect.y < 0 or ball.rect.y + ball_size > screen.get_height():
        ball.y_vel *= -1
    if ball.rect.x + ball_size < 0:
        ball.x_vel = (slow_ball_speed * math.cos(math.radians(random.randint(-30,30))))
        ball.y_vel = (slow_ball_speed * math.sin(math.radians(random.randint(-30,30))))
        ball.rect.x = (screen.get_width() / 2) - (ball_size / 2)
        ball.rect.y = (screen.get_height() / 2) - (ball_size / 2)
        r_score += 1
    if ball.rect.x > screen.get_width():
        ball.x_vel = -(slow_ball_speed * math.cos(math.radians(random.randint(-30,30))))
        ball.y_vel = (slow_ball_speed * math.sin(math.radians(random.randint(-30,30))))
        ball.rect.x = (screen.get_width() / 2) - (ball_size / 2)
        ball.rect.y = (screen.get_height() / 2) - (ball_size / 2)
        l_score += 1

    paddle_l_y_vel *= .8
    paddle_l.rect.y += paddle_l_y_vel
    if ball.rect.y + (ball_size / 2) + 26 < paddle_l.rect.y + (paddle_height / 2) and ball.x_vel < 0:
        paddle_l_y_vel -= 2.2
    if ball.rect.y + (ball_size / 2) - 26 > paddle_l.rect.y + (paddle_height / 2) and ball.x_vel < 0:
        paddle_l_y_vel += 2.2
    if paddle_l.rect.y < 0:
        paddle_l_y_vel = 0
        paddle_l.rect.y = 0
    if paddle_l.rect.y + paddle_height > screen.get_height():
        paddle_l_y_vel = 0
        paddle_l.rect.y = screen.get_height() - paddle_height

    # render
    screen.fill("#212325")
    pygame.draw.rect(screen, "white", pygame.Rect((screen.get_width() / 2) - (line_width / 2), 0, line_width, screen.get_height()))
    ball_group.draw(screen)
    paddle_group.draw(screen)
    l_score_text(l_score)
    r_score_text(r_score)
    pygame.display.flip()
    clock.tick(60) / 1000
pygame.quit()
