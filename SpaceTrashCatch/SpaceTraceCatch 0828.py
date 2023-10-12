#**************모듈, 파이게임 기본 설정*********
import sys, pygame, math, time, random
from pygame.locals import *

pygame.init()
W,H = 1024, 768
screen = pygame.display.set_mode((W,H))
##screen = pygame.display.set_mode(
##    (W,H),
##    pygame.FULLSCREEN
##)
pygame.display.set_caption("우주 쓰레기 잡기")
clock = pygame.time.Clock()


#***********이미지*********
#우주선 이미지
big_spaceShip_image = pygame.image.load("spaceship.png").convert()
spaceShip_image = pygame.transform.scale(big_spaceShip_image, (100,120))
spaceShip_image.set_colorkey((255,255,255))
#회전한 이미지 저장
rotate_spaceShip = spaceShip_image
#중심 좌표 변경용 우주선 이미지
new_spaceShip_rect = rotate_spaceShip.get_rect(
    center = spaceShip_image.get_rect(
            center = (W / 2, H / 2)
    ).center
)

#그물 이미지
big_net_image = pygame.image.load("net.png").convert()
net_image = pygame.transform.scale(big_net_image, (90, 80))
net_image.set_colorkey((255,255,255))
#회전한 이미지 저장
rotate_net = net_image
#중심 좌표 변경용 그물 이미지
#그물 좌표
net_x, net_y = (W / 2), (H / 2)
new_net_rect = rotate_net.get_rect(
    center = net_image.get_rect(
            center = (net_x, net_y)
    ).center
)

#쓰레기 이미지
big_trash_image = pygame.image.load("trash.png").convert()
big_trash_image.set_colorkey((0,0,0))
big_targetTrash_image = pygame.image.load("targetTrash.png").convert()
big_targetTrash_image.set_colorkey((0,0,0))


#색
White = [255,255,255]
Black = [0,0,0]



#***********전역변수***********
#키 입력
pressed_keys = None
#각도
angle = 0
#쓰레기 생성 쿨타임
trashCreateTime = time.time()
#그물 발사 쿨타임
netShootTime = time.time() - 3
#게임 시간
gamePlayTime = time.time()
#게임 점수
score = 0



#쓰레기 클래스 생성
class Trash:
    #도는 범위, 속도, 크기 지정, 좌표 변수 생성
    def __init__(self):
        self.r = random.randint(150, 500) #도는 크기
        self.speed = random.random() + 0.1 #도는 속도
        self.size = random.randint(30, 70) #쓰레기의 크기
        self.angle = random.randint(0,359) #시작 각도
        self.target = 0 #청소 우선 순위

        self.x = W/2 + math.sin(math.pi / 180 * self.angle) * self.r #쓰레기의 x좌표
        self.y = H/2 + math.cos(math.pi / 180 * self.angle) * self.r #쓰레기의 y좌표

        self.image = pygame.transform.scale(big_trash_image, (self.size, self.size)) #쓰레기의 이미지
        self.rotate_image = self.image #쓰레기의 회전 이미지
        #쓰레기의 중심좌표 지정
        self.image_rect = self.rotate_image.get_rect(
            center = self.image.get_rect(
                center = (self.x, self.y)
            ).center
        )

    #쓰레기의 움직임 함수
    def move(self):
        #쓰레기의 현재 각도가 360도 이상이면 0도로 바꿈
        if self.angle + self.speed >= 360:
            self.angle = self.angle + self.speed - 360
        #쓰레기의 각도를 속도에 따라 증가
        else:
            self.angle += self.speed

        #쓰레기의 현재 각도에 알맞는 좌표값 계산
        self.x = W/2 + math.sin(math.pi / 180 * self.angle) * self.r
        self.y = H/2 + math.cos(math.pi / 180 * self.angle) * self.r

        #쓰레기의 좌표에 맞는 회전 이미지
        self.rotate_image = pygame.transform.rotate(self.image, self.angle) 
        #쓰레기의 중심 좌표 지정
        self.image_rect = self.rotate_image.get_rect(   
            center = self.image.get_rect(
                center = (self.x, self.y)
            ).center
        )
        #쓰레기 이미지 출력
        screen.blit(self.rotate_image, self.image_rect)

    def First(self):
        self.image = pygame.transform.scale(big_targetTrash_image, (self.size, self.size))
        self.target = 1




#************보통 함수*********
#주어진 좌표가 화면을 넘어서는지 확인하는 함수
def Check_Out_Net(x, y):
    if x <= -50 or x >= W+50:
        return False
    if y <= -50 or y >= H+50:
        return False
    return True

