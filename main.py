import pygame, random, math, os, json, numpy, bezier

pygame.init()

def load_image(filename):
    rawImg = pygame.image.load(filename).convert_alpha()
    brighten = 38
    rawImg.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
    img = pygame.transform.scale(rawImg, [rawImg.get_width() * resolutionScale, rawImg.get_height() * resolutionScale])
    return img

def equalPlusMinus(value1, value2, plusMinus):
    if value1 + plusMinus < value2 or value1 - plusMinus > value2:
        return False
    return True

def angle(A, B, aspectRatio):
    x = B[0] - A[0]
    y = B[1] - A[1]
    angle = math.atan2(-y, x / aspectRatio)
    return angle

resolutionScale = 2
screenX = 0
screenY = 0

WIDTH, HEIGHT = 480*resolutionScale, 270*resolutionScale
icon = pygame.image.load("img/icon.png")

screen = pygame.display.set_mode((WIDTH, HEIGHT),0,256,0,0)
screenS = pygame.Surface((WIDTH + screenX, HEIGHT))
pygame.display.set_caption("Fisherman Tales")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

class Screen:
    def __init__(self):
        self.screenPos = [0,0]

    def mouseButtonDown(self):
        pass

    def mouseButtonUp(self):
        pass

    def keyDown(self, key):
        pass

    def keyUp(self, key):
        pass

    def update(self):
        pass

