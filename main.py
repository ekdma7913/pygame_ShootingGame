import pygame
import sys
import random

from time import sleep

# 기본 게임 화면 크기
padWidth = 480  # 전체 가로
padHeight = 640  # 전체 세로

# 메인화면
def main_menu():
    global gamePad, clock, selectSound
    pygame.mixer.music.load("main.mp3")  # 배경음악
    pygame.mixer.music.play(-1)  # 배경음악재생
    menu = True
    selected = "start"
    background2 = pygame.image.load("메인메뉴.jpeg")
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selectSound.play()
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selectSound.play()
                    selected = "quit"
                if event.key == pygame.K_SPACE:
                    if selected == "start":
                        pygame.mixer.music.stop()
                        runGame()
                    if selected == "quit":
                        pygame.mixer.music.stop()
                        pygame.quit()
                        quit()

        # 메인메뉴 구성
        drawObject(background2, 0, 0)
        if selected == "start":
            text_start = pygame.image.load('start2.png')
        else:
            text_start = pygame.image.load('start.png')
        if selected == "quit":
            text_quit = pygame.image.load('quit2.png')
        else:
            text_quit = pygame.image.load('quit.png')

        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        gamePad.blit(text_start, (padWidth / 2 - (start_rect[2] / 2), 250))
        gamePad.blit(text_quit, (padWidth / 2 - (quit_rect[2] / 2), 350))
        pygame.display.update()
        clock.tick(60)  # 게임 프레임 60 고정


# 미사일 종류
missile1 = ["paper1.png", "paper2.png", "paper3.png"]
missile2 = ['missile.png', 'missile1.png']  # ehkoo


## 시간 초 세기
def start():
    global gamePad, time_all
    font = pygame.font.Font("BMJUA.ttf", 20)
    time_all = round(pygame.time.get_ticks() / 1000)
    text = font.render(str(time_all)+"초", True, (255, 100, 100))
    gamePad.blit(text, (220, 0))

## 스테이지 표시
def stageShow():
    global gamePad, stage
    font = pygame.font.Font("BMJUA.ttf", 40)
    if stage == 1:
        text = font.render("stage 1", True, (255, 200, 200))
        gamePad.blit(text, (180, 60))
    elif stage == 2:
        text = font.render("stage 2", True, (255, 200, 200))
        gamePad.blit(text, (180, 60))

# 파이터
fighter = [pygame.image.load('fighter0.png'), pygame.image.load('fighter1.png'), pygame.image.load('fighter2.png'),
           pygame.image.load('fighter3.png'),
           pygame.image.load('fighter4.png')]

# 파이터 움직이는 카운트
fighterCount = 0

# 운석 종류
rockImage = ['왓챠.png', '쿠팡.png', '넷플.png', '디즈니.png']
rockImage2 = ['apple.png', 'benz.png', 'bmw.png', 'chanel.png']

# 폭발 소리
explosionSound = ["짤랑.mp3"]


# 운석 맞춘 개수 계산
def writeScore(count):
    global gamePad
    font = pygame.font.Font("BMJUA.ttf", 20)
    text = font.render("파괴한 운석:" + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))


# 운석이 화면 아래로 통과한 개수
def writePassed(count):
    global gamePad
    font = pygame.font.Font("BMJUA.ttf", 20)
    text = font.render("놓친 운석: " + str(count), True, (255, 0, 0))
    gamePad.blit(text, (360, 0))


# 게임 패배 메시지 출력
def writeMessage(text):
    global gamePad, gameOverSound  # 게임오버 소리도 추가함
    textfont = pygame.font.Font("BMJUA.ttf", 80)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()  # 배경음악정지
    gameOverSound.play()  #  게임오버 사운드 재생
    sleep(2)
    pygame.mixer.music.play(-1)  # 배경 음악 재생
    runGame()


