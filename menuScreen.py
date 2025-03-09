class MenuScreen(Screen):
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
