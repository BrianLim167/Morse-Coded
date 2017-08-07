# 15-112, Summer 2, Morse Coded
################################################################################
# Full name: Brian Lim
# Section: B
# Andrew ID: blim2
################################################################################

def rgbString(red, green, blue): # by Professor Davis
    return "#%02x%02x%02x" % (red, green, blue)

from tkinter import *

# Initialize the data which will be used to draw on the screen.

def init(data):
    # load data as appropriate
    initAlphabet(data)
    initWidgets(data)

def initAlphabet(data):
    path = "reference/alphabet.txt"
    text = open(path,'r', encoding="utf8").read().splitlines()
    data.toMorse = dict()
    data.toText = dict()
    for line in text:
        if (not (line == "" or line[0] == "#")):
            char  = line.split()[0]
            morse = line.split()[1]
            data.toMorse[char] = morse
            data.toMorse[char.lower()] = morse
            data.toText[morse] = char
    data.toMorse[" "] = "/"
    data.toText["/"] = " "

def initWidgets(data):
    data.wText = Text(data.frame, font="Consolas 12", width=40, height=15)
    data.wText.pack()
    data.wText.place(x=20, y=100)
    data.wMorse = Text(data.frame, font="Consolas 12", width=40, height=15)
    data.wMorse.pack()
    data.wMorse.place(x=780, y=100, anchor=NE)

# These are the CONTROLLERs.
# IMPORTANT: CONTROLLER does *not* draw at all!
# It only modifies data according to the events.
def toMorse(data, text):
    ans = ""
    for i in range(len(text)):
        char = text[i]
        if (char in data.toMorse):
            if (i == 0): space = ""
            else: space = " "
            ans += space + data.toMorse[char]
    return ans

def toText(data, morse):
    ans = ""
    morse = morse.split()
    for i in range(len(morse)):
        char = morse[i]
        if (char in data.toText):
            ans += data.toText[char]
    return ans

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if (event.widget == data.wText):
        data.wMorse.delete("1.0",END)
        data.wMorse.insert(END, toMorse(data, data.wText.get("1.0",END)))
    if (event.widget == data.wMorse):
        data.wText.delete("1.0",END)
        data.wText.insert(END, toText(data, data.wMorse.get("1.0",END)))

def timerFired(data):
    pass


# This is the VIEW
# IMPORTANT: VIEW does *not* modify data at all!
# It only draws on the canvas.
def redrawAll(canvas, data):
    # draw in canvas
    pass



####################################
####################################
# use the run function as-is
####################################
####################################

def run(width=800, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    data.root = Tk()
    canvas = Canvas(data.root, width=data.width, height=data.height)
    canvas.pack()
    data.frame = Frame(canvas, bg="red", width=data.width, height=data.height)
    data.frame.pack(expand=True,fill=BOTH)
    init(data)
    # set up events
    data.root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    data.root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    data.root.mainloop()  # blocks until window is closed

run()