class MenuScreen(Screen):
    def __init__(self):
        self.screenPos = [0,0]

        print("MENU SCREEN INITIALIZED")
        self.background = load_image("img/menu_bg.png")
        self.backgroundFunny = load_image("img/menu_bg_guy_fall.png")
        self.guyFalling = load_image("img/guy_falling.png")
        self.guyFallingR = self.guyFalling
        self.currentBackground = self.background
        self.startButton = StartButton("img/startButton.png", "img/startButton_pressed.png", [WIDTH//2, HEIGHT//2 - 74])
        self.optionsButton = OptionsButton("img/optionsButton.png", "img/optionsButton_pressed.png", [WIDTH//2, HEIGHT//2 + 61])
        self.chains = load_image("img/buttonChains.png")
        self.chainsRect = self.chains.get_rect()
        self.chainsRect.centerx = WIDTH//2
        self.chainsRect.top = HEIGHT//2 - 50

        self.guyFall = False
        self.gX = 218
        self.gY = 360
        self.angle = 0

        self.gFRect = self.guyFalling.get_rect()
        self.gFRect.left = self.gX
        self.gFRect.top = self.gY

    def mouseButtonDown(self):
        self.startButton.click()
        self.optionsButton.click()

    def mouseButtonUp(self):
        self.startButton.click()
        self.optionsButton.click()
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] > self.gX and mousePos[0] < self.gX + self.gFRect.width and mousePos[1] > self.gY and mousePos[1] < self.gY + self.gFRect.height:
            self.currentBackground = self.backgroundFunny
            self.guyFall = True

    def easterEgg(self):
        self.gX += 1
        self.gY += 2
        self.angle -= 1
        self.guyFallingR  = pygame.transform.rotate(self.guyFalling, self.angle)
        screenS.blit(self.guyFallingR, [self.gX, self.gY])
        if self.gY > HEIGHT:
            self.guyFall = False
        print("FALLIIING", random.randint(10, 1000))

    def update(self):
        screenS.blit(self.currentBackground, [0,0])
        self.startButton.update()
        self.optionsButton.update()
        screenS.blit(self.chains, self.chainsRect)
        if self.guyFall:
            self.easterEgg()


class OptionsScreen(Screen):
    def __init__(self):
        print("OPTIONS SCREEN INITIALIZED")
        self.background = pygame.Surface([WIDTH, HEIGHT])
        self.background.fill((100,100,100))
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("OPTIONS", False, [255,255,255])

    def update(self):
        screenS.blit(self.background, [0,0])
        screenS.blit(self.text, [0,0])

class Fish:
    def __init__(self, region, fishLevels, waterY):
        self.imageNames = [imgName for imgName in os.listdir(f'img/{region}') if imgName.endswith(".png")]

        self.name = random.choice(self.imageNames)
        self.image = load_image(f'img/{region}/{self.name}')
        self.scale = random.uniform(0.8, 1.2)
        self.image = pygame.transform.scale_by(self.image, self.scale)
        self.name = self.name.removesuffix(".png")
        self.levelRange = fishLevels[self.name]
        self.levelRange = [self.levelRange[0] * 200 + waterY, self.levelRange[1] * 200 + waterY]
        
        self.rect = self.image.get_rect()
        self.hitBox = pygame.Surface((10*self.scale,10*self.scale))
        self.hitBoxRect = self.hitBox.get_rect()
        self.hitBox.fill([0,255,255])

        self.showFishLevels = True
        self.showFishHitBox = True
        self.showFishRect = True

        self.x, self.y = random.randint(WIDTH//3, WIDTH + WIDTH//3), random.randint(self.levelRange[0], self.levelRange[1])

        self.rect.center = [self.x, self.y]

        self.angle = 0

        self.direction = random.choice([-1,1])

        self.directionY = random.choice([-1,1])

        self.speed = random.uniform(0.5, 1.2)

        self.caught = False
        self.drop = False
        self.baitPos = [0,0]

        self.upDown = random.choice([-1,1])
        # self.directionY = -1

        if self.direction > 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.turnPos = self.x + random.randint(50,300)*self.direction

    def update(self):
        if not self.caught:
            if self.x < self.turnPos and self.direction < 0:
                self.direction *= -1
                self.image = pygame.transform.flip(self.image, True, False)
                self.turnPos = self.x + random.randint(50,300)*self.direction
                self.directionY = random.choice([-1,1])
                self.upDown = random.choice([-1,1])
            
            if self.x > self.turnPos and self.direction > 0:
                self.direction *= -1
                self.image = pygame.transform.flip(self.image, True, False)
                self.turnPos = self.x + random.randint(50,300)*self.direction
                self.directionY = random.choice([-1,1])
                self.upDown = random.choice([-1,1])
            
            # if self.x < WIDTH//3-1:
            #     self.direction *= -1
            #     self.turnPos = self.x + random.randint(50,300) * self.direction
            #     self.image = pygame.transform.flip(self.image, True, False)
            #     self.directionY = 1
            #     self.upDown = random.choice([-1,1])

            if self.y < self.levelRange[0]:
                self.directionY = 1
                self.upDown = 1
            
            if self.y > self.levelRange[1]:
                self.directionY = -1
                self.upDown = -1

            if self.rect.top <= currentScreen.waterRect.top + 100:
                self.directionY = 1
                self.upDown = random.choice([-1,1])
                # print("OUT OF WATER")
            self.rect.center = [self.x, self.y]

            # self.angle += self.directionY/20
            self.x += self.speed * self.direction
            self.y += self.speed/4 * self.directionY
            # self.y += self.directionY * abs(math.radians(self.angle))
            self.imageR = pygame.transform.rotate(self.image, self.angle)
            self.rectR = self.imageR.get_rect()
            self.rectR.center = [self.x, self.y]

            screenS.blit(self.imageR, self.rectR)
            if self.showFishLevels:
                pygame.draw.aaline(screenS, [255,0,0], [0, self.levelRange[0]], [2000, self.levelRange[0]])
                pygame.draw.aaline(screenS, [0,255,0], [0, self.levelRange[1]], [2000, self.levelRange[1]])
            if self.showFishHitBox:
                screenS.blit(self.hitBox, self.hitBoxRect)
            if self.showFishRect:
                pygame.draw.rect(screenS, [255,0,0], self.rect, 2)
        else:
            # self.caught = True
            if not self.drop:
                # print("BOA", random.randint(100,10000))
                self.x = self.baitPos[0]
                self.y = self.baitPos[1]
                if self.direction == 1:
                    self.imageR = pygame.transform.flip(self.image, True, False)
                else:
                    self.imageR = pygame.transform.flip(self.image, False, False)
                self.imageR = pygame.transform.rotate(self.imageR, -90)
                self.rect.center = [self.x + self.imageR.get_width(), self.y]
                screenS.blit(self.imageR, self.rect)
            else:
                if self.y < currentScreen.waterRect.top:
                    self.y += 3
                    self.x += 2
                    self.rect.center = [self.x, self.y]
                    screenS.blit(self.image, self.rect)
                else:
                    self.drop = False
                    self.caught = False
                    currentScreen.boat.caughtFishIndex = -1
                    currentScreen.isFishing = False
                    screenS.blit(self.image, self.rect)
                

        self.hitBoxRect.centerx = self.rect.centerx + self.rect.width//2*self.direction
        self.hitBoxRect.centery = self.rect.centery
        # pygame.draw.rect(screenS, [255,0,0], self.hitBoxRect)

class Boat:
    def __init__(self):
        global currentScreen
        self.image = load_image("img/boat1.png")
        self.rect = self.image.get_rect()
        self.staticRect = self.image.get_rect()

        self.prut = load_image("img/prut.png")
        self.prutRect = self.prut.get_rect()
        self.prutRect.bottomleft = (self.staticRect.right - 40, self.rect.top + 100)

        self.bait = pygame.Surface((20,20))
        self.bait.fill((0,255,0))
        self.baitRect = self.bait.get_rect()

        self.x = WIDTH//2
        self.y = 0
        self.yM = 0

        self.baitX = 0
        self.baitY = 0

        # 200px = 1m
        self.silonMax = 5
        self.currentSilon = 0

        self.maxDiff = 4
        self.directionY = -1
        self.waveSpeed = 0.2
        self.angle = 0

        self.speed = 1
        
        self.caughtFishIndex = -1
        self.caughtFish = False
        self.fishCount = 0

        self.rect.center = (self.x, self.y)
        self.staticRect.center = (self.x, self.y)
        self.baitRect.center = [self.prutRect.right, self.prutRect.top + 50]

        self.defaultBaitPos = [0,0]
        self.endingPoint = self.baitRect.center

        self.throwingBait = False
        self.gotoPos = [0,0]
        self.fromPos = [0,0]

        self.rollBack = False

        self.a1 = 0
        self.a2 = 90


    def update(self, isFishing, baitSpeed = 0):
        self.defaultY = currentScreen.waterRect.top

        self.x += -self.speed * currentScreen.directionX
        self.y = currentScreen.waterRect.top - 20
        self.defaultBaitPos[0] += -self.speed * currentScreen.directionX

        self.currentSilon = math.dist(self.defaultBaitPos, self.endingPoint)/100

        # print(self.currentSilon)

        if self.angle < -self.maxDiff:
            self.directionY = 1
        if self.angle > self.maxDiff:
            self.directionY = -1
        if self.directionY == 1:
            self.angle += self.waveSpeed
        else:
            self.angle -= self.waveSpeed
        self.imageR = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.imageR.get_rect()
        # self.yM += self.directionY * self.waveSpeed
        self.rect.centerx = self.x + self.angle*-1.3
        self.rect.top = self.y+self.yM-100

        self.staticRect.center = (self.x, self.y)
        # self.baitRect.center = (self.staticRect.centerx + 100 + self.baitX, self.staticRect.centery - 50 + self.baitY)
        self.baitRect.center = [self.prutRect.right + self.baitX, self.prutRect.top + 50 + self.baitY]
        if not isFishing:
            self.baitX = 0
            self.baitY = 0
            # self.defaultBaitPos = [self.staticRect.centerx + 100 + self.baitX, self.staticRect.centery - 50 + self.baitY]
            self.defaultBaitPos = list(self.prutRect.topright)


        if self.throwingBait:
            # if self.baitY < 100:
            # print(self.prutRect.top - 5, currentScreen.waterRect.top)
            if self.baitRect.top - 5 < currentScreen.waterRect.top:
                self.baitY += 1
                # print(self.baitY)
                # if not self.baitRect.colliderect(currentScreen.waterRect):
                self.baitX = self.baitX + math.cos(math.radians(self.baitY*1.2))*5
                # print("MOVING", self.baitY-5 < currentScreen.waterRect.top)
                # print(self.baitX, self.baitY)
                # self.baitX = math.sin(math.radians(self.baitY*4))
                # self.baitRect.center = (self.staticRect.centerx + 100 + self.baitX, self.staticRect.centery - 50 + self.baitY)
                self.baitRect.center = [self.prutRect.right + self.baitX, self.prutRect.top + 50 + self.baitY]
            else:
                self.throwingBait = False
        elif isFishing and not self.rollBack and not self.caughtFish:
            if equalPlusMinus(self.currentSilon, self.silonMax, 0.1):
                if -currentScreen.directionX > 0:
                    currentScreen.directionX = 0
                else:
                    self.baitX -= 0.1
                if -currentScreen.directionY > 0:
                    currentScreen.directionY = 0
                else:
                    self.baitY -= 0.1
            if self.baitX + self.rect.right > self.rect.right:
                self.baitX += -currentScreen.directionX
                pass
            self.baitY += (-currentScreen.directionY + (0 if self.caughtFish else 0.5)) if not equalPlusMinus(self.currentSilon, self.silonMax, 0.1) else 0


        self.endingPoint = self.baitRect.center
        # nodes = numpy.asfortranarray([
        #     [self.defaultBaitPos[0], (self.defaultBaitPos[0] + self.endingPoint[0])/2, self.endingPoint[0]],
        #     [self.defaultBaitPos[1], (self.defaultBaitPos[1] + self.endingPoint[1])/2, self.endingPoint[1]]
        # ])
        # curve = bezier.Curve(nodes, degree=2)

        rect = [self.defaultBaitPos[0] - (self.endingPoint[0]-self.defaultBaitPos[0]),self.defaultBaitPos[1], (self.endingPoint[0]-self.defaultBaitPos[0])*2, (self.endingPoint[1] - self.defaultBaitPos[1])*2]
        # pygame.draw.rect(screenS, [255,0,0],  rect)
        if self.endingPoint[0] - self.defaultBaitPos[0] > 3:
            pygame.draw.arc(screenS, [0,0,0], rect, math.radians(self.a1), math.radians(self.a2), 1)
        else:
            pygame.draw.aaline(screenS, [0,0,0], self.defaultBaitPos, self.endingPoint)

        self.prutRect.bottomleft = (self.staticRect.right - 40, self.rect.top + 100)

        screenS.blit(self.prut, self.prutRect)
        screenS.blit(self.imageR, self.rect)
        if not self.baitRect.colliderect(currentScreen.waterRect) and currentScreen.isFishing and not self.throwingBait and not self.caughtFish and not self.rollBack:
            self.rollBack = True
            self.fromPos = [self.prutRect.right + self.baitX, self.prutRect.top + 50 + self.baitY]
            self.gotoPos = self.defaultBaitPos.copy()
        if not self.caughtFish:
            screenS.blit(self.bait, self.baitRect)
        if self.caughtFish or self.rollBack:
            if not equalPlusMinus(self.baitRect.center[1], self.gotoPos[1] , 4):
                self.fromPos = [self.prutRect.right + self.baitX, self.prutRect.top + 50 + self.baitY]
                direction = (pygame.Vector2(self.gotoPos) - pygame.Vector2(self.fromPos)).normalize()
                self.baitX += direction[0] * 5
                self.baitY += direction[1] * 5
                # print("direction", direction)
                # self.baitRect.center = (self.staticRect.centerx + 100 + self.baitX, self.staticRect.centery - 50 + self.baitY)
            else:
                currentScreen.isFishing = False
                currentScreen.directionY = 0
                self.throwingBait = False
                self.baitRect.center = self.defaultBaitPos.copy()
                if self.caughtFish:
                    if currentScreen.capacity < currentScreen.maxCapacity:
                        self.caughtFish = False
                        currentScreen.fishInventoryDict[currentScreen.fishes[self.caughtFishIndex].name] += 1
                        currentScreen.totalFishAmount += 1
                        print(currentScreen.fishInventoryDict, currentScreen.totalFishAmount)
                        currentScreen.fishes.pop(self.caughtFishIndex)
                        self.caughtFishIndex = -1
                        currentScreen.capacity += 1
                    else:
                        self.caughtFish = False
                        currentScreen.fishes[self.caughtFishIndex].drop = True
                        self.caughtFishIndex = -1
                        currentScreen.isFishing = False
                        currentScreen.boat.caughtFish = False
                elif self.rollBack:
                    self.rollBack = False

class GameScreen(Screen):
    def __init__(self):
        self.boat = Boat()

        self.screenPos = [0, 0]

        self.money = 100
        self.maxCapacity = 10
        self.capacity = 0

        self.background = pygame.Surface([WIDTH - self.screenPos[0], HEIGHT])
        self.background.fill((100,150,100))
        self.water = pygame.Surface([WIDTH + self.screenPos[0], HEIGHT//4], pygame.SRCALPHA)
        self.water.fill((100,100,250))
        self.waterRect = self.water.get_rect()
        self.waterRect.bottomleft = [0, HEIGHT]
        self.water2 = self.water.copy()
        self.water2Rect = self.waterRect.copy()
        self.water2.fill((100,100,250,50))
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("GAME", False, [255,255,255])
        self.region = "tatry"

        levelsJson = open("fishLevels.json")
        self.fishLevels = json.load(levelsJson)

        self.totalFishAmount = 0
        self.fishNames = [imgName for imgName in os.listdir(f'img/{self.region}') if imgName.endswith(".png")]
        self.fishInventoryDict = dict()
        for name in self.fishNames:
            name = name.removesuffix(".png")
            self.fishInventoryDict[name] = 0
        print(self.fishInventoryDict)
        self.fishAmount = 15

        self.fishes = []

        for i in range(self.fishAmount):
            self.fishes.append(Fish(self.region, self.fishLevels, self.waterRect.top))

        # self.block = pygame.Surface([200, 200])
        # self.block.fill((0,0,0))
        # self.blockRect = self.block.get_rect()
        # self.blockRect.center = [10,200]

        self.directionX = 0
        self.directionY = 0
        self.cameraSpeed = 2
        self.defaultBoatX = self.boat.x

        self.leftPressed = False
        self.rightPressed = False
        self.downPressed = False
        self.upPressed = False

        self.correctCameraPos = [self.defaultBoatX, 0]
        self.currentCameraPos = [self.defaultBoatX + self.boat.x, 0]

        self.isFishing = False
        self.fishCollideIndex = -1

        self.fishInventory = FishInventory()
        self.fishInvetoryShow = False

        self.moneyText = self.font.render(f'Money: {self.money}', False, [0,0,0])
        self.moneyRect = self.moneyText.get_rect()
        self.moneyRect.topleft = [10,10]

        self.capacityText = self.font.render(f'Capacity: {self.capacity}/{self.maxCapacity}', False, [0,0,0])
        self.capacityRect = self.capacityText.get_rect()

    def update(self):
        self.currentCameraPos = [self.defaultBoatX + self.screenPos[0], 0]

        self.moneyText = self.font.render(f'Money: {self.money}', False, [0,0,0])
        self.moneyRect = self.moneyText.get_rect()
        self.moneyRect.topleft = [-self.screenPos[0] + 10,-self.screenPos[1] + 10]

        self.capacityText = self.font.render(f'Capacity: {self.capacity}/{self.maxCapacity}', False, [0,0,0])
        self.capacityRect = self.capacityText.get_rect()
        self.capacityRect.topleft = [-self.screenPos[0] + 10,-self.screenPos[1] + 30]

        self.background = pygame.Surface([WIDTH - self.screenPos[0], HEIGHT])
        self.background.fill((100,150,100))

        anyFishDropping = True if (True in [fish.drop for fish in self.fishes]) else False

        if not anyFishDropping:
            if not self.boat.caughtFish:
                self.fishCollideIndex = self.boat.baitRect.collidelist([fish.hitBoxRect for fish in self.fishes])
            if self.fishCollideIndex != -1:
                if self.boat.caughtFishIndex == -1:
                    self.boat.caughtFishIndex = self.fishCollideIndex
                    self.fishes[self.fishCollideIndex].caught = True
                    self.fishes[self.fishCollideIndex].baitPos = self.boat.baitRect.center
                    self.boat.caughtFish = True
                    self.boat.gotoPos = self.boat.defaultBaitPos.copy()
                    self.boat.fromPos = list(self.boat.baitRect.center)
                    # print("CAUGHT!!!")
                elif self.boat.caughtFishIndex == self.fishCollideIndex:                    
                    self.fishes[self.fishCollideIndex].caught = True
                    self.fishes[self.fishCollideIndex].baitPos = self.boat.baitRect.center
                    self.boat.caughtFish = True
                    self.boat.gotoPos = self.boat.defaultBaitPos.copy()
                    self.boat.fromPos = list(self.boat.baitRect.center)
                    # print("CAUGHT!!!")

        if self.isFishing:
            self.screenPos[0] = -self.boat.baitRect.centerx + WIDTH//2
            self.screenPos[1] = -self.boat.baitRect.centery + HEIGHT//2

        if not self.boat.caughtFish:
            for fish in self.fishes:
                if fish.rect.right < 0:
                    self.fishes.remove(fish)
                    self.fishes.append(Fish(self.region, self.fishLevels, self.waterRect.top))
                    self.fishes.append(Fish(self.region, self.fishLevels, self.waterRect.top))

        # print(len(self.fishes))

        # print(equalPlusMinus(111, 100, 10))

        # if -self.screenPos[0] + WIDTH//2 != self.boat.staticRect.centerx and self.directionX == 0:
        if not self.isFishing:
            if not equalPlusMinus(-self.screenPos[0] + WIDTH//2, self.boat.staticRect.centerx, 3) and self.directionX == 0:
                # print("SC")
                if -self.screenPos[0] + WIDTH//2 > self.boat.staticRect.centerx:
                    self.screenPos[0] += 3
                else:
                    self.screenPos[0] -= 3
            if not equalPlusMinus(-self.screenPos[1] + HEIGHT//2, self.boat.staticRect.centery, 3) and self.directionY == 0:
                if - self.screenPos[1] + HEIGHT//2 > self.boat.staticRect.centery:
                    self.screenPos[1] += 3
                else:
                    self.screenPos[1] -= 3
                # print(-self.screenPos[0] + WIDTH//2, self.boat.staticRect.centerx)
                # self.screenPos[0] += 1
            elif equalPlusMinus(-self.screenPos[0] + WIDTH//2, self.boat.staticRect.centerx, 10) and self.directionX == 0:
                self.screenPos[0] = -(self.boat.staticRect.centerx - WIDTH//2)
        else:
            self.cameraSpeed = self.boat.speed
            self.boat.baitRect.center = [-self.screenPos[0] + WIDTH//2, -self.screenPos[1] + HEIGHT//2]
            # print(self.boat.baitRect.center)

        try:
            # print([WIDTH - self.screenPos[0], HEIGHT//4 - self.screenPos[1]])
            self.water = pygame.Surface([WIDTH - self.screenPos[0], HEIGHT//4 - self.screenPos[1]])
            self.water2 = pygame.Surface([WIDTH - self.screenPos[0], HEIGHT//4 - self.screenPos[1]], pygame.SRCALPHA)
        except:
            pass

        if screenY < -500:
            self.water.fill((70,70,220))
        else:
            self.water.fill((100,100,250))
        if screenY < -700:
            self.water.fill((40,40,180))

        self.waterRect = self.water.get_rect()
        self.waterRect2 = self.water2.get_rect()
        self.waterRect.bottomleft = [-self.screenPos[0], HEIGHT - self.screenPos[1]]
        self.waterRect2.bottomleft = [-self.screenPos[0], HEIGHT - self.screenPos[1]]
        self.water2.fill((100,100,250,50))
        # print(self.waterRect.w)

        screenS.blit(self.background, [0,0])
        screenS.blit(self.water, self.waterRect)
        screenS.blit(self.text, [0,0])
        screenS.blit(self.moneyText, self.moneyRect)
        screenS.blit(self.capacityText, self.capacityRect)

        # print(self.screenPos, self.boat.x)
        
        # if self.screenPos[0] + WIDTH >= WIDTH:
        # print("-",self.boat.rect.centerx, "+", WIDTH, "=", -self.boat.staticRect.centerx + WIDTH)
        if -self.boat.staticRect.centerx + WIDTH >= WIDTH//2:
            self.leftPressed = False
            if self.isFishing and self.boat.baitX > 1:
                self.boat.baitX -= 1

        if self.screenPos[1] + HEIGHT >= HEIGHT:
            self.downPressed = False

        if self.leftPressed:
            self.directionX = 1
            self.rightPressed = False
        elif self.rightPressed:
            self.directionX = -1
            self.leftPressed = False
        else:
            self.directionX = 0

        if not self.boat.caughtFish:
            if self.downPressed:
                self.directionY = 1
                self.upPressed = False
            elif self.upPressed:
                self.directionY = -1
                self.downPressed = False
            else:
                self.directionY = 0
        else:
            self.directionX = 0

        self.screenPos[0] += self.directionX * self.cameraSpeed
        self.screenPos[1] += self.directionY * self.cameraSpeed

        # screenS.blit(self.block, self.blockRect)

        for fish in self.fishes:
            fish.update()

        if self.isFishing:
            self.boat.update(self.isFishing, self.screenPos)
        else:
            self.boat.update(self.isFishing)

        screenS.blit(self.water2, self.water2Rect)
        
        if self.fishInvetoryShow:
            self.fishInventory.update()

    def keyDown(self, key):
        if key == pygame.K_a:
            self.leftPressed = True

        if key == pygame.K_d:
            self.rightPressed = True

        if key == pygame.K_s:
            self.upPressed = True
        
        if key == pygame.K_w:
            self.downPressed = True

        if key == pygame.K_i:
            self.fishInvetoryShow = not self.fishInvetoryShow
            if self.isFishing:
                self.fishInvetoryShow = False

        if key == pygame.K_DOWN:
            if not self.fishInvetoryShow:
                self.downPressed = True
            else:
                self.fishInventory.moveDown = True

        if key == pygame.K_UP:
            if not self.fishInvetoryShow:
                self.upPressed = True
            else:
                self.fishInventory.moveUp = True

        if key == pygame.K_SPACE and self.boat.staticRect.centerx != WIDTH//2:
            if not self.fishInvetoryShow:
                if not self.isFishing:
                    self.boat.throwingBait = True
                    self.isFishing = True
                elif not self.boat.throwingBait:
                    self.boat.rollBack = True
                    self.boat.fromPos = list(self.boat.baitRect.center)
                    self.boat.gotoPos = self.boat.defaultBaitPos.copy()
            # self.screenPos[0] = -self.boat.baitRect.centerx + WIDTH//2
            # self.screenPos[1] = -self.boat.baitRect.centery + HEIGHT//2

    def keyUp(self, key):
        if key == pygame.K_a:
            self.leftPressed = False

        if key == pygame.K_d:
            self.rightPressed = False

        if key == pygame.K_s:
            self.upPressed = False
        
        if key == pygame.K_w:
            self.downPressed = False

        if key == pygame.K_DOWN:
            if not self.fishInvetoryShow:
                self.downPressed = False
            else:
                self.fishInventory.moveDown = False

        if key == pygame.K_UP:
            if not self.fishInvetoryShow:
                self.upPressed = False
            else:
                self.fishInventory.moveUp = False

    def mouseButtonDown(self):
        if self.fishInvetoryShow:
            self.fishInventory.click(pygame.mouse.get_pos())

class FishInventory:
    def __init__(self):
        global currentScreen
        self.gapfromScreen = 100
        self.width = WIDTH - self.gapfromScreen
        self.height = HEIGHT - self.gapfromScreen

        self.inventory = pygame.Surface((self.width, self.height))
        self.inventory.fill((100,100,100))
        self.iRect = self.inventory.get_rect()
        self.iRect.center = (WIDTH//2, HEIGHT//2)

        self.container = pygame.Surface((self.width - self.gapfromScreen, self.height * 1.2))
        self.container.fill((50,50,50))
        self.cRect = self.container.get_rect()
        self.cRect.topleft = (self.gapfromScreen//2, self.gapfromScreen//2)

        self.font = pygame.font.Font(size=40)
        
        self.moveDown = False
        self.moveUp = False

        self.itemHeight = 100

        fishPricesJson = open("fishPrices.json")

        self.fishPrices = json.load(fishPricesJson)

        self.items = []

    def click(self, pos):
        cursorRect = pygame.Rect(pos[0], pos[1]-self.iRect.top-self.cRect.top+self.itemHeight, 1, 1)
        collide = cursorRect.collidelist([item.backgroundRect for item in self.items])
        if collide != -1:
            name = self.items[collide].rawName.removesuffix(".png")
            if currentScreen.fishInventoryDict[name] > 0:
                currentScreen.fishInventoryDict[name] -= 1
                currentScreen.money += self.fishPrices[name]
                currentScreen.capacity -= 1


    def update(self):
        # print(self.cy, random.randint(0,1000))
        
        self.iRect.center = (-currentScreen.screenPos[0] + WIDTH//2, -currentScreen.screenPos[1] + HEIGHT//2)

        if self.moveDown and self.cRect.bottom > self.iRect.height - self.gapfromScreen//2:
            self.cRect.topleft = (self.cRect.left, self.cRect.top-3)
        elif self.moveUp and self.cRect.top < self.gapfromScreen//2:
            self.cRect.topleft = (self.cRect.left, self.cRect.top+3)
        else:
            self.cRect.topleft = (self.cRect.left, self.cRect.top)
        # print(self.cRect)

        if len(self.items) == 0:
            for i, fishName in enumerate(currentScreen.fishNames):
                fishImage = load_image(f'img/{currentScreen.region}/{fishName}')
                self.items.append(InventoryItem(self.cRect.w, self.itemHeight, i*self.itemHeight, fishImage, fishName))
        
        self.inventory.fill((100,100,100))

        for i in self.items:
            i.update(self.container)

        self.inventory.blit(self.container, self.cRect)
        # self.inventory.blit(self.money, self.moneyRect)
        screenS.blit(self.inventory, self.iRect)

class InventoryItem:
    def __init__(self, width, height, y, image, name):
        self.rawName = name
        self.name = name.removesuffix(".png")
        self.name = list(self.name.replace("_", " "))
        self.name[0] = self.name[0].upper()
        self.name = "".join(self.name)

        self.width, self.height = width-10, height-5
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((150,150,150))
        self.backgroundRect = self.background.get_rect()
        self.backgroundRect.topleft = (5, y+5)

        self.icon = image.copy()
        self.iconRect = self.icon.get_rect()
        self.iconRect.center = (height//2, height//2)

        self.font = pygame.font.Font(size=40)

        self.nameText = self.font.render(self.name, False, [0,0,0])
        self.nameTextRect = self.nameText.get_rect()
        self.nameTextRect.centerx = width//2
        self.nameTextRect.centery = height//2

        self.amountText = self.font.render(f'Amount: ', False, [0,0,0]) # REPLACE 10 WITH THE ACTUAL VALUE OF THE FISH
        self.amountTextRect = self.amountText.get_rect()
        self.amountTextRect.right = width - 30
        self.amountTextRect.centery = height//2

    def update(self, surf):
        self.amountText = self.font.render(f'Amount: {currentScreen.fishInventoryDict[self.rawName.removesuffix(".png")]}', False, [0,0,0])
        self.amountTextRect = self.amountText.get_rect()
        self.amountTextRect.right = self.width - 30
        self.amountTextRect.centery = self.height//2

        self.background.fill((150,150,150))
        self.background.blit(self.icon, self.iconRect)
        self.background.blit(self.nameText, self.nameTextRect)
        self.background.blit(self.amountText, self.amountTextRect)
        surf.blit(self.background, self.backgroundRect)

        # mousePos = pygame.mouse.get_pos()
        # if mousePos[0] > self.iconRect.left and mousePos[0] < self.iconRect.left + self.iconRect.width and mousePos[1] > self.iconRect.top and mousePos[1] < self.iconRect.top + self.iconRect.height
        #     print(self.name)


class Button:
    def __init__(self, image, clickedImage, pos = [WIDTH//2, HEIGHT//2]):
        self.img = load_image(image)
        self.imgC = load_image(clickedImage)
        self.rect = self.img.get_rect()
        self.rect.center = pos

        self.clicked = False

    def click(self):
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] > self.rect.x and mousePos[0] < self.rect.x + self.rect.width and mousePos[1] > self.rect.y and mousePos[1] < self.rect.y + self.rect.height:
            self.clicked = not self.clicked
        elif self.clicked:
            self.clicked = False

    def update(self):
        self.draw()

    def draw(self):
        if not self.clicked:
            screenS.blit(self.img, self.rect)
        else:
            screenS.blit(self.imgC, self.rect)

class StartButton(Button):
    def click(self):
        global currentScreen
        mousePos = pygame.mouse.get_pos()
        # print(mousePos)
        if mousePos[0] > self.rect.x and mousePos[0] < self.rect.x + self.rect.width and mousePos[1] > self.rect.y and mousePos[1] < self.rect.y + self.rect.height:
            self.clicked = not self.clicked
            if not self.clicked:
                currentScreen = gameScreen
        elif self.clicked:
            self.clicked = False
            currentScreen = gameScreen

class OptionsButton(Button):
    def click(self):
        global currentScreen
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] > self.rect.x and mousePos[0] < self.rect.x + self.rect.width and mousePos[1] > self.rect.y and mousePos[1] < self.rect.y + self.rect.height:
            self.clicked = not self.clicked
            if not self.clicked:
                currentScreen = optionsScreen
        elif self.clicked:
            self.clicked = False
            currentScreen = optionsScreen
 
menuScreen = MenuScreen()
gameScreen = GameScreen()
optionsScreen = OptionsScreen()

currentScreen = menuScreen

running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            currentScreen.mouseButtonDown()
        
        if event.type == pygame.MOUSEBUTTONUP:
            currentScreen.mouseButtonUp()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                currentScreen = menuScreen
            currentScreen.keyDown(event.key)

        if event.type == pygame.KEYUP:
            currentScreen.keyUp(event.key)

    # print((WIDTH - currentScreen.screenPos[0] + 2, HEIGHT - currentScreen.screenPos[1] + 2))
    screenS = pygame.Surface((WIDTH - currentScreen.screenPos[0] + 2, HEIGHT - currentScreen.screenPos[1] + 2))

    screen.fill([255,255,255])

    currentScreen.update()

    screen.blit(screenS, currentScreen.screenPos)

    pygame.display.flip()

pygame.quit()