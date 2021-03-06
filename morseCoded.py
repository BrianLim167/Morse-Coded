# 15-112, Summer 2, Morse Coded
################################################################################
# Full name: Brian Lim
# Section: B
# Andrew ID: blim2
################################################################################

from tkinter import *
import random
from tkinter import messagebox
import sys
import hashlib

# Initialize the data which will be used to draw on the screen.
class Data(object):
    def __init__(self, width, height, cheatMode):
        # load self as appropriate
        self.page = self.logIn
        self.canvas = None
        self.infoCanvas = None
        self.runInit(width, height)
        self.root.protocol("WM_DELETE_WINDOW", self.exitProtocol)
        self.root.title("Morse Coded")
        self.font = "Consolas "
        self.initUser()
        self.user = "Guest"
        self.initAlphabet()
        self.initRefWords()
        self.logIn()
        self.cheatVar = IntVar()
        self.interval = 200
        self.showInfo = False
        self.pulse = False
        self.pulseDelay = 10
        self.pulseOnTime = 0
        self.pulseOffTime = 0
        self.pulseCode = ""
        self.pulseEvent()

    # ask the user to quit
    def exitProtocol(self):
        if (messagebox.askyesno("Quit", "Do you want to quit?")):
            self.root.destroy()
            sys.exit(0)

    # runInit method is modified code from Professor Davis's course website
    # source: https://pd43.github.io/notes/code/events-example0.py
    def runInit(self, width, height): 
        self.width = width
        self.height = height
        self.timerDelay = 100 # milliseconds
        self.root = Tk()
        self.frame = Frame(self.root, bg="black",
                           width=self.width, height=self.height)
        self.frame.pack(expand=True,fill=BOTH)
        # set up events
        self.root.bind("<Button-1>", lambda event:
                       self.mousePressedWrapper(event))
        self.root.bind("<ButtonRelease-1>", lambda event:
                       self.mouseReleasedWrapper(event))
        self.root.bind("<Key>", lambda event:
                       self.keyPressedWrapper(event))
        self.timerFiredWrapper()

    # destroy widgets in the frame
    def resetFrame(self):
        self.pulseCode = ""
        for w in self.frame.winfo_children():
            w.destroy()

    def initUser(self):
        path = "user/user.txt"
        self.users = open(path, 'r', encoding="utf8").read().splitlines()
        path = "user/password.txt"
        self.passwords = open(path, 'r', encoding="utf8").read().splitlines()
        path = "user/clicks.txt"
        self.clicks = open(path, 'r', encoding="utf8").read().splitlines()
        path = "user/pressTime.txt"
        self.pressTime = open(path, 'r', encoding="utf8").read().splitlines()

    # create dictionaries that can be used to translate to and from morse code
    def initAlphabet(self):
        path = "reference/morse.txt"
        text = open(path, 'r', encoding="utf8").read().splitlines()
        self.mapToMorse = dict()
        self.mapToText = dict()
        for line in text:
            line = line.strip()
            if (not (line == "" or line[0] == "#")):
                char  = line.split()[0]
                morse = line.split()[1]
                self.mapToMorse[char] = morse
                self.mapToMorse[char.lower()] = morse
                self.mapToText[morse] = char
        self.mapToMorse[" "] = "/"
        self.mapToText["/"] = " "

    def initRefWords(self):
        path = "reference/words.txt"
        text = open(path, 'r', encoding="utf8").read().strip().split()
        self.refWords = text

    # button that sends pulses
    def pulseButton(self):
        button = Button(self.frame, bg="red", overrelief=FLAT,
                              width=20, height=4,
                              command=lambda:
                              self.translatePulse())
        button.pack()
        button.place(x=400, y=500, anchor=CENTER)
        button.bind("<ButtonPress>", lambda event:
                    self.pulseOn())
        button.bind("<ButtonRelease>", lambda event:
                    self.pulseOff())
        return button

    # button that goes to the previous screen
    def backButton(self, prevPage):
        button = Button(self.frame, bg="red", overrelief=FLAT, text="<",
                        font=self.font+"12 bold",
                        width=6, height=3)
        button.pack()
        button.place(x=790, y=10, anchor=NE)
        button.bind("<ButtonPress>", lambda event:
                    prevPage())

    # button that toggles the info screen
    def infoButton(self, infoPage):
        button = Button(self.frame, bg="red", overrelief=FLAT, text="?",
                        font=self.font+"12 bold",
                        width=6, height=3)
        button.pack()
        if (infoPage == self.translator): button.place(x=700, y=10, anchor=NE)
        else: button.place(x=790, y=110, anchor=NE)
        button.bind("<ButtonPress>", lambda event:
                    self.info(infoPage))

    # info displayer
    def info(self, infoPage):
        self.showInfo = not self.showInfo
        if (self.showInfo):
            self.infoCanvas = Canvas(self.frame, bg="blue",
                                     width=400, height=300)
            self.infoCanvas.pack()
            self.infoCanvas.place(x=self.width//2, y=self.height//2,
                                  anchor=CENTER)
        else:
            self.infoCanvas.destroy()
            self.infoCanvas = None

    ############################################################################
    # screen initializers
    ############################################################################

    # menu screen
    def menu(self):
        self.page = self.menu
        self.resetFrame()
        self.showInfo = False
        self.lHello = Label(self.frame,
                            font=self.font+"15", bg="black", fg="white",
                            text="Hello, "+self.user)
        self.lHello.pack()
        self.lHello.place(x=40, y=10)
        self.canvas = Canvas(self.frame, width=550, height=520, bg="black")
        self.canvas.pack()
        self.canvas.place(x=40, y=40)
        self.wTranslator = Button(self.frame, bg="blue", text="Translator",
                                  font=self.font+"12", overrelief=FLAT,
                                  width=18,height=4)
        self.wTranslator.pack()
        self.wTranslator.place(x=780, y=5, anchor=NE)
        self.wTranslator.bind("<ButtonPress>", lambda event:
                              self.translator())
        self.wEncoder = Button(self.frame, bg="blue", text="Encoder",
                               font=self.font+"12", overrelief=FLAT,
                               width=18,height=4)
        self.wEncoder.pack()
        self.wEncoder.place(x=780, y=105, anchor=NE)
        self.wEncoder.bind("<ButtonPress>", lambda event:
                           self.encoder())
        self.wMorseSearch = Button(self.frame, bg="blue", text="Morse Search",
                                   font=self.font+"12", overrelief=FLAT,
                                   width=18,height=4)
        self.wMorseSearch.pack()
        self.wMorseSearch.place(x=780, y=205, anchor=NE)
        self.wMorseSearch.bind("<ButtonPress>", lambda event:
                               self.morseSearch())
        if (self.user != "Guest"):
            self.wUserInfo = Button(self.frame, bg="purple", text="User Info",
                                    font=self.font+"12", overrelief=FLAT,
                                    width=18,height=4)
            self.wUserInfo.pack()
            self.wUserInfo.place(x=780, y=305, anchor=NE)
            self.wUserInfo.bind("<ButtonPress>", lambda event:
                                self.userInfo())
        self.wLogOut = Button(self.frame, bg="purple", text="Log Out",
                              font=self.font+"12", overrelief=FLAT,
                              width=18,height=4)
        self.wLogOut.pack()
        self.wLogOut.place(x=780, y=405, anchor=NE)
        self.wLogOut.bind("<ButtonPress>", lambda event:
                          self.logIn())
        self.wSettings = Button(self.frame, bg="red", text="Settings",
                                font=self.font+"12", overrelief=FLAT,
                                width=18,height=4)
        self.wSettings.pack()
        self.wSettings.place(x=780, y=505, anchor=NE)
        self.wSettings.bind("<ButtonPress>", lambda event:
                               self.settings())

    # translator screen
    def translator(self):
        self.page = self.translator
        self.resetFrame()
        self.showInfo = False
        self.wBack = self.backButton(self.menu)
        self.wInfo = self.infoButton(self.page)
        self.wText = Text(self.frame, font=self.font+"12", width=40, height=15)
        self.wText.pack()
        self.wText.place(x=20, y=100)
        self.wMorse = Text(self.frame, font=self.font+"12", width=40, height=15)
        self.wMorse.pack()
        self.wMorse.place(x=780, y=100, anchor=NE)
        self.wButton = self.pulseButton()

    # encoder screen
    def encoder(self):
        self.page = self.encoder
        self.resetFrame()
        self.showInfo = False
        self.wBack = self.backButton(self.menu)
        self.wInfo = self.infoButton(self.page)
        self.lCheat = Label(self.frame,
                            bg="black", fg="white",
                            font=self.font+"20")
        self.lCheat.pack()
        self.lCheat.place(x=400, y=200, anchor=CENTER)
        self.canvas = Canvas(self.frame, bg="black",
                             width=600, height=100)
        self.canvas.pack()
        self.canvas.place(x=400, y=300, anchor=CENTER)
        self.setMorse()
        self.wButton = self.pulseButton()

    def setMorse(self, dontRepeat=None):
        # select a new character for the encoder
        morseChars = list(self.mapToText.keys())
        morseChars.remove("/")
        if (dontRepeat in morseChars): morseChars.remove(dontRepeat)
        self.morse = random.choice(morseChars)
        self.pulseCode = ""
        if (self.cheatVar.get() == 1): self.lCheat.config(text=self.morse)

    # morse search screen
    def morseSearch(self):
        self.page = self.morseSearch
        self.resetFrame()
        self.showInfo = False
        self.wBack = self.backButton(self.menu)
        self.wInfo = self.infoButton(self.page)
        rows = 15
        cols = 18
        self.board = self.blankBoard(rows, cols)
        self.targetCoords = (0,0,0,0)
        self.lastTargetCoords = (0,0,0,0)
        # dict of tuples of r, c, and direct, which represent the start and end
        # coordinates of each word, mapping to that word
        self.answerKey = dict()
        self.words = self.randomWords(8,40)
        self.loadWords(self.words)
        self.createMorseBoard()
        self.answerOne = None
        self.answerTwo = None
        self.canvas = Canvas(self.frame, width=750, height=100)
        self.canvas.pack()
        self.canvas.place(x=400, y=475, anchor=N)
        self.cRows = 4
        self.cCols = 2

    def blankBoard(self, rows, cols):
        # 2d blank board
        ans = []
        for row in range(rows):
            ans.append([])
            for col in range(cols):
                ans[-1].append("_")
        return ans

    def loadWords(self, words):
        # add each word to the board, if possible
        for word in words:
            attempts = 0
            added = False
            while (attempts < 500 and not added):
                r = random.randint(0,len(self.board)-1)
                c = random.randint(0,len(self.board[0])-1)
                direct = random.randint(0,7)
                if (direct == 0):
                    drow = 1
                    dcol = 0
                elif (direct == 1):
                    drow = 1
                    dcol = 1
                elif (direct == 2):
                    drow = 0
                    dcol = 1
                elif (direct == 3):
                    drow = -1
                    dcol = 1
                elif (direct == 4):
                    drow = -1
                    dcol = 0
                elif (direct == 5):
                    drow = -1
                    dcol = -1
                elif (direct == 6):
                    drow = 0
                    dcol = -1
                elif (direct == 7):
                    drow = 1
                    dcol = -1
                if self.addWord(word, r, c, drow, dcol):
                    added = True
                    rTwo = r + (len(word)-1) * drow
                    cTwo = c + (len(word)-1) * dcol
                    self.answerKey[(r, c, rTwo, cTwo)] = word
                attempts += 1
        # fill the rest of the board with random characters
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if (self.board[r][c] == "_"):
                    self.board[r][c] = chr(ord("A") + random.randint(0,25))

    def addWord(self, word, row, col, drow, dcol):
        for i in range(len(word)):
            if (not 0 <= row + drow*i < len(self.board) or
                not 0 <= col + dcol*i < len(self.board[0]) or
                (self.board[row + drow*i][col + dcol*i] != "_" and
                self.board[row + drow*i][col + dcol*i] != word[i])):
                return False
        for i in range(len(word)):
            self.board[row + drow*i][col + dcol*i] = word[i]
        return True

    def createMorseBoard(self):
        rows = len(self.board)
        cols = len(self.board[0])
        buttonSize = 30
        # frame containing the grid
        self.wBoard = Frame(self.frame,
                            width=cols*buttonSize, height=rows*buttonSize)
        self.wBoard.pack()
        self.wBoard.place(x=400, y=10, anchor=N)
        # grid of buttons for the morse search
        self.boardGUI = []
        for r in range(rows):
            self.boardGUI.append([])
            for c in range(cols):
                button = Button(self.wBoard,
                                bg="white", overrelief=FLAT,
                                font="Arial 11",text=self.board[r][c].upper())
                button.pack()
                button.place(x=c*(buttonSize), y=r*(buttonSize),
                             width=buttonSize, height=buttonSize)
                self.boardGUI[-1].append(button)

    def wordFound(self, rOne, cOne, rTwo, cTwo):
        # highlight found word in color
        if (rTwo > rOne): drow = 1
        elif (rTwo < rOne): drow = -1
        else: drow = 0
        if (cTwo > cOne): dcol = 1
        elif (cTwo < cOne): dcol = -1
        else: dcol = 0
        r = rOne
        c = cOne
        while (not (r == rTwo + drow and c == cTwo + dcol)):
            self.boardGUI[r][c].config(bg="green2")
            r += drow
            c += dcol
        del self.answerKey[(rOne, cOne, rTwo, cTwo)]

    def randomWords(self, numOfWords, lenLimit):
        # list of numOfWords many random words
        ans = []
        while (len(ans) < numOfWords):
            word = random.choice(self.refWords)
            if (len(self.toMorse(word)) <= lenLimit):
                ans.append(word)
        return ans

    def highlight(self, bold):
        # highlight word in bold text
        if (bold):
            font = "Arial 18 bold"
            coords = self.targetCoords
        else:
            font = "Arial 11"
            coords = self.lastTargetCoords
        (rOne, cOne, rTwo, cTwo) = coords
        if (rTwo > rOne): drow = 1
        elif (rTwo < rOne): drow = -1
        else: drow = 0
        if (cTwo > cOne): dcol = 1
        elif (cTwo < cOne): dcol = -1
        else: dcol = 0
        r = rOne
        c = cOne
        while (not (r == rTwo + drow and c == cTwo + dcol)):
            self.boardGUI[r][c].config(font=font)
            r += drow
            c += dcol

    # user info screen
    def userInfo(self):
        self.page = self.userInfo
        self.resetFrame()
        self.showInfo = False
        self.wBack = self.backButton(self.menu)
        clicks = self.clicks[self.users.index(self.user)]
        pressTime = self.pressTime[self.users.index(self.user)]
        self.lClicks = Label(self.frame, text="Number of Clicks: "+clicks,
                             bg="black", fg="white",
                             font=self.font+"20")
        self.lClicks.pack()
        self.lClicks.place(x=400, y=250, anchor=CENTER)
        self.lPressTime = Label(self.frame,
                                text="Time Spent Pressing the Pulse Button: "+\
                                str(int(pressTime)//1000)+" seconds",
                                bg="black", fg="white",
                                font=self.font+"20")
        self.lPressTime.pack()
        self.lPressTime.place(x=400, y=350, anchor=CENTER)

    # login screen
    def logIn(self):
        self.page = self.logIn
        self.resetFrame()
        self.showInfo = False
        self.cheatVar = IntVar()
        self.interval = 200
        self.user = "Guest"
        self.lLogIn = Label(self.frame, text="Log In",
                            bg="black", fg="white",
                            font=self.font+"40")
        self.lLogIn.pack()
        self.lLogIn.place(x=400, y=125, anchor=CENTER)
        self.wUsername = Entry(self.frame, width=30)
        self.wUsername.pack()
        self.wUsername.place(x=300, y=250)
        self.root.focus_set()
        self.wUsername.focus_set()
        self.root.focus_force()
        self.lUsername = Label(self.frame, text="Username",
                               bg="black", fg="white",
                               font=self.font+"12")
        self.lUsername.pack()
        self.lUsername.place(x=200, y=250)
        self.wPassword = Entry(self.frame, width=30, show="*")
        self.wPassword.pack()
        self.wPassword.place(x=300, y=300)
        self.lPassword = Label(self.frame, text="Password",
                               bg="black", fg="white",
                               font=self.font+"12")
        self.lPassword.pack()
        self.lPassword.place(x=200, y=300)
        self.wLogIn = Button(self.frame, bg="red",
                             text="Log In",
                             font=self.font+"12", overrelief=FLAT,
                             width=16, height=4)
        self.wLogIn.pack()
        self.wLogIn.place(x=500, y=285, anchor=W)
        self.wLogIn.bind("<ButtonPress>", lambda event:
                         self.userLogIn(self.wUsername.get(),
                                        self.wPassword.get()))
        self.lMessage = Label(self.frame,
                               bg="black", fg="white",
                               font=self.font+"12")
        self.lMessage.pack()
        self.lMessage.place(x=400, y=375, anchor=CENTER)
        self.wCreateAccount = Button(self.frame, bg="red",
                                     text="Create Account",
                                     font=self.font+"12", overrelief=FLAT,
                                     width=35, height=4)
        self.wCreateAccount.pack()
        self.wCreateAccount.place(x=20, y=580, anchor=SW)
        self.wCreateAccount.bind("<ButtonPress>", lambda event:
                                 self.createAccount())
        self.wGuest = Button(self.frame, bg="red", text="Continue as Guest",
                             font=self.font+"12", overrelief=FLAT,
                             width=45, height=4)
        self.wGuest.pack()
        self.wGuest.place(x=780, y=580, anchor=SE)
        self.wGuest.bind("<ButtonPress>", lambda event:
                            self.menu())

    def userLogIn(self, user, password):
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if (user in self.users and
            password == self.passwords[self.users.index(user)]):
                self.user = user
                self.menu()
        else:
            self.lMessage.config(text="Incorrect username/password.")

    # create account screen
    def createAccount(self):
        self.page = self.createAccount
        self.resetFrame()
        self.showInfo = False
        self.lCreateAccount = Label(self.frame, text="Create Account",
                                    bg="black", fg="white",
                                    font=self.font+"40")
        self.lCreateAccount.pack()
        self.lCreateAccount.place(x=400, y=125, anchor=CENTER)
        self.wUsername = Entry(self.frame, width=30)
        self.wUsername.pack()
        self.wUsername.place(x=300, y=250)
        self.root.focus_set()
        self.wUsername.focus_set()
        self.root.focus_force()
        self.lUsername = Label(self.frame, text="Username",
                               bg="black", fg="white",
                               font=self.font+"12")
        self.lUsername.pack()
        self.lUsername.place(x=200, y=250)
        self.wPassword = Entry(self.frame, width=30, show="*")
        self.wPassword.pack()
        self.wPassword.place(x=300, y=300)
        self.lPassword = Label(self.frame, text="Password",
                               bg="black", fg="white",
                               font=self.font+"12")
        self.lPassword.pack()
        self.lPassword.place(x=200, y=300)
        self.wCreateAccount = Button(self.frame, bg="red",
                                     text="Create Account",
                                     font=self.font+"12", overrelief=FLAT,
                                     width=16, height=4)
        self.wCreateAccount.pack()
        self.wCreateAccount.place(x=500, y=285, anchor=W)
        self.wCreateAccount.bind("<ButtonPress>", lambda event:
                         self.userCreateAccount(self.wUsername.get(),
                                                self.wPassword.get()))
        self.lMessage = Label(self.frame,
                               bg="black", fg="white",
                               font=self.font+"12")
        self.lMessage.pack()
        self.lMessage.place(x=400, y=375, anchor=CENTER)
        self.wLogIn = Button(self.frame, bg="red",
                             text="Log In",
                             font=self.font+"12", overrelief=FLAT,
                             width=35, height=4)
        self.wLogIn.pack()
        self.wLogIn.place(x=20, y=580, anchor=SW)
        self.wLogIn.bind("<ButtonPress>", lambda event:
                         self.logIn())
        self.wGuest = Button(self.frame, bg="red", text="Continue as Guest",
                             font=self.font+"12", overrelief=FLAT,
                             width=45, height=4)
        self.wGuest.pack()
        self.wGuest.place(x=780, y=580, anchor=SE)
        self.wGuest.bind("<ButtonPress>", lambda event:
                            self.menu())

    def userCreateAccount(self, user, password):
        if (user in self.users):
            self.lMessage.config(text="Username already exists.")
        else:
            password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            self.users.append(user)
            self.passwords.append(password)
            path = "user/user.txt"
            open(path, 'a', encoding="utf8").write(user+"\n")
            path = "user/password.txt"
            open(path, 'a', encoding="utf8").write(password+"\n")
            path = "user/clicks.txt"
            open(path, 'a', encoding="utf8").write("0\n")
            path = "user/pressTime.txt"
            open(path, 'a', encoding="utf8").write("0\n")
            self.initUser()

    # settings screen
    def settings(self):
        self.page = self.settings
        self.resetFrame()
        self.showInfo = False
        self.wBack = self.backButton(self.menu)
        self.wInfo = self.infoButton(self.page)
        self.wCheat = Checkbutton(self.frame, text="Cheats",
                                  bg="black", fg="white", selectcolor="black",
                                  font=self.font+"12",
                                  variable=self.cheatVar)
        self.wCheat.pack()
        self.wCheat.place(x=400, y=200, anchor=CENTER)
        self.wTime = Scale(self.frame, from_=30, to=300, length = 270,
                           bg="black", fg="white", font=self.font+"12",
                           orient=HORIZONTAL, label="Interval")
        self.wTime.pack()
        self.wTime.place(x=400, y=300, anchor=CENTER)
        self.wTime.set(self.interval)

    ############################################################################
    # translation methods
    ############################################################################
    
    def toMorse(self, text):
        ans = ""
        for i in range(len(text)):
            char = text[i]
            if (char in self.mapToMorse):
                if (i == 0): space = ""
                else: space = " "
                ans += space + self.mapToMorse[char]
        return ans

    def toText(self, morse):
        ans = ""
        morse = morse.split()
        for i in range(len(morse)):
            char = morse[i]
            if (char in self.mapToText):
                ans += self.mapToText[char]
        return ans
    
    ############################################################################
    # pulse event handling
    ############################################################################

    def pulseOn(self):
        self.pulse = True

    def pulseOff(self):
        self.pulse = False

    def pulseEvent(self):
        if (self.pulse):
            if (self.pulseOffTime > self.interval*7 and self.pulseCode != ""):
                self.pulseCode += " / "
            elif (self.pulseOffTime > self.interval*2 and self.pulseCode != ""):
                self.pulseCode += " "
            if (self.pulseOffTime > 0): self.translatePulse()
            self.pulseOffTime = 0
            self.pulseOnTime += self.pulseDelay
        else:
            if (self.interval*3 < self.pulseOnTime):
                self.pulseCode += "-"
            elif (0 < self.pulseOnTime):
                self.pulseCode += "."
            if (self.pulseOnTime > 0): self.translatePulse()
            if (self.user != "Guest"):
                pressTime = self.pressTime[self.users.index(self.user)]
                self.pressTime[self.users.index(self.user)] = str(
                    int(pressTime) + self.pulseOnTime)
                newPressTimeTxt = ""
                for line in self.pressTime:
                    newPressTimeTxt += line + "\n"
                path = "user/pressTime.txt"
                open(path, 'w', encoding="utf8").write(newPressTimeTxt)
            self.pulseOnTime = 0
            self.pulseOffTime += self.pulseDelay
            if (self.pulseOffTime > self.interval*10):
                self.pulseCode = ""
        self.root.after(self.pulseDelay, self.pulseEvent)

    def translatePulse(self):
        if (self.page == self.translator):
            self.wMorse.delete("1.0",END)
            self.wMorse.insert(END, self.pulseCode)
            self.wText.delete("1.0",END)
            self.wText.insert(END, self.toText(self.pulseCode))
        elif (self.page == self.encoder):
            if (self.pulseCode.strip() == self.morse):
                self.setMorse(self.morse)

    ############################################################################
    # other events
    ############################################################################

    def mousePressed(self, event):
        # use event.x and event.y
        if (self.page == self.morseSearch):
            if (event.widget.master == self.wBoard):
                if (self.answerOne == None):
                    self.answerOne = event.widget
                    self.answerOne.config(font=self.font+"12 bold",
                                          bg=self.answerOne.cget("fg"),
                                          fg=self.answerOne.cget("bg"))
                else:
                    self.answerOne.config(font=self.font+"12",
                                          bg=self.answerOne.cget("fg"),
                                          fg=self.answerOne.cget("bg"))
                    self.answerTwo = event.widget
                    rOne, cOne = -1,-1
                    rTwo, cTwo = -1,-1
                    for r in range(len(self.boardGUI)):
                        for c in range(len(self.boardGUI[r])):
                            if (self.boardGUI[r][c] == self.answerOne):
                                rOne,cOne = r,c
                            if (self.boardGUI[r][c] == self.answerTwo):
                                rTwo,cTwo = r,c
                    if ( (rOne, cOne, rTwo, cTwo) in self.answerKey.keys()):
                        self.wordFound(rOne, cOne, rTwo, cTwo)
                    self.answerOne = None
                    self.answerTwo = None

    def mouseReleased(self, event):
        if (self.user != "Guest"):
            user = self.user
            clicks = self.clicks[self.users.index(user)]
            self.clicks[self.users.index(user)] = str(int(clicks) + 1)
            newClicksTxt = ""
            for line in self.clicks:
                newClicksTxt += line + "\n"
            path = "user/clicks.txt"
            open(path, 'w', encoding="utf8").write(newClicksTxt)
        if (self.page == self.userInfo):
            self.lClicks.config(text="Number of Clicks: "+clicks)
        if (self.page == self.settings):
            if (event.widget == self.wCheat):
                self.cheat = (self.cheatVar == 1)
            if (event.widget == self.wTime):
                self.interval = self.wTime.get()

    def keyPressed(self, event):
        # use event.char and event.keysym
        if (self.page == self.translator):
            if (event.widget == self.wText):
                self.pulseCode = ""
                self.wMorse.delete("1.0",END)
                self.wMorse.insert(END, self.toMorse(self.wText.get("1.0",END)))
            if (event.widget == self.wMorse):
                self.pulseCode = ""
                self.wText.delete("1.0",END)
                self.wText.insert(END, self.toText(self.wMorse.get("1.0",END)))

    def timerFired(self):
        if (self.page == self.morseSearch):
            if (self.cheatVar.get() == 1):
                width = int(self.canvas.cget("width"))
                height = int(self.canvas.cget("height"))
                x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
                y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
                rows = self.cRows
                cols = self.cCols
                i = 0
                self.lastTargetCoords = self.targetCoords
                self.highlight(False)
                found = False
                for row in range(rows):
                    for col in range(cols):
                        if (width*col//cols <= x < width*(col+1)//cols and
                            height*row//rows <= y < height*(row+1)//rows):
                            target = self.words[i]
                            for coords in self.answerKey:
                                if (self.answerKey[coords] == target):
                                    self.targetCoords = coords
                                    found = True
                                    break
                            if (found): self.highlight(True)
                            return
                        i +=1

    ############################################################################
    # canvas drawing
    ############################################################################
    
    def redrawAll(self):
        # draw in canvas
        canvas = self.canvas
        width = int(canvas.cget("width"))
        height = int(canvas.cget("height"))
        if (self.page == self.menu):
            fg = "white"
            canvas.create_text(10, 100,
                               font=self.font+"90 bold", fill=fg,
                               anchor=NW, text="Morse\n   Coded")
            canvas.create_text(width//2, 480,
                               font=self.font+"15 italic", fill=fg,
                               anchor=CENTER, text="developed by Brian Lim")
        if (self.page == self.encoder):
            fg = "white"
            canvas.create_text(width//2, height//2,
                               font=self.font+"50 bold", fill=fg,
                               anchor=CENTER, text=self.toText(self.morse))
        if (self.page == self.morseSearch):
            rows = self.cRows
            cols = self.cCols
            i = 0
            for row in range(rows):
                for col in range(cols):
                    if ((row + col) % 2 == 0): bg = "white"
                    else: bg="black"
                    if (i < len(self.words)):
                        word = self.words[i]
                        morse = self.toMorse(word)
                        if (word in self.answerKey.values()): fg = "red"
                        else:
                            bg = "green2"
                            fg = "white"
                    else: word = ""
                    canvas.create_rectangle(width*col//cols,
                                            height*row//rows,
                                            width*(col+1)//cols,
                                            height*(row+1)//rows,
                                            fill=bg, outline=bg)
                    if (word != ""):
                        canvas.create_text(width*col//cols + 10,
                                           height*row//rows,
                                           font=self.font+"12 bold", fill=fg,
                                           anchor=NW, text=morse)
                    i += 1

    def redrawInfo(self):
        canvas = self.infoCanvas
        width = int(canvas.cget("width"))
        height = int(canvas.cget("height"))
        text = ""
        if (self.page == self.translator):
            text = '''\
The left text box represents text in normal
characters; the right text box, in morse
code dots and dashes. Type in one box in
order to get the appropriate translation in
the other. Pressing the button near the
bottom of the window will create a pulse
that the text boxes will also be able to
translate.
'''
        if (self.page == self.encoder):
            text = '''\
Some text will be displayed in the center of
the screen; press the button near the bottom
of the window in order to create a pulse
that matches the displayed text.
'''
        if (self.page == self.morseSearch):
            text = '''\
Solve the word search by figuring out the
words in the morse code word bank. Click on
the word search to indicate where the words
appear.
'''
        if (self.page == self.settings):
            text = '''\
Enabling cheats will show the correct morse
code marks in Encoder, and will highlight a
word in Morse Search if the cursor is
hovering over a word in the word bank.
Setting the interval determines the timing
for pulses.
'''
        canvas.create_text(5, 0, font=self.font+"12", fill="yellow",
                           anchor=NW, text=text)

    ############################################################################
    # event wrapper functions
    ############################################################################
    # these wrapper methods are modified code from Professor Davis's course
    # website
    # source: https://pd43.github.io/notes/code/events-example0.py
    
    def redrawAllWrapper(self):
        if (self.canvas in self.frame.winfo_children()):
            self.canvas.delete(ALL)
            self.redrawAll()
            self.canvas.update()
        if (self.infoCanvas in self.frame.winfo_children()):
            self.infoCanvas.delete(ALL)
            self.redrawInfo()
            self.infoCanvas.update()

    def mousePressedWrapper(self, event):
        self.mousePressed(event)
        self.redrawAllWrapper()

    def mouseReleasedWrapper(self, event):
        self.mouseReleased(event)
        self.redrawAllWrapper()

    def keyPressedWrapper(self, event):
        self.keyPressed(event)
        self.redrawAllWrapper()

    def timerFiredWrapper(self):
        self.timerFired()
        self.redrawAllWrapper()
        # pause, then call timerFired again
        self.root.after(self.timerDelay, self.timerFiredWrapper)

def run(cheatMode=False):
    width = 800
    height = 600
    # Set up data and call init
    data = Data(width,height,cheatMode)
    # launch the app
    w = data.width
    h = data.height
    data.root.geometry("%dx%d%+d%+d" % (w, h,
                                        data.root.winfo_screenwidth()//2 - w//2,
                                        data.root.winfo_screenheight()//2 - h//2))
    data.root.mainloop()  # blocks until window is closed

if (__name__ == "__main__"):
    cheatMode = True
    run(cheatMode)
