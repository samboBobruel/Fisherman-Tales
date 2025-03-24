import pygame, random, math, os, json, webbrowser, threading, gc, os, cProfile
from collections.abc import Callable

gc.set_threshold(500)

pygame.init()

pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN, pygame.KEYUP])

def load_image(filename, resolutionScale = 2):
    rawImg = pygame.image.load(filename).convert_alpha()
    brighten = 0
    # rawImg.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD) 
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

def genFishNamesForRarity(fishNames, rarities):
    final = []
    for fishName in fishNames:
        rarity = rarities[fishName]
        for i in range(rarity):
            final.append(fishName)
    return final

def saveData():
    with open("inventorySave.json", "w") as inventoryFile:
        inventoryData = dict()
        inventoryData["inventory"] = currentScreen.fishInventoryDict
        inventoryData["money"] = currentScreen.moneyVisual.money
        json.dump(inventoryData, inventoryFile)

    with open("boatSave.json", "w") as boatFile:
        boatData = dict()
        boatData["boatPos"] = [currentScreen.boat.x, currentScreen.boat.y]
        if currentScreen.isFishing:
            boatData["screenPos"] = [-currentScreen.boat.x + WIDTH//2, -currentScreen.boat.y + HEIGHT//2]
        else:
            boatData["screenPos"] = currentScreen.camera.pos

        json.dump(boatData, boatFile)

    with open("fishDiscovered.json", "w") as fishDFile:
        fishDData = currentScreen.discoveredFishes
        json.dump(fishDData, fishDFile)

def screenSetup():
    global screen, screenBuffer, screenS, WIDTH, HEIGHT, screenX, screenY
    resolutionScale = 2
    screenX = 0
    screenY = 0

    WIDTH, HEIGHT = 480*resolutionScale, 270*resolutionScale
    icon = pygame.image.load("img/icon.png")

    screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.DOUBLEBUF,256,0,0)
    screenBuffer = pygame.Surface((WIDTH, HEIGHT))
    screen.set_alpha(0)
    screenS = pygame.Surface((WIDTH + screenX, HEIGHT))
    screen.set_alpha(0)
    pygame.display.set_caption("Fisherman Tales", "Fisherman Tales")
    pygame.display.set_icon(icon)

screenSetup()

