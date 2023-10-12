import sys, pygame, math
from pygame.locals import *

angle = 0
pygame.init()
width, height = 1024, 768
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("우주 쓰레기 잡기")
clock = pygame.time.Clock()

big_spaceShip_image = pygame.image.load("spaceship.png").convert()
spaceShip_image = pygame.transform.scale(big_spaceShip_image, (100,120))
spaceShip_image.set_colorkey((255,255,255))
#회전한 이미지 저장
rotate_spaceShip = spaceShip_image
#중심 좌표 변경용 우주선 이미지
new_spaceShip_rect = rotate_spaceShip.get_rect(
    center = spaceShip_image.get_rect(
            center = (width / 2, height / 2)
    ).center
)



def Rotate_Spaceship():
    global angle, rotate_spaceShip, new_rect

    #각도 360 이상이면 0으로 바꿈
    if abs(angle) >= 360:
        angle = 0

    #좌우
    if pressed_keys[K_RIGHT]:
        angle -= 2
    if pressed_keys[K_LEFT]:
        angle += 2

    #중간에서 고정으로 돔
    rotate_spaceShip = pygame.transform.rotate(spaceShip_image, angle)
    new_spaceShip_rect = rotate_spaceShip.get_rect(
        center = spaceShip_image.get_rect(
            center = (width / 2, height / 2)
        ).center
    )


while True:
    #게임 속
    clock.tick(120)
    #이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #키입력
    pressed_keys = pygame.key.get_pressed()
    #우주선 회전
    Rotate_Spaceship()

    screen.fill((255,255,255))
    screen.blit(rotate_spaceShip, new_spaceShip_rect)
    pygame.display.update()