# 게임 우승 메시지 출력
def writeMessage2(text):
    global gamePad, winSound
    textfont = pygame.font.Font("BMJUA.ttf", 40)
    text = textfont.render(text, True, (0, 0, 0))
    text2 = textfont.render(str(time_all) + "초 걸렸어요", True, (0, 0, 0))
    textpos = text.get_rect()
    textpos2 = text2.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2)
    textpos2.center = (padWidth / 2, padHeight / 1.5)
    gamePad.blit(text, textpos)
    gamePad.blit(text2, textpos2)
    pygame.display.update()
    pygame.mixer.music.stop()  # 배경음악정지
    winSound.play()  # 승리 사운드 재생
    #sleep(3)
    pygame.time.wait(2000)
    ending()
    #pygame.quit()

def ending():
    global gamePad, ending_img
    gamePad.blit(ending_img, (0, 0))

    pygame.display.update()
    pygame.time.wait(3000)

    pygame.quit()

# 스테이지2 넘어갈때
def stageJump():
    global gamePad, stage, stageSound, levelupSound
    if stage == 2:
        stageSound.play()
        textfont = pygame.font.Font("BMJUA.ttf", 50)
        text = textfont.render('STAGE 2!', True, (255, 0, 0))
        textpos = text.get_rect()
        textpos.center = (padWidth / 2, padHeight / 2)
        gamePad.blit(text, textpos)

## 레벨업
def levelUp():
    global gamePad
    if stage == 2:
        levelupSound.play()
        font = pygame.font.Font("BMJUA.ttf", 80)
        text = font.render("Level Up!!", True, (255, 212, 0))
        textpos = text.get_rect()
        textpos.center = (padWidth / 2, padHeight / 2)
        gamePad.blit(text, textpos)


# 전투기가 운석 충돌시 메시지 출력
def crash():
    global gamePad
    writeMessage("전투기 파괴!")


# 게임 오버 메시지 표시
def gameOver():
    global gamePad
    writeMessage("게임 오버")


## 게임 우승 메시지 표시
def gameEnd():
    global gamePad
    writeMessage2("게임 우승")


# 게임 등장 객체
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

# 기본으로 필요한 변수들
def initGame():
    global gamePad, clock, background, missile, explosion, missileSound, gameOverSound, boss, explosion_boss, colSound, money
    global winSound, selectSound, stageSound, levelupSound,ending_img
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption("FlexShot")  # game name
    background = pygame.image.load("background.png")  # 배경
    missile = pygame.image.load("missile.png")
    explosion = pygame.image.load("explosion.png")
    explosion_boss = pygame.image.load("보스폭발.jpg")
    boss = pygame.image.load("보스.png")  ##
    ending_img = pygame.image.load("ending_img.png")
    # 돈다발 객체
    money = pygame.image.load("bg_money.png")

    # 소리
    winSound = pygame.mixer.Sound("우승.mp3")
    selectSound = pygame.mixer.Sound("선택.mp3")
    stageSound = pygame.mixer.Sound("클리어.mp3")

    levelupSound = pygame.mixer.Sound("레벨업.wav")

    colSound = pygame.mixer.Sound("충돌.mp3")  # 충돌 사운드
    missileSound = pygame.mixer.Sound("짤랑.mp3")  # 미사일 사운드
    gameOverSound = pygame.mixer.Sound("게임오버.mp3")  # 게임 오버 사운드

    clock = pygame.time.Clock()  # 시간 시작


