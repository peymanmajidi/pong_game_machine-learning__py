import pygame
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

pygame.init()

WIDTH = 1200
HEIGHT = 600
BORDER = 30
WHITE = pygame.Color("white")
BLACK = pygame.Color("black")
GREEN = pygame.Color("green")
BLUE = (127,127,127)
RED = pygame.Color("red")
bgColor = BLACK
ball_color = RED
VELOCITY = 5
FRAMERATE = 15
# BLUE = WHITE

screen = pygame.display.set_mode((WIDTH, HEIGHT))

#-------Ball-------
class Ball:
    
    RADIUS = 25
    
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    
    def show(self,color):
        pygame.draw.circle(screen, color, (self.x, self.y), self.RADIUS)
        
    def update(self, paddle_y, paddle_WIDTH, paddle_HEIGHT):
        global bonus_left, bonus_right
        newx = self.x + self.vx
        newy = self.y + self.vy
        
        if paddle_y - paddle_HEIGHT//2 <= newy + self.RADIUS and newy - self.RADIUS <= paddle_y + paddle_HEIGHT//2 \
            and (newx + self.RADIUS >= WIDTH - paddle_WIDTH or newx - self.RADIUS + VELOCITY <= Paddle.WIDTH):
            self.vx = - self.vx
            
        if newy < BORDER + self.RADIUS or newy > HEIGHT - BORDER - self.RADIUS:
            self.vy = - self.vy
            
        self.show(bgColor)
        self.x += self.vx
        self.y += self.vy
        self.show(ball_color)

        if self.x <=0: 
            self.show(bgColor)
            bonus_right +=1
            ball.x = WIDTH // 2
            ball.y = HEIGHT // 2
            self.show(GREEN)
            pygame.display.flip()
            pygame.time.delay(200)


            
        if self.x > WIDTH:
            self.show(bgColor)
            bonus_left +=1
            ball.x = WIDTH // 2
            ball.y = HEIGHT // 2
            self.show(GREEN)
            pygame.display.flip()
            pygame.time.delay(200)


        
#-------Paddle-------
class Paddle:
    WIDTH = 30
    HEIGHT = 120
    
    def __init__(self,y):
        self.y = y

        
    def show(self, colour,x):
        pygame.draw.rect(screen, colour, pygame.Rect(x, self.y - self.HEIGHT//2,self.WIDTH,self.HEIGHT))
        
    def update(self,mouse,x):
        self.show(bgColor,x)
        self.y = mouse
        self.show(BLUE,x)

    @property
    def Y(self):
        return self.y - self.HEIGHT//2

paddle = Paddle(HEIGHT//2)

user_paddle = Paddle(HEIGHT//2)
        
ball = Ball(WIDTH - Ball.RADIUS - paddle.WIDTH, HEIGHT//2, -VELOCITY, -VELOCITY)

bonus_left = 0
bonus_right = 0

def draw_ui():
    pygame.draw.rect(screen, WHITE ,pygame.Rect((0,0),(WIDTH,BORDER)))
    pygame.draw.rect(screen, WHITE ,pygame.Rect(0,HEIGHT - BORDER,WIDTH,BORDER))
    pygame.draw.line(screen, WHITE , ( WIDTH // 2, 0),( WIDTH//2, HEIGHT))

    myfont = pygame.font.SysFont('tahoma', 20)
    textsurface = myfont.render(f"Left: {bonus_left}" , False, (0, 0, 0))
    screen.blit(textsurface,(0,0))
    textsurface = myfont.render(f"Right: {bonus_right}" , False, (0, 0, 0))
    screen.blit(textsurface,(WIDTH - textsurface.get_size()[0]  ,0))

draw_ui()
ball.show(ball_color)

paddle.show(BLUE,WIDTH - Paddle.WIDTH)

user_paddle.show(BLUE, WIDTH - Paddle.WIDTH)

#sample = open("game.csv","a")
#print("x,y,vx,vx,Paddle.y", file=sample)

pong = pd.read_csv("game.csv")
pong = pong.drop_duplicates()

x = pong.drop(columns="Paddle.y")
y = pong["Paddle.y"]

clf = KNeighborsRegressor(n_neighbors=3)

clf.fit(x,y)

df = pd.DataFrame(columns=['x','y','vx','vy'])

clock = pygame.time.Clock()

#=============GAME============
while True:
    e = pygame.event.poll()
    if e.type == pygame.QUIT: break

    draw_ui()
    toPredict = df.append({'x':ball.x, 'y':ball.y, 'vx': ball.vx, 'vy':ball.vy}, ignore_index=True)
    shouldMove = int(clf.predict(toPredict))
    
    ball.update(paddle.y, paddle.WIDTH, paddle.HEIGHT)

    if ball.vx > 0 and ( shouldMove < paddle.Y or shouldMove > paddle.Y + paddle.HEIGHT):
        paddle.update(shouldMove,WIDTH - Paddle.WIDTH)
        print(paddle.Y,":", shouldMove, ":", paddle.Y + paddle.HEIGHT)
    
    ball.update(user_paddle.y, user_paddle.WIDTH, user_paddle.HEIGHT)
    user_paddle.update(pygame.mouse.get_pos()[1],0)
    
    pygame.time.delay(FRAMERATE)
    #refresh
    pygame.display.flip()
    ##collecting data
    #print("{},{},{},{},{}".format(ball.x,ball.y,ball.vx,ball.vy,paddle.y), file=sample)

pygame.quit()
