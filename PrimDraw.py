import turtle
import os
import tkinter as tk
customSet = (False, (0, 0, 0))
undidActions = []
actions = []


def draw(x,y, noActionAppend = False):
    weight = pen.pensize()
    color = pen.color()
    if not noActionAppend:
        actions.append(((x, y), weight, color[0], True))
    print('DRAWTO ' + str(x) + ', ' + str(y) + '. COLOR: ' + color[0] + '. WEIGHT: ' + str(weight))
    pen.goto(x,y)


def teleport(x,y, noActionAppend = False):
    weight = pen.pensize()
    color = pen.color()
    if not noActionAppend:
        actions.append(((x, y), weight, color[0], False))
    pen.penup()
    pen.goto(x,y)
    pen.pendown()

def changeToCustom():
    global customSet
    if os.path.isfile('customRGB.in') and not customSet[0]:
        f = open('customRGB.in', 'r')
        ln = 1
        r = 0
        g = 0
        b = 0
        for line in f:
            global r, g, b, ln
            if ln == 1:
                r = int(line.strip())
            elif ln == 2:
                g = int(line.strip())
            elif ln == 3:
                b = int(line.strip())
            elif ln == 4:
                break
            ln += 1
        pen.color((r, g, b))
        customSet = (True, (r, g, b))
    elif customSet[0]:
        pen.color((customSet[1][0], customSet[1][1], customSet[1][2]))
    else:
        print('No configuration file found')


def changeToRed():
    pen.color('red')

def changeToOrange():
    pen.color('orange')

def changeToYellow():
    pen.color('yellow')

def changeToGreen():
    pen.color('green')

def changeToBlue():
    pen.color('blue')

def changeToPurple():
    pen.color('purple')

def changeToBlack():
    pen.color('black')

def changeToBrown():
    pen.color('brown')
    

def penSizeUp():
    global sizePen
    sizePen.set(sizePen.get() + 1)
    pen.pensize(sizePen.get())


def penSizeDown():
    global sizePen
    sizePen.set(sizePen.get() -1)
    pen.pensize(sizePen.get())

#tk widget funcs
def updatePen():
    global sizePen
    pen.pensize(sizePen.get())

def updateColor(choice):
    if choice == 'Red':
        changeToRed()
    elif choice == 'Orange':
        changeToOrange()
    elif choice == 'Yellow':
        changeToYellow()
    elif choice == 'Green':
        changeToGreen()
    elif choice == 'Blue':
        changeToBlue()
    elif choice == 'Purple':
        changeToPurple()
    elif choice == 'Black':
        changeToBlack()
    elif choice == 'Brown':
        changeToBrown()
    elif choice == 'Custom':
        changeToCustom()

def updateCnvsColor():
    global clrEntryVar
    wn.bgcolor(clrEntryVar.get())

def undo():
    lastIndex = len(actions) - 1
    undidActions.append(actions[lastIndex])
    actions.remove(actions[lastIndex])
    print('=====UNDO=====')
    print(undidActions)
    print(actions)
    print('==============')
    print('\n')
    pen.undo()

def redo():
    action = undidActions[len(undidActions) - 1]
    if action[3]:
        pen.color(action[2])
        pen.pensize(action[1])
        draw(action[0][0], action[0][1], True)
    elif not action[3]:
        pen.color(action[2])
        pen.pensize(action[1])
        teleport(action[0][0], action[0][1], True)
    undidActions.remove(action)
    actions.append(action)
    print('=====REDO=====')
    print(undidActions)
    print(actions)
    print('==============')
    print('\n')



# set up tk window
root = tk.Tk()
root.title('')
root.geometry('175x500')
frame = tk.Frame()
frame.grid()
sizePen = tk.IntVar()
sizePen.set(2)

# turtle window & pen
wn = turtle.Screen()
wn.title('PrimDraw')
pen = turtle.Turtle()
pen.pensize(sizePen.get())
pen.speed(10)
wn.colormode(255)



###setup control buttons###
colourOptions = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple', 'Black', 'Brown', 'Custom']

#pensize control
pensizeLabel = tk.Label(text = 'Stroke Weight', font = ('Arial', 10, 'bold')).grid(row = 0, column = 0)
enterPenSize = tk.Entry(textvariable = sizePen, width = 7).grid(row = 1, column = 0)
updatePenSize = tk.Button(text = 'Set', command = updatePen, relief = 'groove', width = 7).grid(row = 1, column = 1)

#color control
colorMenuLabel = tk.Label(text = 'Colors', font = ('Arial', 10, 'bold')).grid(row = 2, column = 0)
defaultOption = tk.StringVar()
defaultOption.set(colourOptions[6])
colorMenu = tk.OptionMenu(root, defaultOption, *colourOptions, command = updateColor).grid(row = 3, column = 0)

#undo&redo
undoRedoLabel = tk.Label(text = 'Undo/Redo', font = ('Arial', 10, 'bold')).grid(row = 4, column = 0)
undoButton = tk.Button(text = 'Undo', command = undo, width = 7, relief = 'groove').grid(row = 5, column = 0)
redoButton = tk.Button(text = 'Redo', command = redo, width = 7, relief = 'groove').grid(row = 5, column = 1)

#canvas colour set
canvasColorLabel = tk.Label(text = 'Canvas Colour', font = ('Arial', 10, 'bold')).grid(row = 6, column = 0)
clrEntryVar = tk.StringVar()
clrEntryVar.set('white')
colourEntry = tk.Entry(textvariable = clrEntryVar, width = 7).grid(row = 7, column = 0)
updateCnvsColorB = tk.Button(text = 'Set', command = updateCnvsColor, width = 7, relief = 'groove').grid(row = 7, column = 1)


# listeners to teleport
wn.onclick(draw,1)    # left click
wn.onclick(teleport,3) # right click

# listeners to change colour by keyboard
wn.onkey(changeToRed, 1)
wn.onkey(changeToOrange, 2)
wn.onkey(changeToYellow, 3)
wn.onkey(changeToGreen, 4)
wn.onkey(changeToBlue, 5)
wn.onkey(changeToPurple, 6)
wn.onkey(changeToBrown, 7)
wn.onkey(changeToBlack, 8)
wn.onkey(changeToCustom, 0)
wn.onkey(penSizeUp, 'Up')
wn.onkey(penSizeDown, 'Down')

# turn on the listeners and run
wn.listen()
wn.mainloop()