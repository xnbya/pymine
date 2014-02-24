import random, curses, time
noofmines = int(input("Number of mines [20]: "))
gridsize = int(input("Grid size [10]: "))
stdscr = curses.initscr()
curses.noecho()
curses.curs_set(False)
curses.start_color()
curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)
stdscr.keypad(True)
#lstoflsts = [[0]*14]*14
lstoflsts=[]
#noofmines = 20
realmines = noofmines
#gridsize = 15
#print (chr(27) + "[2J")

#fill the grid with 0s
while(len(lstoflsts) < gridsize):
    part = []
    while(len(part) < gridsize):
        part.append(0)
    lstoflsts.append(part)

'''
#print the grid
def pprint(lstA):
    for lstB in lstA:
        #print(lstB)
        for item in lstB:            
            print(item,end=' ')
        print(' ')'''

def conprint(lstA):
    stdscr.addstr(2,4,"Python Minesweeper")
    acc = 0
    while(acc < len(lstA)):
        down = 0
        while(down < len(lstA[acc])):
            toprint = ""
            if(lstA[acc][down] != 0):
                toprint = str(lstA[acc][down])
                #print("\033[" + str((acc+1)*2) + ";" + str((down+1)*4) + "H" + toprint)
                if(toprint == 'X'):
                    stdscr.addstr((down+2)*2,(acc+1)*4,"  ",curses.color_pair(4))
                elif(toprint == '*'):
                    stdscr.addstr((down+2)*2,(acc+1)*4,toprint,curses.color_pair(3))
                elif(toprint == "F"):
                    stdscr.addstr((down+2)*2,(acc+1)*4,"  ",curses.color_pair(5))
                elif(lstA[acc][down] > 1):
                    stdscr.addstr((down+2)*2,(acc+1)*4,toprint,curses.color_pair(1))
                else:
                    stdscr.addstr((down+2)*2,(acc+1)*4,toprint,curses.color_pair(2))
            down += 1
        acc += 1        

#lstoflsts[2][3] = 'yay'

#pprint(lstoflsts)

#add mines  
while(noofmines > 0):
    intA= random.randint(0,gridsize-1)
    intB=random.randint(0,gridsize-1)
    #print(lstoflsts[intA][intB])
    if(lstoflsts[intA][intB] == 0):
        lstoflsts[intA][intB] = '*'
    noofmines -= 1

def addnum(down,along):
    global lstoflists
    if(-1 < down < gridsize and -1 < along < gridsize):    
        if(lstoflsts[down][along] != '*'):
            lstoflsts[down][along] += 1
        #print('down',down,'along',along)


#calculate numbers
down = 0
while(down < gridsize):
    along = 0
    while(along < gridsize):
        if(lstoflsts[down][along] == '*'):
            #print('mine at',along,',',down)
            #pprint(lstoflsts)            
            addnum(down,along-1)
            addnum(down-1,along-1)
            addnum(down-1,along)
            addnum(down-1,along+1)
            addnum(down,along+1)
            addnum(down+1,along+1)
            addnum(down+1,along)
            addnum(down+1,along-1)            
        along += 1
    down += 1
            


#print('starting game')
#game logic
#
#
sqopen = 0
ended = False
lost = False
lstplayer = []
#fill the grid with 0s
while(len(lstplayer) < gridsize):
    part = []
    while(len(part) < gridsize):
        part.append('X')
    lstplayer.append(part)

#print("\033[2J")
#conprint(lstplayer)

def printo(up,across):
    #print (chr(27) + "[2J")    
    stdscr.erase()
    stdscr.border()
    conprint(lstplayer)
    stdscr.addstr(up*2+2,across*4-1,'-')
    stdscr.addstr(up*2+2,across*4+2,'-')
    #print("\033[" + str(up*2) + ";" + str(across*4-1) + "H-")
    #print("\033[" + str(up*2) + ";" + str(across*4+1) + "H-")
    
def openboard(up,across):
    global sqopen
    if(across >= 0 and up >= 0 and across < gridsize and up < gridsize):
        if(lstoflsts[across][up] != '*' and lstplayer[across][up] == 'X'):
            #print(up,across)
            #ime.sleep(0.1)
            lstplayer[across][up] = lstoflsts[across][up]
            sqopen += 1
            if(lstoflsts[across][up] == 0):
                openboard(up-1,across-1)
                openboard(up-1,across)
                openboard(up-1,across+1)
                openboard(up,across+1)
                openboard(up+1,across+1)
                openboard(up+1,across)
                openboard(up+1,across-1)
                openboard(up,across-1)

        

def checksquare(up,across):
    global ended, lost, sqopen
    openboard(up-1,across-1)    
    if(lstoflsts[across-1][up-1] == '*'):
        ended = True
        lost = True    
        lstplayer[across-1][up-1] = lstoflsts[across-1][up-1]
    if(sqopen == gridsize**2 - realmines):
        ended = True
    

	

#curses.setsyx(4,6)
up = 1
across = 1
printo(up,across)
while(not ended):
    #time.sleep(0.1)
    #conprint(lstoflsts)
    #print(lstoflsts)    
    char = stdscr.getch()
    if((char == curses.KEY_UP or char==107) and up > 1):
        up -=1          
    elif((char==curses.KEY_DOWN or char==106) and up < gridsize):
        up += 1        
    elif((char==curses.KEY_LEFT or char==104) and across > 1):
        across -= 1
    elif((char==curses.KEY_RIGHT or char==108) and across < gridsize):
        across += 1
    elif(char==32):
        checksquare(up,across)     
    elif(char == 102):
        if(lstplayer[across-1][up-1] == "X"):
            lstplayer[across-1][up-1] = "F"
        elif(lstplayer[across-1][up-1] == "F"):
            lstplayer[across-1][up-1] = "X"
    printo(up,across)
   # stdscr.addstr(gridsize*2+5,2,str(char))

    
if(lost):
    #print("You have lost!")
    stdscr.addstr(gridsize*2+4,4,"You have lost!")
    stdscr.refresh()
    time.sleep(2)
else:
    #print("You have won!")
    stdscr.addstr(gridsize*2+4,4,"Congradulations, you have won!")
    stdscr.refresh()
    time.sleep(2)


curses.nocbreak()
stdscr.keypad(False)
curses.curs_set(True)
curses.echo()
curses.endwin()    


#print("\033[6;3HX")
#print("\033[12;4HO")