INSTAGRAM_LINK = "https://www.instagram.com"
TWITTER_LINK = "https://www.twitter.com/Fisherman_Tales"

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

    ##########
    #Initialazation functions
    ##########

    def __init__(self):
        self.screenPos = [0,0]

        self.initImg() #Initialize images

        self.initCalcParam() #Initialize calculation parameters for images

    def initImg(self):
        ###################
        # Initializing all images in MenuScreen class
        ###################

        self.background = load_image("img/menu_bg.png") #Menu Background
        self.backgroundFunny = load_image("img/menu_bg_guy_fall.png") #Easter Egg Menu Background 1
        self.guyFalling = load_image("img/guy_falling.png") # 2
        self.guyFallingR = self.guyFalling # 3
        self.currentBackground = self.background #Variable to render correct background when switching to easter egg background

        self.startButton = Button("img/startButton.png", "img/startButton_pressed.png", self.startButtonFunction, [WIDTH//2, HEIGHT//2 - 74]) #Start button in menu
        self.optionsButton = Button("img/optionsButton.png", "img/optionsButton_pressed.png", self.optionsButtonFunction, [WIDTH//2, HEIGHT//2 + 61]) #Options button in menu
        self.chains = load_image("img/buttonChains.png") #Chains connecting the two buttons

        self.instagram = Button("img/instagram.png", "img/instagram.png", self.redirectToInstagram, [WIDTH-60, HEIGHT-60]) #Instagram buttom for fisherman tales instagram site
        self.xLogo = Button("img/x.png", "img/x.png", self.redirectToX, [WIDTH-150, HEIGHT-60]) #X button for fisherman tales x site

    def initCalcParam(self):
        ###################
        # Initializing all needed calculation parameters for MenuScreen class images
        ###################

        ###################
        #Positioning chains 1
        self.chainsRect = self.chains.get_rect()
        self.chainsRect.centerx = WIDTH//2
        self.chainsRect.top = HEIGHT//2 - 50
        ###################

        ###################
        #Easter egg parameters
        self.guyFall = False
        self.gX = 218
        self.gY = 360
        self.angle = 0
        self.gFRect = self.guyFalling.get_rect()
        self.gFRect.left = self.gX
        self.gFRect.top = self.gY
        ###################

    ##########
    #Button functions
    ##########

    def startButtonFunction(self):
        ###################
        # Changing screen to game screen after clicking startButton
        ###################

        global currentScreen
        currentScreen = gameScreen

    def optionsButtonFunction(self):
        ###################
        # Changing screen to options screen after clicking optionsButton
        ###################

        global currentScreen
        currentScreen = optionsScreen

    ##########
    #Link functions
    ##########

    def redirectToInstagram(self):
        ###################
        # Redirecting user to instagram page
        ###################

        global INSTAGRAM_LINK
        webbrowser.open(INSTAGRAM_LINK)

    def redirectToX(self):
        ###################
        # Redirecting user to X page
        ###################

        global TWITTER_LINK
        webbrowser.open(TWITTER_LINK)

    ##########
    #Mouse functions
    ##########

    def mouseButtonDown(self):
        ###################
        # Handler for mouse click event
        ###################

        self.startButton.press()
        self.optionsButton.press()
        self.instagram.press()
        self.xLogo.press()

    def mouseButtonUp(self):
        ###################
        # Handler for mouse release event
        ###################

        self.startButton.click()
        self.optionsButton.click()
        self.instagram.click()
        self.xLogo.click()

        self.easterEggClick()

    ##########
    #Easter egg functions
    ##########

    def easterEggClick(self):
        ###################
        # Trigger for easter egg
        ###################

        mousePos = pygame.mouse.get_pos()
        if mousePos[0] > self.gX and mousePos[0] < self.gX + self.gFRect.width and mousePos[1] > self.gY and mousePos[1] < self.gY + self.gFRect.height:
            self.currentBackground = self.backgroundFunny
            self.guyFall = True

    def easterEgg(self):
        ###################
        # Easter egg handler
        ###################

        self.gX += 1
        self.gY += 2
        self.angle -= 1
        self.guyFallingR  = pygame.transform.rotate(self.guyFalling, self.angle)
        screenS.blit(self.guyFallingR, [self.gX, self.gY])
        if self.gY > HEIGHT:
            self.guyFall = False

    ##########
    #Updation function
    ##########

    def update(self):
        ###################
        # Updating all objects in Menu Screen
        ###################

        screenS.blit(self.currentBackground, [0,0])
        self.startButton.update()
        self.optionsButton.update()
        self.instagram.update()
        self.xLogo.update()
        screenS.blit(self.chains, self.chainsRect)
        if self.guyFall:
            self.easterEgg()

#WORK IN PROGRESS --- WAITING FOR GRAPHICS AND DESIGN
class OptionsScreen(Screen):
    def __init__(self):

        self.background = pygame.Surface([WIDTH, HEIGHT])
        self.background.fill((100,100,100))
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("OPTIONS", False, [255,255,255])

        self.screenPos = [0,0]

    def update(self):
        screenS.blit(self.background, [0,0])
        screenS.blit(self.text, [0,0])

class GameScreen(Screen):

    ##########
    #Initialazation functions
    ##########

    def __init__(self):
        ###################
        # Initializing GameScreen
        ###################

        self.region = "tatry"

        self.initData()

        self.gameObjects()

        self.initImg()

        self.initText()

        self.initCalcParams()

        self.gameParams()

        self.genFishes()

        self.genBackgroundReflections()

    def genFishes(self):
        ###################
        # Generating fishes based on region and level of their spawning
        ###################

        self.totalFishAmount = 0
        self.fishAmount = self.endOfMap//100 + 5

        self.fishes = []

        for i in range(self.fishAmount):
            self.totalFishAmount += 1
            self.fishes.append(Fish(self.region, self.fishLevels, self.water.rect.top, self.endOfMap, self.fishNames))

    def genBackgroundReflections(self):
        ###################
        # Generating reflections on water of the background images
        ###################

        self.backgroundReflections = []
        for bg in self.backgrounds:
            bgReflection = pygame.transform.flip(bg[0], False, True)
            # bgReflection.set_alpha(self.setReflectionAlpha)
            self.backgroundReflections.append(bgReflection)

    def initData(self):
        ###################
        # Data loader
        ###################

        #Boat save file
        self.boatSave = json.load(open("boatSave.json"))

        #Screen position from boat save
        self._screenPos = self.boatSave["screenPos"]

        #Inventory save file
        self.inventorySave = json.load(open("inventorySave.json"))

        #All fish names without suffix .png
        self.originalFishNames = [imgName.removesuffix(".png") for imgName in os.listdir(f'img/{self.region}/fish') if imgName.endswith(".png")]

        #Loading fish inventory from inventory save
        self.fishInventoryDict = self.inventorySave["inventory"]

        #Loading discovered fishes
        self.discoveredFishes = json.load(open("fishDiscovered.json"))

        #Levels at which fishes spawn
        levelsJson = open("fishLevels.json")
        self.fishLevels = json.load(levelsJson)

        #Data on which is calculated how rare it is to encounter a fish
        fishRarityJson = open("fishRarity.json")
        self.fishRarity = json.load(fishRarityJson)

        #Generating fish based on their rarity
        self.fishNames = genFishNamesForRarity(self.originalFishNames, self.fishRarity)

    def initText(self):
        ###################
        # Initiliazing text
        ###################

        self.font = pygame.font.Font("font/pixelFont.ttf", 20)
        self.text = self.font.render("GAME", False, [255,255,255])

    def initImg(self):
        ###################
        # Initializing images and surfaces
        ###################

        #Main game surface. When turning to shops, it's changing gsPosition.
        self.gameScreenS = pygame.Surface((WIDTH, HEIGHT))
        # self.gameScreenS.set_alpha(0)

        #Image containing shopping part of a specified region
        self.shops = load_image(f'img/{self.region}/backgrounds/obchody.png')
        
        #Image cointaing fishing surface part of a specified region
        self.background = load_image(f'img/{self.region}/backgrounds/pozadie.png')

        #Array containing all backgrounds - useful for optimalized rendering
        self.backgrounds = [[self.background.copy(), self.background.get_rect()] for i in range(2)]
        for i in range(len(self.backgrounds)):
            self.backgrounds[i][1].topleft = [i*WIDTH, -270]

        #Harbor image
        self.harbor = load_image(f'img/{self.region}/backgrounds/harbor.png')
        
    def initCalcParams(self):
        ###################
        # Initializing variables and rects required for calculation and rendering
        ###################

        #Calculating end of map
        self.endOfMap = 0
        for i in range(len(self.backgrounds)):
            self.endOfMap += i*WIDTH
        self.endOfMap *= 2

        #Game screen positioning
        self.gsPos = [0,0]

        #Rect for shop part of game and positioning
        self.shopsRect = self.shops.get_rect()
        self.shopsRect.topright = [0,0]

        #Direction of transition between shop and fishing part of game
        self.transition = 0

        #Check for whether the player is viewing shop part or not
        self.showingShops = False

        #Rect for harbor and positioning
        self.harborRect = self.harbor.get_rect()
        self.harborRect.centery = self.water.rect.top - 20
        self.harborRect.left = 0

        #Counter for amount of fish shown
        self.fishShowingCount = 0

    def gameParams(self):
        ###################
        # Parameters used for dynamic changes in game
        ###################

        #Default boat X position
        self.defaultBoatX = self.boat.x

        #Camera position variables
        self.correctCameraPos = [self.defaultBoatX, 0]
        self.currentCameraPos = [self.defaultBoatX + self.boat.x, 0]

        #Checks for key pressing
        self.leftPressed = False #Key A
        self.rightPressed = False #Key D
        self.downPressed = False #Key S
        self.upPressed = False #Key W
        self.usePressed = False #Key E

        #Check for fishing or moving mode
        self.isFishing = False

        #Index for checking if a fish collided with fish that's being pulled out
        self.fishCollideIndex = -1

        #Check for showing inventory
        self.fishInventoryShow = False 

    def gameObjects(self):
        ###################
        # Objects in game
        ###################

        self.camera = Camera(self._screenPos)

        self.boat = Boat()

        self.fishInventory = FishInventory()

        self.moneyVisual = MoneyVisual()
        self.moneyVisual.initData(self.inventorySave["money"])

        self.capacityVisual = CapacityVisual()
        self.capacityVisual.initData(self.originalFishNames, self.fishInventoryDict)

        self.harborTextVisual = HarborTextVisual()

        self.dockingHandler = DockingHandler()

        self.fishHandler = FishHandler()

        self.water = Water()

        self.silonVisual = SilonVisual()

        self.menuButton = Button("img/burgerButton.png", "img/burgerButtonClicked.png", self.openMenu)

    def openMenu(self):
        print("OPENED MENU")

    def stopInput(self):
        self.leftPressed = False
        self.rightPressed = False
        self.topPressed = False
        self.downPressed = False
        self.boat.dirX = 0
        self.camera.dirX = 0
        self.camera.dirY = 0

    ##########
    #Updation functions 
    ##########

    def updateScreen(self):
        self.gameScreenS = pygame.Surface((WIDTH - self.camera.pos[0] + 2, HEIGHT - self.camera.pos[1]))

    def bgRenderHandler(self):
        for i, background in enumerate(self.backgrounds):
            if background[1].right > abs(currentScreen.camera.pos[0]) and background[1].left < WIDTH + abs(currentScreen.camera.pos[0]) and background[1].bottom > abs(currentScreen.camera.pos[1]) and background[1].top < HEIGHT + abs(currentScreen.camera.pos[1]):
                self.gameScreenS.blit(background[0], background[1])

    def updateFish(self):
        for i, fish in enumerate(self.fishes):
            fish.update()

    def drawFish(self):
        for fish in self.fishes:
            if fish.rect.right > abs(self.camera.pos[0]) and fish.rect.left < WIDTH + abs(self.camera.pos[0]):
                if fish.rect.bottom > abs(self.camera.pos[1]) and fish.rect.top < HEIGHT + abs(self.camera.pos[1]):
                    fish.draw()
                elif fish.caught:
                    fish.draw()
            elif fish.caught:
                fish.draw()

    def updateBoat(self):
        if self.isFishing:
            self.boat.update(self.isFishing, self.camera.pos)
        else:
            self.boat.update(self.isFishing)

    def update(self):
        #########
        #Updating Game Screen
        #########

        #Current camera position
        self.currentCameraPos = [self.defaultBoatX + self.camera.pos[0], 0]

        anyFishDropping = True if (True in [fish.drop for fish in self.fishes]) else False

        #Check if you're fishing and there are no falling fishes
        if self.isFishing and not anyFishDropping:
            self.boat.checkFishCollisions()

        #Camera control while fishing
        self.camera.checkCameraBoundsWhileFishing()

        #Fixing camera centering while not fishing
        self.camera.fixCameraCentering()

        self.updateScreen()

        self.bgRenderHandler()

        #Handling docking
        self.dockingHandler.checkDocking()
        if self.boat.dockedIn:
            self.dockingHandler.handleDockingTransition()

        self.fishHandler.outOfBound()
        
        self.fishHandler.keepEnoughFish()

        self.silonVisual.update()

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^ DONE ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        self.water.reflectionRect.topleft = [-self.camera.pos[0]-2,self.water.rect.y + self.boat.staticRect.h/6]

        if not self.isFishing and self.boat.wsFinished:
            self.boat.wsFinished = False

        self.water.renderBackgroundReflections()

        fishUpdateThread = threading.Thread(target=self.updateFish)
        fishDrawThread = threading.Thread(target=self.drawFish)
        boatThread = threading.Thread(target=self.updateBoat)

        boatThread.start()
        fishUpdateThread.start()
        
        boatThread.join()
        fishDrawThread.start()

        if not boatThread.is_alive():
            self.water.renderSurfaceReflections()
            fishUpdateThread.join()
            if not fishUpdateThread.is_alive():
                fishDrawThread.join()

        self.water.adjustSurf()

        if not self.isFishing or not self.boat.wsFinished:
            if self.water.frontReflectionSurfAlpha < 255:
                self.water.frontReflectionSurfAlpha += 13
                print("REFLECT")
            if self.water.bgReflectionAlpha < self.water.setReflectionAlpha:
                self.water.bgReflectionAlpha += 4
        else:
            if self.water.frontReflectionSurfAlpha > 0:
                self.water.frontReflectionSurfAlpha -= 13
            if self.water.bgReflectionAlpha > 0:
                self.water.bgReflectionAlpha -= 4

        self.gameScreenS.blit(self.harbor, self.harborRect)
        screenS.blit(self.shops, self.shopsRect)

        if -self.boat.staticRect.centerx + WIDTH >= WIDTH//2:
            self.leftPressed = False
            if self.isFishing and self.boat.baitX > 1:
                self.boat.baitX -= 1

        if self.boat.x >= self.endOfMap - WIDTH//2:
            self.rightPressed = False

        if self.camera.pos[1] + HEIGHT >= HEIGHT:
            self.downPressed = False

        if not self.boat.rollBack:
            if self.leftPressed:
                self.camera.dirX = 1
                self.rightPressed = False
            elif self.rightPressed:
                self.camera.dirX = -1
                self.leftPressed = False
            else:
                self.camera.dirX = 0

        if not self.boat.caughtFish:
            if self.downPressed:
                self.camera.dirY = -1
                self.upPressed = False
            elif self.upPressed:
                self.camera.dirY = 1
                self.downPressed = False
            else:
                self.camera.dirY = 0
        else:
            self.camera.dirX = 0

        if self.boat.rollBack:
            self.camera.dirY = 0

        if self.camera.pos[0] <= 0 and self.camera.pos[0] - WIDTH >= -self.endOfMap:
            self.camera.pos[0] += self.camera.dirX * (self.boat.speed if (self.boat.staticRect.centerx - abs(self.camera.pos[0])) <= 250 or abs(self.boat.staticRect.centerx - abs(self.camera.pos[0] - WIDTH)) <= 250 else self.camera.speed)
        
        if self.camera.pos[0] > 0:
            self.camera.pos[0] = 0


        self.camera.pos[1] += self.camera.dirY * self.camera.speed

        self.fishShowingCount = 0

        if self.isFishing and self.silonTextOpacity > 5:
            self.gameScreenS.blit(self.silonText, self.silonTextRect)
        else:
            self.silonTextOpacity = 0
        
        if self.fishInventoryShow:
            self.fishInventory.update()

        self.harborTextVisual.draw()

        self.moneyVisual.draw()

        self.capacityVisual.draw()

        self.silonVisual.draw()

        self.menuButton.update(update=True)

        screenS.blit(self.gameScreenS, self.gsPos)

        # if self.transition or self.showingShops:
        #     screenS.blit(self.moneyText, self.moneyRect)

    def keyDown(self, key):
        if not self.boat.throwingBait and (not self.transition and not self.showingShops):
            if key == pygame.K_a:
                self.leftPressed = True

            if key == pygame.K_d:
                self.rightPressed = True
            
            if key == pygame.K_w and self.isFishing:
                self.upPressed = True

            if key == pygame.K_i:
                self.fishInventoryShow = not self.fishInventoryShow
                if self.isFishing or self.boat.dockedIn:
                    self.fishInventoryShow = False

            if key == pygame.K_DOWN:
                if self.fishInventoryShow:
                    self.fishInventory.moveDown = True

            if key == pygame.K_UP:
                if self.fishInventoryShow:
                    self.fishInventory.moveUp = True

        if key == pygame.K_SPACE and (self.isFishing or self.boat.staticRect.centerx != WIDTH//2):
            if not self.fishInventoryShow:
                if not self.isFishing:
                    self.boat.charging = True
                    # self.boat.throwingBait = True
                    # self.isFishing = True
                elif not self.boat.throwingBait and not self.boat.charging:
                    if not self.boat.rollBack:
                        self.boat.rollBack = True
                        self.stopInput()
                    else:
                        self.boat.rollBack = False
                    self.boat.fromPos = list(self.boat.baitRect.center)
                    self.boat.gotoPos = self.boat.defaultBaitPos.copy()

        if key == pygame.K_e:
            self.usePressed = not self.usePressed
            # self.camera.pos[0] = -self.boat.baitRect.centerx + WIDTH//2
            # self.camera.pos[1] = -self.boat.baitRect.centery + HEIGHT//2

    def keyUp(self, key):
        if key == pygame.K_a:
            self.leftPressed = False

        if key == pygame.K_d:
            self.rightPressed = False

        if key == pygame.K_w:
            self.upPressed = False
        
        if key == pygame.K_w:
            self.downPressed = False

        if key == pygame.K_DOWN:
            if not self.fishInventoryShow:
                self.downPressed = False
            else:
                self.fishInventory.moveDown = False

        if key == pygame.K_UP:
            if not self.fishInventoryShow:
                self.upPressed = False
            else:
                self.fishInventory.moveUp = False
        
        if key == pygame.K_SPACE:
            if self.boat.charging:
                self.boat.charging = False
                self.boat.throwingBait = True
                self.isFishing = True

    def mouseButtonDown(self):
        if self.fishInventoryShow:
            self.fishInventory.click(pygame.mouse.get_pos())
        else:
            self.menuButton.press()

    def mouseButtonUp(self):
        if not self.fishInventoryShow:
            self.menuButton.click()

    def mouseScroll(self, e):
        if self.fishInventoryShow:
            self.fishInventory.scroll(e)

class Water:
    def __init__(self):
        #Water texture tile WORK IN PROGRESS!!!
        self.waterTexture = load_image('img/waterTexture.png')

        #Water surface
        self.surf = pygame.Surface([WIDTH, 162], pygame.SRCALPHA)
        self.surf.fill((46,166,204))

        #Rect for water and positioning
        self.rect = self.surf.get_rect()
        self.rect.bottomleft = [0, HEIGHT]

        #Surface used to render reflections of objects like backgrounds, boat etc.
        self.frontReflectionSurf = pygame.Surface((WIDTH + 4, HEIGHT))
        self.frontReflectionSurf.fill((46,166,204))

        #Reflection rect and positioning
        self.reflectionRect = self.frontReflectionSurf.get_rect()
        self.reflectionRect.topleft = [0,0]

        #Reflection opacity variables
        self.setReflectionAlpha = 80
        self.frontReflectionSurfAlpha = 255
        self.reflectionAlpha = 80
        self.bgReflectionAlpha = 80

    def adjustSurf(self):
        self.surf = pygame.Surface([WIDTH - currentScreen.camera.pos[0], 162 - currentScreen.camera.pos[1]])
        
        self.surf.fill((46,166,204))

        self.rect = self.surf.get_rect()
        self.rect.bottomleft = [0, HEIGHT - currentScreen.camera.pos[1]]

    def renderBackgroundReflections(self):
        currentScreen.backgroundReflections = []
        for bg in currentScreen.backgrounds:
            bgReflection = pygame.transform.flip(bg[0], False, True)

            bgReflection.set_alpha(self.setReflectionAlpha)

            currentScreen.backgroundReflections.append(bgReflection)

        for i, bgR in enumerate(currentScreen.backgroundReflections):
            bgR.set_alpha(self.bgReflectionAlpha)
            self.surf.blit(bgR, [WIDTH*i, -160 + 70])

        currentScreen.gameScreenS.blit(self.surf, self.rect)

    def renderSurfaceReflections(self):

        boatReflection = pygame.transform.flip(currentScreen.boat.imageR, False, True)

        self.frontReflectionSurf.fill((46,166,204))

        bgShowing = 0
        for i, bgR in enumerate(currentScreen.backgroundReflections):
            if i*WIDTH - WIDTH <= -currentScreen.camera.pos[0] or i*WIDTH >= -currentScreen.camera.pos[0]:
                bgShowing += 1
                boatReflectionRect = boatReflection.get_rect()
                boatReflectionRect.left = currentScreen.boat.rect.left-WIDTH*i
                boatReflectionRect.top = 160-77
                bgR.blit(boatReflection, boatReflectionRect)
                self.frontReflectionSurf.blit(bgR, [WIDTH*i + currentScreen.camera.pos[0] + 2, -185 + 77])
        self.frontReflectionSurf.set_alpha(self.frontReflectionSurfAlpha)
        currentScreen.gameScreenS.blit(self.frontReflectionSurf, self.reflectionRect)


class Camera:
    def __init__(self, pos):
        ############
        #Variables for camera positioning and movement
        ############


        self.dirX = 0
        self.dirY = 0
        self.speed = 2
        self.pos = pos
        self.cameraOutOfBounds = False

    def ensureCameraBounds(self):
        ############
        #Ensure that camera doesn't go out of map
        ############

        if self.cameraOutOfBounds:
            self.pos[0] = -(currentScreen.endOfMap - WIDTH)
        else:
            self.pos[0] = -currentScreen.boat.baitRect.centerx + WIDTH//2
        self.pos[1] = -currentScreen.boat.baitRect.centery + HEIGHT//2
        if self.pos[1] > 0:
            self.pos[1] = 0

    def checkCameraBoundsWhileFishing(self):
        ############
        #Check if camera is going out of bounds
        ############

        if not currentScreen.isFishing:
            return
        if currentScreen.boat.baitRect.centerx + WIDTH//2 > currentScreen.endOfMap:
            self.cameraOutOfBounds = True
        elif currentScreen.boat.baitRect.centerx + WIDTH//2 < currentScreen.endOfMap:
            self.cameraOutOfBounds = False

        self.ensureCameraBounds()

    def fixCameraCentering(self):
        #############
        #Fixing camera centering while not fishing
        #############

        if currentScreen.isFishing:
            return

        if (not equalPlusMinus(-self.pos[0] + WIDTH//2, currentScreen.boat.staticRect.centerx, 3) and self.dirX == 0):
            if -self.pos[0] + WIDTH//2 > currentScreen.boat.staticRect.centerx:
                self.pos[0] += 3
            else:
                self.pos[0] -= 3
        if not currentScreen.boat.dockedIn:
            if not equalPlusMinus(-self.pos[1] + HEIGHT//2, currentScreen.boat.staticRect.centery - 138, 3) and self.dirY == 0:
                if -self.pos[1] + HEIGHT//2 > currentScreen.boat.staticRect.centery - 138:
                    self.pos[1] += 3
                else:
                    self.pos[1] -= 3
            elif equalPlusMinus(-self.pos[0] + WIDTH//2, currentScreen.boat.staticRect.centerx, 10) and self.dirX == 0:
                self.pos[0] = -(currentScreen.boat.staticRect.centerx - WIDTH//2)
        else:
            if self.pos[1] < 0:
                self.pos[1] += 3
        
        if self.pos[1] > 0:
            self.pos[1] = 0

class HarborTextVisual:
    def __init__(self):
        #############
        #Initialization of font, text, opacity and rect
        #############

        self.font = pygame.font.Font("font/pixelFont.ttf", 70)
        self.text = self.font.render("Harbor", False, (255,255,255)).convert_alpha()

        self.textOpacity = 0
        self.text.set_alpha(self.textOpacity)

        self.rect = self.text.get_rect()
        self.rect.center = [WIDTH//2, 150]

    def appear(self):
        ###########
        #Handler for making harbor text visible
        ###########


        if self.textOpacity < 255:
            self.textOpacity += 5
        else:
            self.textOpacity = 255

        self.updateText()

    def disappear(self):
        #############
        #Handler for making harbor text visible
        #############

        if self.textOpacity > 0:
            self.textOpacity -= 5
        else:
            self.textOpacity = 0

        self.updateText()
        
    def updateText(self):
        #############
        #Updating text opacity
        #############

        self.text.set_alpha(self.textOpacity)

    def draw(self):
        #############
        #Rendering text if visible
        #############

        if self.textOpacity > 0:
            currentScreen.gameScreenS.blit(self.text, self.rect)

class MoneyVisual:
    def __init__(self):
        #########
        #Initializing font, money value and money bar img
        #########

        self.font = pygame.font.Font("font/pixelFont.ttf", 20)

        self.background = load_image("img/moneyBar.png")
        self.rect = self.background.get_rect()

    def initData(self, money):
        ########
        #Loading money and formatting it
        ########

        self.money = money        
    
        self.formattedText = self.money
        self.formatMoney()

    def add(self, amount):
        #########
        #Adding parameter amount to money
        #########

        self.money += amount
        self.formatMoney()

    def remove(self, amount):
        #########
        #Removing parameter amount from money
        #########

        self.money -= amount
        self.formatMoney()

    def formatMoney(self):
        #########
        #Formating money for rendering
        #########

        if self.money > 1000000:
            self.formattedText = str(int(self.money/1000000*10)/10) + "M"
        elif self.money > 1000:
            self.formattedText = str(int(self.money/1000*10)/10) + "K"
        
        self.updateText()

    def updateText(self):
        #########
        #Updating money text after formatting
        #########

        self.text = self.font.render(f'{self.formattedText}¢', False, [227,188,15])

    def draw(self):
        #########
        #Positioning and rendering money bar and money text
        #########

        self.rect.topleft = [-currentScreen.camera.pos[0] + 10, -currentScreen.camera.pos[1] + 10]

        currentScreen.gameScreenS.blit(self.background, self.rect)
        moneyTextPos = self.rect.center
        moneyTextRect = self.text.get_rect()
        moneyTextRect.center = moneyTextPos
        moneyTextRect.left += 2
        currentScreen.gameScreenS.blit(self.text, moneyTextRect)

class CapacityVisual:
    def __init__(self):
        self.font = pygame.font.Font("font/pixelFont.ttf", 20)

        self.background = load_image("img/moneyBar.png")
        self.rect = self.background.get_rect()

        self.maxCapacity = 10
        self.capacity = 0

    def initData(self, originalFishNames, fishInventoryDict):
        for name in originalFishNames:
            if fishInventoryDict[name] > 0:
                self.capacity += fishInventoryDict[name]

        self.updateText()

    def updateText(self):
        self.text = self.font.render(f'{self.capacity}/{self.maxCapacity}', False, [227,188,15])

    def add(self):
        self.capacity += 1
        self.updateText()

    def remove(self):
        self.capacity -= 1
        self.updateText()

    def draw(self):
        self.rect.topleft = [-currentScreen.camera.pos[0] + 10,-currentScreen.camera.pos[1] + 45]

        self.rect.top += 5
        currentScreen.gameScreenS.blit(self.background, self.rect)
        capacityTextPos = self.rect.center
        capacityTextRect = self.text.get_rect()
        capacityTextRect.center = capacityTextPos
        currentScreen.gameScreenS.blit(self.text, capacityTextRect)
        
class SilonVisual:
    def __init__(self):
        self.font = pygame.font.Font("font/pixelFont.ttf", 70)
        self.text = self.font.render("Out of line", False, [255,255,255])

        self.rect = self.text.get_rect()

        self.opacity = 0
        self.fade = 0

        self.outOfSilon = False
    
    def fadeHandler(self):
        if self.opacity > 200:
            self.fade = -10
        elif self.opacity < 50 and self.outOfSilon:
            self.fade = 10

        if self.opacity >= 0:
            self.opacity += self.fade
        else:
            self.opacity = -1

    def update(self):
        self.fadeHandler()

        self.rect.center = (currentScreen.boat.baitRect.centerx, currentScreen.boat.baitRect.centery - 100)
        self.text.set_alpha(self.opacity)

    def draw(self):
        currentScreen.gameScreenS.blit(self.text, self.rect)

class WaterSplash:
    def __init__(self, pos = [100,100], sizeX = -1, sizeY = -1):
        self.imageNames = [imgName for imgName in os.listdir(f'img/waterSplash') if imgName.endswith(".png")]
        self.images = [load_image(f'img/waterSplash/{img}') for img in self.imageNames]

        if sizeX != -1 and sizeY != -1:
            for img in self.images:
                _img = img
                img = pygame.transform.scale(img, [sizeX, img.get_rect().h * sizeY])
                self.images[self.images.index(_img)] = img

        self.count = 0
        self.index = 0
        self.finished = False
        self.pos = [pos[0] - self.images[0].get_rect().w//2, pos[1] - self.images[0].get_rect().h]
    
    def update(self):
        self.count += 1

        if self.count == 5:
            self.count = 0
            if self.index < len(self.images) - 1:
                self.index += 1
            else:
                self.finished = True

        currentScreen.gameScreenS.blit(self.images[self.index], list(self.pos))

class Fish:
    def __init__(self, region, fishLevels, waterY, endOfMap, fishNames): 
        self.imageNames = fishNames
        self.fishWeights = json.load(open("fishWeight.json"))

        self.name = f'{random.choice(self.imageNames)}.png'
        self.image = load_image(f'img/{region}/fish/{self.name}')
        self.scale = random.uniform(0.8, 1.2)
        self.image = pygame.transform.scale_by(self.image, self.scale)
        self.weight = self.scale * self.fishWeights[self.name.removesuffix(".png")]
        self.name = self.name.removesuffix(".png")
        self.levelRange = fishLevels[self.name]
        self.levelRange = [self.levelRange[0] * 100 + waterY, self.levelRange[1] * 100 + waterY]

        self.rect = self.image.get_rect()
        self.hitBox = pygame.Surface((10*self.scale,10*self.scale))
        self.hitBoxRect = self.hitBox.get_rect()
        self.hitBox.fill([0,255,255])

        self.showFishLevels = False
        self.showFishHitBox = False
        self.showFishRect = False

        self.x, self.y = random.randint(WIDTH//2, endOfMap), random.uniform(self.levelRange[0], self.levelRange[1])

        self.rect.center = [self.x, self.y]

        self.angle = 0

        self.direction = random.choice([-1,1])

        self.directionY = random.choice([-1,1])

        self.speed = random.uniform(0.5, 1.2)

        self.scared = False
        self.caught = False
        self.drop = False
        self.baitPos = [0,0]

        self.escapeSpeed = 2.7
        self.currentSpeed = self.speed

        self.upDown = random.choice([-1,1])
        # self.directionY = -1

        if self.direction > 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.turnPos = self.x + random.randint(50,300)*self.direction

        self.ws = None

    def scare(self, caughtFishRect: pygame.Rect):
        if not self.scared:
            self.currentSpeed = self.escapeSpeed
            if caughtFishRect.centerx > self.rect.centerx:
                if self.direction == 1:
                    self.changeDirectionX(direction = -1, turnPosDis = 200)
            else:
                if self.direction == -1:
                    self.changeDirectionX(direction = 1, turnPosDis = 200)

            if caughtFishRect.centery > self.rect.centery:
                self.changeDirectionY(-1)
            else:
                self.changeDirectionY(1)
                
        if self.name != "green_Fish" or self.name != "purple_Fish":
            self.scared = True

    def changeDirectionX(self, direction = 0, turnPosDis = None):
        if direction == 0:
            self.direction *= -1
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            if self.direction != direction:
                self.image = pygame.transform.flip(self.image, True, False)
            self.direction = direction
        if turnPosDis == None:
            self.turnPos = self.x + random.randint(50,300)*self.direction
        else:
            self.turnPos = self.x + turnPosDis * self.direction
        self.directionY = random.choice([-1,1])
        self.upDown = random.choice([-1,1])

    def changeDirectionY(self, direction = 0):
        if direction == 0:
            self.directionY = random.choice([-1,1])
        else:
            self.directionY = direction

    def update(self):
        global currentScreen

        if not self.caught:
            if not self.scared:
                if self.x < self.turnPos and self.direction < 0:
                    self.changeDirectionX()
                
                if self.x > self.turnPos and self.direction > 0:
                    self.changeDirectionX()
            else:
                if self.currentSpeed > self.speed:
                    self.currentSpeed -= 0.01
                else:
                    self.currentSpeed = self.speed
                    self.scared = False

            if self.y < self.levelRange[0]:
                self.directionY = 1
                self.upDown = 1
            
            if self.y > self.levelRange[1]:
                self.directionY = -1
                self.upDown = -1

            if self.rect.top <= currentScreen.water.rect.top + 100:
                self.directionY = 1
                self.upDown = random.choice([-1,1])
            self.rect.center = [self.x, self.y]

            # self.angle += self.directionY/20
            self.x += self.currentSpeed * self.direction
            self.y += self.currentSpeed/(2 if self.scared else 4) * self.directionY
            # self.y += self.directionY * abs(math.radians(self.angle))
            self.imageR = pygame.transform.rotate(self.image, self.angle)
            self.rectR = self.imageR.get_rect()
            self.rectR.center = [self.x, self.y]

            if not self.caught and not self.drop and self.rectR.top + 5 < currentScreen.water.rect.top:
                if self.ws == None:
                    self.ws = WaterSplash(self.rectR.center, self.rectR.width * 2.5, self.scale)

            if not self.ws == None:
                if not self.ws.finished:
                    self.ws.update()
                else:
                    self.ws = None

                

        self.hitBoxRect.centerx = self.rect.centerx + self.rect.width//2*self.direction
        self.hitBoxRect.centery = self.rect.centery
        # pygame.draw.rect(screenS, [255,0,0], self.hitBoxRect)

    def draw(self):
        if not self.caught:
            if self.rect.right > abs(currentScreen.camera.pos[0]) and self.rect.left < WIDTH + abs(currentScreen.camera.pos[0]):
                if self.rect.bottom > abs(currentScreen.camera.pos[1]) and self.rect.top < HEIGHT + abs(currentScreen.camera.pos[1]):
                    if currentScreen.isFishing or self.drop:
                        currentScreen.gameScreenS.blit(self.imageR, self.rectR)
                        currentScreen.fishShowingCount += 1
            if self.showFishLevels:
                pygame.draw.aaline(currentScreen.gameScreenS, [255,0,0], [0, self.levelRange[0]], [2000, self.levelRange[0]])
                pygame.draw.aaline(currentScreen.gameScreenS, [0,255,0], [0, self.levelRange[1]], [2000, self.levelRange[1]])
            if self.showFishHitBox:
                currentScreen.gameScreenS.blit(self.hitBox, self.hitBoxRect)
            if self.showFishRect:
                pygame.draw.rect(currentScreen.gameScreenS, [255,0,0], self.rect, 2)
        else:
            if not self.drop:
                self.x = self.baitPos[0]
                self.y = self.baitPos[1]
                if self.direction == 1:
                    self.imageR = pygame.transform.flip(self.image, True, False)
                else:
                    self.imageR = pygame.transform.flip(self.image, False, False)
                self.imageR = pygame.transform.rotate(self.imageR, -90)
                self.rect.center = [self.x + self.imageR.get_width(), self.y]
                currentScreen.gameScreenS.blit(self.imageR, self.rect)
            else:
                if self.y < currentScreen.water.rect.top:
                    self.y += 3
                    self.x += 2
                    self.rect.center = [self.x, self.y]
                    currentScreen.gameScreenS.blit(self.image, self.rect)
                else:
                    self.drop = False
                    self.caught = False
                    currentScreen.boat.caughtFishIndex = -1
                    currentScreen.gameScreenS.blit(self.image, self.rect)
                    currentScreen.isFishing = False

class Boat:
    def __init__(self):
        global currentScreen
        self.image = load_image("img/boat1.png", 2.25)
        self.imageR = self.image.copy()
        self.rect = self.image.get_rect()
        self.staticRect = self.image.get_rect()

        self.prut = load_image("img/prut.png")
        self.prutRect = self.prut.get_rect()
        self.prutRect.bottomleft = (self.staticRect.right - 40, self.rect.top + 100)

        # self.bait = pygame.Surface((20,20))
        self.bait = load_image("img/bait.png")
        # self.bait.fill((0,255,0))
        self.baitRect = self.bait.get_rect()

        self.baitStartFall = False
        self.baitFallingAfterRollback = False

        self.ws = None
        self.wsFinished = False

        self.x, self.y = json.load(open("boatSave.json"))["boatPos"]
        self.yM = 0

        self.baitX = 0
        self.baitY = 0

        # 200px = 1m
        self.silonMax = 15 + 0.7
        self.currentSilon = 0

        self.maxDiff = 3
        self.directionY = -1
        self.waveSpeed = 0.1
        self.angle = 0

        self.speed = 1
        
        self.caughtFishIndex = -1
        self.caughtFish = False
        self.fishCount = 0

        self.rect.center = (self.x, self.y)
        self.staticRect.center = (self.x, self.y)
        self.baitRect.center = [self.prutRect.right, self.prutRect.top + 50]

        self.depthText = pygame.Surface((20,20))
        self.depthTextRect = self.depthText.get_rect()
        self.depthTextRect.center = [self.baitX, self.baitY + 50]

        self.defaultBaitPos = [0,0]
        self.endingPoint = self.baitRect.center

        self.chargingBar = pygame.Rect(self.staticRect.left, self.staticRect.top, 100, 20)

        self.charging = False
        self.minThrowPower = -2
        self.throwPower = self.minThrowPower
        self.throwingBait = False
        self.gotoPos = [0,0]
        self.fromPos = [0,0]

        self.rollBack = False

        self.a1 = 0
        self.a2 = 90

        self.dockedIn = False

        self.scareRadius = pygame.Rect(0, 0, 400, 300)

    def update(self, isFishing, baitSpeed = 0):
        self.defaultY = currentScreen.water.rect.top + 200

        self.x += -self.speed * currentScreen.camera.dirX
        self.y = currentScreen.water.rect.top + self.rect.height//2 - self.rect.height//5
        self.defaultBaitPos[0] += -self.speed * currentScreen.camera.dirX

        self.currentSilon = math.dist(self.defaultBaitPos, self.endingPoint)/100

        if self.currentSilon > self.silonMax-0.2:
            currentScreen.silonVisual.outOfSilon = True
        else:
            currentScreen.silonVisual.outOfSilon = False

        depth = int(((self.defaultBaitPos[1] + self.baitY)/100-2.7)*10)/10
        if depth < 0:
            depth = 0
        self.depthText = currentScreen.font.render(f'{depth}m', False, (255,255,255))
        self.depthTextRect = self.depthText.get_rect()
        self.depthTextRect.center = [self.baitRect.centerx, self.baitRect.centery + 50]

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
        self.baitRect.center = [self.prutRect.right + self.baitX, self.prutRect.top + 50 + self.baitY]
        if not currentScreen.isFishing:
            self.baitX = 0
            
            if not self.baitStartFall:
                self.baitY = -35
                self.baitStartFall = True
            
            if self.baitY < 0:
                self.baitFallingAfterRollback = True
            else:
                self.baitFallingAfterRollback = False
            # self.baitFallingAfterRollback = True if self.baitY < 0 else False
            # self.defaultBaitPos = [self.staticRect.centerx + 100 + self.baitX, self.staticRect.centery - 50 + self.baitY]
            self.defaultBaitPos = list(self.prutRect.topright)

            if self.baitFallingAfterRollback:
                self.baitY += 1

        if self.charging:
            self.throwPower += 0.05
            if self.throwPower >= 2:
                self.throwPower = 2
                self.charging = False
                self.throwingBait = True
                currentScreen.isFishing = True
        elif not self.throwingBait:
            self.throwPower = self.minThrowPower

        if self.throwingBait:
            if self.baitRect.top - 5 < currentScreen.water.rect.top:

                self.baitY += 3 - self.throwPower


                self.baitX = self.baitX + math.cos(math.radians(self.baitY*0.70))*(6 + self.throwPower)

                self.baitRect.center = [self.prutRect.right + self.baitX, self.prutRect.top + 50 + self.baitY]
            else:
                self.throwingBait = False
            
            if self.baitRect.top + 10 >= currentScreen.water.rect.top:
                if self.ws == None:
                    self.ws = WaterSplash([self.baitRect.centerx, self.baitRect.centery+self.baitRect.h])
        elif isFishing and not self.rollBack and not self.caughtFish:
            if equalPlusMinus(self.currentSilon, self.silonMax, 0.1):
                if -currentScreen.camera.dirX > 0:
                    currentScreen.camera.dirX = 0
                else:
                    self.baitX -= 0.1
                if -currentScreen.camera.dirY > 0:
                    currentScreen.camera.dirY = 0
                else:
                    self.baitY -= 0.1
            if self.baitRect.right < currentScreen.endOfMap - 150:
                if self.baitX + self.staticRect.right > self.staticRect.right:
                    self.baitX += -currentScreen.camera.dirX
                    pass
                else:
                    if currentScreen.rightPressed:
                        self.baitX += -currentScreen.camera.dirX

            # self.baitY += (-currentScreen. + (0 if self.caughtFish else 0.75)) if not equalPlusMinus(self.currentSilon, self.silonMax, 0.1) else 0
            self.baitY += (-1.5 if currentScreen.camera.dirY > 0 else 1) if not equalPlusMinus(self.currentSilon, self.silonMax, 0.1) else 0


        self.endingPoint = self.baitRect.center
        # nodes = numpy.asfortranarray([
        #     [self.defaultBaitPos[0], (self.defaultBaitPos[0] + self.endingPoint[0])/2, self.endingPoint[0]],
        #     [self.defaultBaitPos[1], (self.defaultBaitPos[1] + self.endingPoint[1])/2, self.endingPoint[1]]
        # ])
        # curve = bezier.Curve(nodes, degree=2)

        rect = [self.defaultBaitPos[0] - (self.endingPoint[0]-self.defaultBaitPos[0]),self.defaultBaitPos[1], (self.endingPoint[0]-self.defaultBaitPos[0])*2, (self.endingPoint[1] - self.defaultBaitPos[1])*2]
        # pygame.draw.rect(screenS, [255,0,0],  rect)
        if self.endingPoint[0] - self.defaultBaitPos[0] > 3:
            pygame.draw.arc(currentScreen.gameScreenS, [255,255,255], rect, math.radians(self.a1), math.radians(self.a2), 2)
            # pygame.draw.aaline(currentScreen.gameScreenS, [0,0,0], self.defaultBaitPos, self.endingPoint)
        else:
            pygame.draw.aaline(currentScreen.gameScreenS, [255,255,255], self.defaultBaitPos, self.endingPoint)
            pygame.draw.aaline(currentScreen.gameScreenS, [255,255,255], [self.defaultBaitPos[0] + 1, self.defaultBaitPos[1]], [self.endingPoint[0] + 1, self.endingPoint[1]])

        self.prutRect.bottomleft = (self.staticRect.right - 40, self.rect.top)

        currentScreen.gameScreenS.blit(self.prut, self.prutRect)
        currentScreen.gameScreenS.blit(self.imageR, self.rect)
        self.chargingBar.left = self.prutRect.left
        self.chargingBar.top = self.prutRect.top - 30
        self.chargingBar.width = 100 * ((self.throwPower+2) / 4)
        if not currentScreen.isFishing:
            pygame.draw.rect(currentScreen.gameScreenS, [0,255,0], self.chargingBar)
        if isFishing and not self.caughtFish:
            currentScreen.gameScreenS.blit(self.depthText, self.depthTextRect)
        if not self.baitRect.colliderect(currentScreen.water.rect) and currentScreen.isFishing and not self.throwingBait and not self.caughtFish and not self.rollBack:
            self.rollBack = True

            currentScreen.stopInput()

            self.fromPos = [self.prutRect.right + self.baitX, self.prutRect.top + 50 + self.baitY]
            self.gotoPos = self.defaultBaitPos.copy()
        if not self.caughtFish:
            currentScreen.gameScreenS.blit(self.bait, self.baitRect)

        if not self.ws == None:
            if not self.ws.finished:
                self.ws.update()
            else:
                self.ws = None
                self.wsFinished = True

        if self.caughtFish or self.rollBack:
            if not equalPlusMinus(self.baitRect.center[1], self.gotoPos[1] , 4):
                self.fromPos = [self.prutRect.right + self.baitX, self.prutRect.top + 50 + self.baitY]
                direction = (pygame.Vector2(self.gotoPos) - pygame.Vector2(self.fromPos)).normalize()
                self.baitX += direction[0] * 5
                self.baitY += direction[1] * 5

            else:
                currentScreen.isFishing = False
                currentScreen.usePressed = False
                currentScreen.camera.dirY = 0
                self.throwingBait = False
                if self.caughtFish:
                    if currentScreen.capacityVisual.capacity < currentScreen.capacityVisual.maxCapacity:
                        self.caughtFish = False
                        currentScreen.fishInventoryDict[currentScreen.fishes[self.caughtFishIndex].name] += 1
                        currentScreen.fishHandler.deleteFish(currentScreen.fishes[self.caughtFishIndex])
                        # currentScreen.totalFishAmount -= 1
                        # currentScreen.fishes.pop(self.caughtFishIndex)
                        self.caughtFishIndex = -1
                        currentScreen.capacityVisual.add()
                    else:
                        self.caughtFish = False
                        currentScreen.fishes[self.caughtFishIndex].drop = True
                        self.caughtFishIndex = -1
                        currentScreen.isFishing = False
                        currentScreen.boat.caughtFish = False
                elif self.rollBack:
                    self.rollBack = False

    def checkFishCollisions(self):
            #########
            #Handler of collision between bait and fish hit boxes
            #########

            #Check if you aren't catching already another fish
            if not self.caughtFish:
                self.fishCollideIndex = self.baitRect.collidelist([fish.hitBoxRect for fish in currentScreen.fishes])

            #If a fish is caught - continue
            if self.fishCollideIndex != -1:

                #If caughtFishIndex is null, set to index of fish caught
                if self.caughtFishIndex == -1:
                    self.caughtFishIndex = self.fishCollideIndex

                #If it's already set, and it equals fishCollideIndex, catch the fish 
                elif self.caughtFishIndex == self.fishCollideIndex:                    
                    self.catchFish()

    def catchFish(self):
        ########
        #Handler of catching fish
        ########

        #Set the fish that it has been caught
        currentScreen.fishes[self.fishCollideIndex].caught = True

        #Set fish's position to bait's position
        currentScreen.fishes[self.fishCollideIndex].baitPos = self.baitRect.center

        #Set the boat that it has caught a fish
        self.caughtFish = True

        #Set position towards which the fish and bait will go
        self.gotoPos = self.defaultBaitPos.copy()

        #Seperate position from baitRect.center
        self.fromPos = list(self.baitRect.center)

        #Scare the other fishes once the fish is caught
        self.scareFish()

    def scareFish(self):
        ########
        #Handler for scaring surrounding fishes
        ########

        #Positioning scare rect to the fish's position
        self.scareRadius.center = currentScreen.fishes[self.fishCollideIndex].rect.center

        #Check if fishes collide with the scare rect
        for fishIndex in self.scareRadius.collidelistall([fish.hitBoxRect for fish in currentScreen.fishes]):

            #If they do, call the scare function in fish
            if fishIndex != self.fishCollideIndex:
                currentScreen.fishes[fishIndex].scare(currentScreen.fishes[currentScreen.fishCollideIndex].rect)
        
        #Exclude the fish caught from scaring
        currentScreen.fishes[self.fishCollideIndex].scared = False

class DockingHandler:

    def checkDocking(self):
        ###########
        #Check if player is docked and handle harbor text visibility
        ###########

        if currentScreen.boat.staticRect.centerx == WIDTH//2:
            if not currentScreen.boat.dockedIn:
                currentScreen.boat.dockedIn = True
                currentScreen.usePressed = False
            currentScreen.harborTextVisual.appear()
        else:
            currentScreen.boat.dockedIn = False
            currentScreen.harborTextVisual.disappear()

    def handleDockingTransition(self):
        ###########
        #Handle transition between shops and fishing parts
        ###########

        if currentScreen.usePressed and not currentScreen.isFishing:
            self.checkDirection()

        self.handleTransition()

    def checkDirection(self):
        #############
        #Checking direction of transition
        #############

        if currentScreen.showingShops:
            if currentScreen.transition == 0:
                currentScreen.transition = -1
            else:
                currentScreen.transition = 1
            currentScreen.usePressed = False
        else:
            if currentScreen.transition == 0:
                currentScreen.transition = 1
            else:
                currentScreen.transition = -1
            currentScreen.usePressed = False

    def handleTransition(self):
        ##########
        #Moving the game screen according to the transition
        ##########

        currentScreen.gsPos[0] += 3 * currentScreen.transition
        currentScreen.shopsRect.right += 3 * currentScreen.transition
        if currentScreen.gsPos[0] >= WIDTH:
            currentScreen.gsPos[0] = WIDTH
            currentScreen.shopsRect.right = WIDTH
            currentScreen.transition = 0
            currentScreen.usePressed = False
            currentScreen.showingShops = True
        elif currentScreen.gsPos[0] < 0:
            currentScreen.gsPos[0] = 0
            currentScreen.shopsRect.right = 0
            currentScreen.transition = 0
            currentScreen.usePressed = False
            currentScreen.showingShops = False

class FishHandler:
    def spawnFish(self):
        #############
        #Spawn a random fish
        #############

        currentScreen.fishes.append(Fish(currentScreen.region, currentScreen.fishLevels, currentScreen.water.rect.top, currentScreen.endOfMap, currentScreen.fishNames))
        currentScreen.totalFishAmount += 1

    def deleteFish(self, fish : Fish):
        #############
        #Delete a fish
        #############

        print(fish.name)

        if fish.caught and not currentScreen.discoveredFishes[fish.name]:
            currentScreen.discoveredFishes[fish.name] = True

        currentScreen.fishes.remove(fish)
        currentScreen.totalFishAmount -= 1

    def outOfBound(self):
        ############
        #Handler for checking and removing fishes if they are out of the map
        ############

        if currentScreen.boat.caughtFish:
            return
        for fish in currentScreen.fishes:
            if fish.rect.right < 0 or fish.rect.left > currentScreen.endOfMap:
                self.deleteFish(fish)
                gc.collect()

    def keepEnoughFish(self):
        ###########
        #Handler for keeping enough fish in map
        ###########

        if currentScreen.totalFishAmount >= currentScreen.fishAmount or currentScreen.boat.caughtFish or currentScreen.fishCollideIndex != -1:
            return
        
        self.spawnFish()

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

        self.container = pygame.Surface((self.width - self.gapfromScreen, self.height * 1.4))
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

        self.scrolling = False
        self.oldPos = []

    def click(self, pos):
        print("CLICK")
        cursorRect = pygame.Rect(pos[0], pos[1]-self.iRect.top-self.cRect.top, 1, 1)
        collide = cursorRect.collidelist([item.backgroundRect for item in self.items])
        if collide != -1:
            name = self.items[collide].rawName.removesuffix(".png")
            if currentScreen.fishInventoryDict[name] > 0:
                currentScreen.fishInventoryDict[name] -= 1
                currentScreen.moneyVisual.add(self.fishPrices[name])
                currentScreen.capacityVisual.remove()
    
    def scroll(self, direction):
        if direction == 1:
            self.moveUp = True
            self.moveDown = False
        else:
            self.moveDown = True
            self.moveUp = False
        self.oldPos = self.cRect.topleft
        self.scrolling = True

    def update(self):
        
        self.iRect.center = (-currentScreen.camera.pos[0] + WIDTH//2, -currentScreen.camera.pos[1] + HEIGHT//2)

        if self.moveDown and self.cRect.bottom > self.iRect.height - self.gapfromScreen//2:
            self.cRect.topleft = (self.cRect.left, self.cRect.top-3)
        elif self.moveUp and self.cRect.top < self.gapfromScreen//2:
            self.cRect.topleft = (self.cRect.left, self.cRect.top+3)
        else:
            self.cRect.topleft = (self.cRect.left, self.cRect.top)

        if self.scrolling:
            if abs(self.oldPos[1] - self.cRect.topleft[1]) > 40:
                self.scrolling = False
                self.moveDown = False
                self.moveUp = False

        if len(self.items) == 0:
            for i, fishName in enumerate(self.fishPrices.keys()):
                fishImage = load_image(f'img/{currentScreen.region}/fish/{fishName}.png')
                self.items.append(InventoryItem(self.cRect.w, self.itemHeight, i*self.itemHeight, fishImage, fishName))
        
        self.inventory.fill((100,100,100))

        for i in self.items:
            i.update(self.container)

        self.inventory.blit(self.container, self.cRect)
        # self.inventory.blit(self.money, self.moneyRect)
        currentScreen.gameScreenS.blit(self.inventory, self.iRect)

class InventoryItem:
    def __init__(self, width, height, y, image, name):

        self.image = image

        self.fullName = name
        self.rawName = self.fullName.removesuffix(".png")

        if currentScreen.discoveredFishes[self.rawName]:
            self.name = list(self.rawName.replace("_", " "))
            self.name[0] = self.name[0].upper()
            self.name = "".join(self.name)

            self.icon = image
            
            self.discovered = True
        else:
            self.iconMask = pygame.mask.from_surface(image)
            self.iconMask.invert()
            self.icon = self.iconMask.to_surface()
            self.icon.set_colorkey((255,255,255))

            self.discovered = False

        self.width, self.height = width-10, height-5
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((150,150,150))
        self.backgroundRect = self.background.get_rect()
        self.backgroundRect.topleft = (5, y+5)

        self.iconRect = self.icon.get_rect()
        self.iconRect.center = (height//2, height//2)

        self.font = pygame.font.Font(size=40)

        if self.discovered:
            self.nameText = self.font.render(self.name, False, [0,0,0])
        else:
            self.nameText = self.font.render("???", False, [0,0,0])
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

        if currentScreen.discoveredFishes[self.rawName] and not self.discovered:
            self.name = list(self.rawName.replace("_", " "))
            self.name[0] = self.name[0].upper()
            self.name = "".join(self.name)

            self.nameText = self.font.render(self.name, False, [0,0,0])
            self.nameTextRect = self.nameText.get_rect()
            self.nameTextRect.centerx = self.width//2
            self.nameTextRect.centery = self.height//2

            self.icon = self.image

            self.discovered = True

        self.background.fill((150,150,150))
        self.background.blit(self.icon, self.iconRect)
        self.background.blit(self.nameText, self.nameTextRect)
        if currentScreen.discoveredFishes[self.rawName]:
            self.background.blit(self.amountText, self.amountTextRect)
        surf.blit(self.background, self.backgroundRect)

class Button:
    def __init__(self, image, clickedImage, function: Callable, pos = [WIDTH//2, HEIGHT//2]):
        self.img = load_image(image)
        self.imgC = load_image(clickedImage)
        self.rect = self.img.get_rect()
        self.rect.center = pos
        self.function = function

        self.pressed = False

    def click(self):
        mousePos = list(pygame.mouse.get_pos())
        if isinstance(currentScreen, GameScreen):
            mousePos[0] -= currentScreen.camera.pos[0]
            mousePos[1] -= currentScreen.camera.pos[1]
        if mousePos[0] > self.rect.x and mousePos[0] < self.rect.x + self.rect.width and mousePos[1] > self.rect.y and mousePos[1] < self.rect.y + self.rect.height and self.pressed:
            self.function()
        self.pressed = False

    def press(self):
        mousePos = list(pygame.mouse.get_pos())
        if isinstance(currentScreen, GameScreen):
            mousePos[0] -= currentScreen.camera.pos[0]
            mousePos[1] -= currentScreen.camera.pos[1]
        if mousePos[0] > self.rect.x and mousePos[0] < self.rect.x + self.rect.width and mousePos[1] > self.rect.y and mousePos[1] < self.rect.y + self.rect.height:
            self.pressed = True

    def update(self, update=False):
        if update:
            self.rect.topright = [-currentScreen.camera.pos[0] + WIDTH - 10, -currentScreen.camera.pos[1] + 10]
        self.draw()

    def draw(self):
        if not self.pressed:
            if isinstance(currentScreen, MenuScreen):
                screenS.blit(self.img, self.rect)
            elif isinstance(currentScreen, GameScreen):
                currentScreen.gameScreenS.blit(self.img, self.rect)
        else:
            if isinstance(currentScreen, MenuScreen):
                screenS.blit(self.imgC, self.rect)
            elif isinstance(currentScreen, GameScreen):
                currentScreen.gameScreenS.blit(self.imgC, self.rect)
 
menuScreen = MenuScreen()
gameScreen = GameScreen()
optionsScreen = OptionsScreen()

currentScreen = menuScreen

running = True

while running:
    clock.tick(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if isinstance(currentScreen, GameScreen):
                #Saving inventory
                saveData()

            running = False

        if event.type == pygame.MOUSEWHEEL:
            if isinstance(currentScreen, GameScreen):
                currentScreen.fishInventory.scroll(event.y)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                currentScreen.mouseButtonDown()
        
        if event.type == pygame.MOUSEBUTTONUP:
            currentScreen.mouseButtonUp()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                currentScreen = menuScreen
            currentScreen.keyDown(event.key)

        if event.type == pygame.KEYUP:
            currentScreen.keyUp(event.key)



    if type(currentScreen) in [MenuScreen, OptionsScreen]:
        screenS = pygame.Surface((WIDTH - currentScreen.screenPos[0] + 2, HEIGHT - currentScreen.screenPos[1] + 2))
    else:
        screenS = pygame.Surface((WIDTH - currentScreen.camera.pos[0] + 2, HEIGHT - currentScreen.camera.pos[1] + 2))

    if isinstance(currentScreen, GameScreen):
        color = currentScreen.shops.get_at((0,400))
    else:
        color = (255,255,255)

    screenS.fill(color)

    currentScreen.update()

    if type(currentScreen) in [MenuScreen, OptionsScreen]:
        screen.blit(screenS, currentScreen.screenPos)
    else:
        screen.blit(screenS, currentScreen.camera.pos)

    pygame.display.flip()

pygame.quit()