#쓰레기들을 움직이게 하는 함수
def Trash_Move():
    for i in range(len(trash)):
        trash[i].move()

#쓰레기 중 최우선 청소 대상 지정
def Pick_Clean_Trash():
    trash[0].image = pygame.transform.scale(big_trash_image, (trash[0].size, trash[0].size))
    trash[0].target = 0
    firstSpeed = 0
    firstBig = 0
    
    for i in range(1,len(trash)):
        trash[i].image = pygame.transform.scale(big_trash_image, (trash[i].size, trash[i].size))
        trash[i].target = 0
        
        if trash[i].speed > trash[firstSpeed].speed:
            firstSpeed = i

        if trash[i].size > trash[firstSpeed].size:
            firstBig = i

    trash[firstSpeed].First()
    trash[firstBig].First()


#*********주요 함수*********
#우주선 회전
def Rotate_Spaceship():
    global angle, rotate_spaceShip, new_spaceShip_rect

    #각도 360 이상이면 0으로 바꿈
    if angle >= 360:
        angle = 0
    #각도가 0 미만이면 359으로 바꿈
    if angle < 0:
        angle = 359
    #좌우
    if pressed_keys[K_RIGHT]:
        angle -= 2
    if pressed_keys[K_LEFT]:
        angle += 2

    #중간에서 고정으로 돔
    rotate_spaceShip = pygame.transform.rotate(spaceShip_image, angle)
    new_spaceShip_rect = rotate_spaceShip.get_rect(
        center = spaceShip_image.get_rect(
            center = (W / 2, H / 2)
        ).center
    )

#그물 발사
def Shoot_Net():
    global rotate_net, net_x, net_y, new_net_rect, netShootTime, score

    radian = 0 #각도에 따른 라디안 값
    dnet_x, dnet_y =  net_x, net_y #그물 발사 위치
    crash = 0 #충돌 이벤트
    weight = 0 #잡은 쓰레기의 무게
    
    radian = math.pi / 180 * angle
    rotate_net = pygame.transform.rotate(net_image, angle)
    while Check_Out_Net(dnet_x, dnet_y) and crash == 0:
        dnet_x -= math.sin(radian) * 5
        dnet_y -= math.cos(radian) * 5
        new_net_rect = rotate_net.get_rect(
            center = net_image.get_rect(
                center = (dnet_x, dnet_y)
            ).center
        )

        for i in range(len(trash)):
            if pygame.Rect(trash[i].x, trash[i].y, trash[i].size+5, trash[i].size+5).collidepoint((dnet_x, dnet_y)): 
                weight = trash[i].size
                if trash[i].target == 1:
                    score += 500
                else:
                    score += 100
                    
                del(trash[i])
                Pick_Clean_Trash()
                crash = 1
                break
        
        screen.fill(Black)
        Trash_Move()
        screen.blit(rotate_net, new_net_rect)
        screen.blit(rotate_spaceShip, new_spaceShip_rect)
        pygame.display.update()
        clock.tick(120)
        
    if crash == 1:
        netShootTime += 1
        while not pygame.Rect(dnet_x - 5, dnet_y - 5, 10, 10).collidepoint((W/2,H/2)):
            dnet_x += math.sin(radian) * 2
            dnet_y += math.cos(radian) * 2
            new_net_rect = rotate_net.get_rect(
                center = net_image.get_rect(
                    center = (dnet_x, dnet_y)
                ).center
            )

            screen.fill(Black)
            Trash_Move()
            screen.blit(rotate_net, new_net_rect)
            screen.blit(rotate_spaceShip, new_spaceShip_rect)
            pygame.display.update()
            clock.tick(120)
        
trash = []
for i in range(5): trash.append(Trash())
Pick_Clean_Trash()


#********게임 실행*********
game = True
while game:
    #게임 속
    clock.tick(120)
    #이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if len(trash) >= 11 or time.time() - gamePlayTime >= 60:
        game = False

    if time.time() - trashCreateTime >= 5:
        trashCreateTime = time.time()
        trash.append(Trash())
        Pick_Clean_Trash()
        
    #키입력
    pressed_keys = pygame.key.get_pressed()
    #우주선 회전
    Rotate_Spaceship()
    #그물 발사
    if pressed_keys[pygame.K_SPACE] and time.time() - netShootTime >= 2:
        netShootTime = time.time()
        pressed_keys = None
        Shoot_Net()

    #화면그리기
    screen.fill(Black)
    screen.blit(rotate_spaceShip, new_spaceShip_rect)
    Trash_Move()
    pygame.display.update()

print(1)


    
