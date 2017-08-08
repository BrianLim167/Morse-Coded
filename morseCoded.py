# 15-112, Summer 2, Morse Coded
################################################################################
# Full name: Brian Lim
# Section: B
# Andrew ID: blim2
################################################################################

# rgbString function is code from Professor Davis's course website
# source: https://pd43.github.io/notes/notes2-2.html
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

from tkinter import *
import random

# Initialize the data which will be used to draw on the screen.
class Data(object):
    def __init__(self, width, height):
        # load self as appropriate
        self.page = self.menu
        self.runInit(width, height)
        self.root.title("Morse Coded")
        self.font = "Consolas 12"
        self.initAlphabet()
        self.menu()
        self.interval = 200
        self.pulse = False
        self.pulseDelay = 10
        self.pulseOnTime = 0
        self.pulseOffTime = 0
        self.pulseCode = ""
        self.pulseEvent()

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
    
    def resetFrame(self):
        self.pulseCode = ""
        for w in self.frame.winfo_children():
            w.destroy()

    def initAlphabet(self):
        path = "reference/morse.txt"
        text = open(path,'r', encoding="utf8").read().splitlines()
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

    def pulseButton(self):
        button = Button(self.frame, bg="red",
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

    def backButton(self, prevPage):
        button = Button(self.frame, bg="red", text="X",
                            width=6, height=3)
        button.pack()
        button.place(x=790, y=10, anchor=NE)
        button.bind("<ButtonPress>", lambda event:
                        prevPage())

    def menu(self):
        self.page = self.menu
        self.resetFrame()
        self.wTranslator = Button(self.frame, bg="red", text="Translator",
                                  width=20,height=4)
        self.wTranslator.pack()
        self.wTranslator.place(x=400, y=300, anchor=CENTER)
        self.wTranslator.bind("<ButtonPress>", lambda event:
                              self.translator())
        self.wEncoder = Button(self.frame, bg="red", text="Encoder",
                               width=20,height=4)
        self.wEncoder.pack()
        self.wEncoder.place(x=400, y=400, anchor=CENTER)
        self.wEncoder.bind("<ButtonPress>", lambda event:
                           self.encoder())
        self.wMorseSearch = Button(self.frame, bg="red", text="Morse Search",
                                   width=20,height=4)
        self.wMorseSearch.pack()
        self.wMorseSearch.place(x=400, y=500, anchor=CENTER)
        self.wMorseSearch.bind("<ButtonPress>", lambda event:
                               self.morseSearch())

    def translator(self):
        self.page = self.translator
        self.resetFrame()
        self.wBack = self.backButton(self.menu)
        self.wText = Text(self.frame, font=self.font, width=40, height=15)
        self.wText.pack()
        self.wText.place(x=20, y=100)
        self.wMorse = Text(self.frame, font=self.font, width=40, height=15)
        self.wMorse.pack()
        self.wMorse.place(x=780, y=100, anchor=NE)
        self.wButton = self.pulseButton()

    def encoder(self):
        self.page = self.encoder
        self.resetFrame()
        self.wBack = self.backButton(self.menu)
        self.wText = Text(self.frame, font=self.font, width=60, height=3)
        self.wText.pack()
        self.wText.place(x=400, y=100, anchor=CENTER)
        self.setEncoderText()
        self.wButton = self.pulseButton()
        
    def morseSearch(self):
        self.page = self.morseSearch
        self.resetFrame()
        self.wBack = self.backButton(self.menu)
        rows = 15
        cols = 15
        self.board = self.blankBoard(rows, cols)
        # dict of tuples of r, c, and direct, which represent the start and end
        # coordinates of each word, mapping to that word
        self.answerKey = dict()
        self.words = ["qwert","qwery","rrrrr"]
        self.loadWords(self.words)
        self.createMorseBoard()
        self.answerOne = None
        self.answerTwo = None
        self.canvas = Canvas(self.frame, width=450, height=100)
        self.canvas.pack()
        self.canvas.place(x=400, y=475, anchor=N) 

    # 2d blank board
    def blankBoard(self, rows, cols):
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
                                font="Arial 11",text=self.board[r][c])
                button.pack()
                button.place(x=r*(buttonSize), y=c*(buttonSize),
                             width=buttonSize, height=buttonSize)
                self.boardGUI[-1].append(button)
        print(self.answerKey)

    # These are the CONTROLLERs.
    # IMPORTANT: CONTROLLER does *not* draw at all!
    # It only modifies data according to the events.
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

    def pulseOn(self):
        self.pulse = True

    def pulseOff(self):
        self.pulse = False

    def pulseEvent(self):
        if (self.pulse):
    ##        if (self.pulseOffTime > self.interval*14):
    ##            self.pulseCode = ""
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
            self.pulseOnTime = 0
            self.pulseOffTime += self.pulseDelay
            if (self.pulseOffTime > self.interval*14):
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
                self.setEncoderText()

    def setEncoderText(self):
        self.morse = random.choice(list(self.mapToText.keys()))
        self.wText.delete("1.0",END)
        self.wText.insert(END, self.toText(self.morse))

    def wordFound(self, rOne, cOne, rTwo, cTwo):
        if (rTwo > rOne): drow = 1
        elif (rTwo < rOne): drow = -1
        else: drow = 0
        if (cTwo > cOne): dcol = 1
        elif (cTwo < cOne): dcol = -1
        else: dcol = 0
        r = rOne
        c = cOne
        while (not (r == rTwo + drow and c == cTwo + dcol)):
            self.boardGUI[r][c].config(bg="green")
            r += drow
            c += dcol
        del self.answerKey[(rOne, cOne, rTwo, cTwo)]
        
    
    def mousePressed(self, event):
        # use event.x and event.y
        if (self.page == self.morseSearch):
            if (event.widget.master == self.wBoard):
                if (self.answerOne == None):
                    self.answerOne = event.widget
                    self.answerOne.config(font=self.font+" bold",
                                          bg=self.answerOne.cget("fg"),
                                          fg=self.answerOne.cget("bg"))
                else:
                    self.answerOne.config(font=self.font,
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
        pass
            
                    
                

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
        pass


    # This is the VIEW
    # IMPORTANT: VIEW does *not* modify data at all!
    # It only draws on the canvas.
    def redrawAll(self):
        # draw in canvas
        canvas = self.canvas
        if (self.page == self.morseSearch):
            text = ""
            for word in self.words():
                if word in self.answerKey.values(): text += "*"
                text += word+"\n"
            canvas.create_text(int(canvas.cget("width"))//2, 0,
                               anchor=N,
                               font=self.font, fill="red",
                               text=text.strip())
            canvas.create_text(int(canvas.cget("width"))//2, 0,
                               anchor=N,
                               font=self.font, fill="red",
                               text=text.strip())

    # these wrapper methods are modified code from Professor Davis's course
    # website
    # source: https://pd43.github.io/notes/code/events-example0.py
    def redrawAllWrapper(self):
        if (hasattr(self, "canvas")):
            self.canvas.delete(ALL)
            self.redrawAll()
            self.canvas.update()    

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
        if (hasattr(self, "canvas")):
            self.canvas.after(self.timerDelay, self.timerFiredWrapper)

def run(width=800, height=600):
        
    # Set up data and call init
    data = Data(width,height)
    # launch the app
    data.root.mainloop()  # blocks until window is closed

run()