# 게임실행
def runGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, boss, explosion_boss, missile2_stage, missile1_stage
    global fighterCount, stage, i, money, moneyHeight, missileWidth, j

    # 배경 음악 시작
    pygame.mixer.music.load("브금1.mp3")  # 배경음악
    pygame.mixer.music.play(-1)  # 배경음악재생
    ## 스테이지1
    stage = 1

    ## 레벨업 기준
    j = 0
    ## 스테이지2 보스 위치
    bossSize = boss.get_rect().size
    bossWidth = bossSize[0]
    bossHeight = bossSize[1]

    bossX = -100
    bossY = 50
    bossD = "right"  # 오른쪽으로 이동

    # 전투기 형태
    fighterSize = fighter[0].get_rect().size

    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    # 전투기 초기 위치
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterY = 0
    fighterX = 0

    # 무기 좌표 리스트
    missileXY = []

    # 운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]

    ### 보스전 쓸 운석 랜덤 생성
    rock2 = pygame.image.load(random.choice(rockImage2))
    rock2Size = rock2.get_rect().size
    rock2Width = rock2Size[0]
    rock2Height = rock2Size[1]

    # 폭파 소리 랜덤픽
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    # 운석 초기 위치 설정
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    ### 보스전 쓸 운석 초기 위치 설정
    rock2X = random.randrange(0, padWidth - rock2Width)
    rock2Y = 0
    rock2Speed = 2

    # 전투기 미사일에 운석이 맞은경우 변수 초기설정
    isShot = False

    shotCount = 0
    rockPassed = 0

    ## 전투기 미사일에 보스가 맞은경우 변수 초기설정
    isShot2 = False
    shotCount2 = 0

    ### 전투기 미사일에 보스 운석 맞은 경우 변수 초기설정
    isShot3 = False

    # 돈다발 초기 위치 211208 추가
    moneySize = money.get_rect().size
    moneyHeight = moneySize[1]  # 돈다발 객체 높이 가져오기
    moneyHeight = padWidth / 2 + 15  # 초기위치
    money_h = 100

    onGame = False
    while not onGame:  # false 일때 무한 반복
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()  # 프로그램 종료
                sys.exit()

            # 전투기 이동
            if event.type in [pygame.KEYDOWN]:  # 방향키 누를때
                if event.key == pygame.K_LEFT:  # 좌
                    fighterX = fighterX - 10
                elif event.key == pygame.K_RIGHT:  # 우
                    fighterX = fighterX + 10
                elif event.key == pygame.K_UP:  ## 위
                    fighterY = fighterY - 10
                elif event.key == pygame.K_DOWN:  ## 아래
                    fighterY = fighterY + 10

                elif event.key == pygame.K_SPACE:  # 스페이스 누를때
                    missile2_stage = pygame.image.load(random.choice(missile2))  # ehkoo
                    missile1_stage = pygame.image.load(random.choice(missile1))  # money
                    if stage == 1 and j == 0:  # 스테이지별 미사일 사이즈 가져오기 by yjlim
                        missileSize = missile2_stage.get_rect().size
                    else:
                        missileSize = missile1_stage.get_rect().size

                    missileWidth = missileSize[0]
                    missileSound.play()  # 미사일 사운드 재생
                    missileX = x + (fighterWidth / 2) - (missileWidth / 2)  # 발 사 아
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])

                elif event.key == pygame.K_ESCAPE:  # 게임종료 키 ESC
                    pygame.quit()
                    sys.exit()

            if event.type in [pygame.KEYUP]:  # 방향키 안누를때
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:  ##
                    fighterY = 0

        drawObject(background, 0, 0)  # 게임화면 띄움

        # 3개 운석 놓치면 게임오버 #돈다발 객체 높이 변화를 위해 위치 조정 211208
        if rockPassed == 3:
            gameOver()

        # 돈다발 객체 띄움 211208 추가
        drawObject(money, 0, moneyHeight)

        # 전투기 위치 재조정(좌우)
        x = x + fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        ## 전투기 위치 재조정2(상하)
        y = y + fighterY
        if y < 100:
            y = 100
        elif y > padHeight - fighterHeight:
            y = padHeight - fighterHeight

        # 전투기가 운석과 충돌하는지 체크
        if y > rockY - rockHeight and y < rockY + rockHeight:
            if (rockX > x and rockX < x + fighterWidth) or (
                    rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                colSound.play()
                rock = pygame.image.load(random.choice(rockImage))
                rockSize = rock.get_rect().size
                rockWidth = rockSize[0]
                rockHeight = rockSize[1]
                rockX = random.randrange(0, padWidth - rockWidth)
                rockY = 0
                rockPassed += 1
                isshot = False
                moneyHeight += money_h  # 돈다발 객체 위치 조정

        ### 전투기가 보스전 운석과 충돌하는지 체크
        if y > rock2Y - rock2Height and y < rock2Y + rock2Height:
            if (rock2X > x and rock2X < x + fighterWidth) or (
                    rock2X + rock2Width > x and rock2X + rock2Width < x + fighterWidth):
                colSound.play()
                rock2 = pygame.image.load(random.choice(rockImage2))
                rock2Size = rock2.get_rect().size
                rock2Width = rock2Size[0]
                rock2Height = rock2Size[1]
                rock2X = random.randrange(0, padWidth - rock2Width)
                rock2Y = 0
                rockPassed += 1
                isshot = False
                moneyHeight += money_h  # 돈다발 객체 위치 조정

        if fighterCount > 4:
            fighterCount = 0

        gamePad.blit(fighter[fighterCount], (x, y))
        fighterCount = fighterCount + 1

        # 미사일 발사 화면에 그림
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):  # 미사일 반복
                bxy[1] = bxy[1] - 10  # 총알 y:-10이동
                missileXY[i][1] = bxy[1]

                # 미사일이 운석을 맞춘다면
                if bxy[1] < rockY:

                    # 수정 yjlim
                    missile_left = bxy[0]
                    missile_right = bxy[0] + missileWidth
                    rock_left = rockX
                    rock_right = rockX + rockWidth

                    if ((missile_left > rock_left and missile_left < rock_right) or
                    (missile_right > rock_left and missile_right < rock_right) or
                    (rock_left > missile_left and rock_left < missile_right) or
                    (rock_right > missile_left and rock_right < missile_right)):
                        if bxy in missileXY:
                            missileXY.remove(bxy)
                            isShot = True
                            shotCount = shotCount + 1

                ### 미사일이 보스 운석을 맞춘다면 if stage == 2:
                if bxy[1] < rock2Y:

                    missile_left = bxy[0]
                    missile_right = bxy[0] + missileWidth
                    rock2_left = rock2X
                    rock2_right = rock2X + rock2Width

                    # if bxy[0] > rock2X and bxy[0] < rock2X + rock2Width:
                    if ((missile_left > rock2_left and missile_left < rock2_right) or
                    (missile_right > rock2_left and missile_right < rock2_right) or
                    (rock2_left > missile_left and rock2_left < missile_right) or
                    (rock2_right > missile_left and rock2_right < missile_right)):
                        if bxy in missileXY:
                            missileXY.remove(bxy)
                            isShot3 = True
                            shotCount = shotCount + 1

                ## 미사일이 보스를 맞춘다면
                if bxy[1] < bossY:

                    missile_left = bxy[0]
                    missile_right = bxy[0] + missileWidth
                    boss_left = bossX
                    boss_right = bossX + bossWidth

                    # if bxy[0] > bossX and bxy[0] < bossX + bossWidth :
                    if ((missile_left > boss_left and missile_left < boss_right) or
                    (missile_right > boss_left and missile_right < boss_right) or
                    (boss_left > missile_left and boss_left < missile_right) or
                    (boss_right > missile_left and boss_right < missile_right)):
                        if bxy in missileXY:
                            missileXY.remove(bxy)
                            isShot2 = True
                            shotCount2 = shotCount2 + 1

                if bxy[1] <= 0:  # 미사일이 화면 밖으로 탈출시
                    try:
                        missileXY.remove(bxy)  # 미사일 삭제
                    except:
                        pass

        if len(missileXY) != 0:
            for bx, by in missileXY:
                if stage != 1 and j == 1:
                    drawObject(missile1_stage, bx, by)  # 스테이지 2에 미사일 변경 #ehkoo
                else:
                    drawObject(missile2_stage, bx, by)  # 스테이지1
        # 운석 맞춘 점수 표시
        writeScore(shotCount)

        rockY = rockY + rockSpeed  # 운석: 아래로 움직임
        if stage == 2:
            rock2Y = rock2Y + rock2Speed

        # 운석이 지구로 떨어진 경우
        if rockY > padHeight:
            # 랜덤 새로운 운석 생성
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]

            # 운석 초기 위치 설정
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0

            rockPassed = rockPassed + 1  # 운석 지구에 떨어진 횟수 추가
            moneyHeight += money_h  # 돈다발 객체 위치 조정

        ### 보스 운석이 지구로 떨어진 경우
        if rock2Y > padHeight:
            # 랜덤 새로운 운석 생성
            rock2 = pygame.image.load(random.choice(rockImage2))
            rock2Size = rock2.get_rect().size
            rock2Width = rock2Size[0]
            rock2Height = rock2Size[1]

            # 운석 초기 위치 설정
            rock2X = random.randrange(0, padWidth - rock2Width)
            rock2Y = 0

            rockPassed = rockPassed + 1  # 운석 지구에 떨어진 횟수 추가
            moneyHeight += money_h  # 돈다발 객체 위치 조정

        ## 10개 운석 맞추면 스테이지2
        if shotCount == 10:
            i = 2
            stage = 2
        elif shotCount < 10 or shotCount > 10:
            i = 1
        if shotCount == 10 and i == 2:
            stageJump()

        if shotCount == 20:
            j = 1
            levelUp()

        ## 보스 15번 맞추면 게임 끝
        if shotCount2 == 15:
            gameEnd()
        # 놓친 운석 수 표시
        writePassed(rockPassed)

        ## 보스 등장
        if stage == 2:
            drawObject(boss, bossX, bossY)
            if bossD == 'right':
                bossX += 5
                if bossX == 300:
                    bossD = "left"
            elif bossD == "left":
                bossX -= 5
                if bossX == 0:
                    bossD = "right"

        ## 보스를 맞춘경우
        if isShot2:
            drawObject(explosion_boss, bossX, bossY)  # 보스 폭발 그리기
            destroySound.play()  # 운석 폭발 사운드 재생
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot2 = False

            rockSpeed = rockSpeed + 0.05
            if rockSpeed >= 10:
                rockSpeed = 10
        if stage == 2:
            drawObject(rock, rockX, rockY)

        # 운석을 맞춘경우
        if isShot:
            # 운석 폭발시
            drawObject(explosion, rockX, rockY)  # 운석 폭발 그리기

            destroySound.play()  # 운석 폭발 사운드 재생

            # 랜덤하게 새로운 운석 등장
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]

            # 운석 초기 위치 설정
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0

            # (아마 또 터져서 소리날걸 대비해서 미리 음악을 선택한듯)
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))

            isShot = False

            # 운석 맞추면 속도 증가
            rockSpeed = rockSpeed + 0.05
            if rockSpeed >= 10:
                rockSpeed = 10
        drawObject(rock, rockX, rockY)  # 운석그리기

        ### 보스 운석을 맞춘경우 : if stage == 2:
        if isShot3:
            # 운석 폭발시
            drawObject(explosion, rock2X, rock2Y)  # 운석 폭발 그리기

            destroySound.play()  # 운석 폭발 사운드 재생

            # 랜덤하게 새로운 운석 등장
            rock2 = pygame.image.load(random.choice(rockImage2))
            rock2Size = rock2.get_rect().size
            rock2Width = rock2Size[0]
            rock2Height = rock2Size[1]

            # 운석 초기 위치 설정
            rock2X = random.randrange(0, padWidth - rock2Width)
            rock2Y = 0

            # (아마 또 터져서 소리날걸 대비해서 미리 음악을 선택한듯)
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))

            isShot3 = False

            ### 보스 운석 맞추면 속도증가
            rock2Speed = rock2Speed + (random.randint(0, 1) / 10)
            if rock2Speed >= 10:
                rock2Speed = 2

        ### 보스 운석 그리기
        if stage == 2:
            drawObject(rock2, rock2X, rock2Y)

        ## 시간 흐름
        start()

        ## 스테이지 표시
        stageShow()

        pygame.display.update()  # 게임 화면 다시 그림

    pygame.quit()  # 파이게임 끝

initGame()
main_menu()