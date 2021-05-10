# -*- coding: utf-8 -*-
"""
Alissa Horton, SP'21 DAT-129-NC71 Python II

Personality icon manipulation

"""
#initate lists for icon rows
iconRow0 = []
iconRow1 = []
iconRow2 = []
iconRow3 = []
iconRow4 = []
iconRow5 = []
iconRow6 = []
iconRow7 = []
iconRow8 = []
iconRow9 = []

#Get 10 integers from user, error check and validate values are either 1 or 0
def getTen(list, start):
    # clear list of default values
    list.clear()
    i = start
    while i < start+10:
        prompt = "{}. Enter a 1 or 0 and press ENTER: ".format(i)
        try:
            n = int(input(prompt))
            if n == 0 or n == 1:
                list.append(n)
                i += 1
            else:
                raise ValueError
        except ValueError:
            print('\n*** Please enter a 1 or 0. ***')
    # display values entered
    print('\nYou entered: ', list)
    # ask user if they want to re-enter the values
    if reEnterTen() == True:
        getTen(list,start)

# ask user if they want to re-enter the last 10 values entered, error check and validate
def reEnterTen():
    ask = input('Do you want to re-enter the last 10 digits? (y/n): ').lower().strip()
    if ask[0] =='y':
        return True
    elif ask[0] =='n':
        return False
    else:
        print('\n*** Invalid input ***')
        return reEnterTen()

# prompt user to enter the scale for the icon display, error check and validate      
def scale():
    prompt = 'Enter the scale (as a whole number) to display your icon: '
    try:
        n = int(input(prompt))
        if n > 0:
            return n
        else:
            raise ValueError
    except ValueError:
        print('\n*** Scale must be a whole number greater than zero. ***')
        return scale()

# ask user if they want to invert the icon display, error check and validate          
def invert():
    ask = input('Do you want to invert the display of your icon? (y/n): ').lower().strip()
    if ask[0] =='y':
        return True
    elif ask[0] =='n':
        return False
    else:
        print('\n*** Invalid input ***')
        return invert()

# ask user if they want to re-enter the last 10 values entered, error check and validate     
def custom():
    ask = input('Do you want to create your own icon? (y/n): ').lower().strip()
    if ask[0] =='y':
        return True
    elif ask[0] =='n':
        return False
    else:
        print('\n*** Invalid input ***')
        return custom()

# ask user if they want to manipulate the icon again, error check and validate    
def manipulateAgain():
    ask = input('Do you want to manipulate this icon again? (y/n): ').lower().strip()
    if ask[0] =='y':
        return True
    elif ask[0] =='n':
        return False
    else:
        print('\n*** Invalid input ***')
        return manipulateAgain()

# ask user if they want to start over, error check and validate    
def startOver():
    ask = input('Do you want to start over? (y/n): ').lower().strip()
    if ask[0] =='y':
        return True
    elif ask[0] =='n':
        return False
    else:
        print('\n*** Invalid input ***')
        return startOver()
    
# initiate getTen each list of 10 values and assign start values
def getData():
    getTen (iconRow0, 1)
    getTen (iconRow1, 11)
    getTen (iconRow2, 21)
    getTen (iconRow3, 31)
    getTen (iconRow4, 41)
    getTen (iconRow5, 51)
    getTen (iconRow6, 61)
    getTen (iconRow7, 71)
    getTen (iconRow8, 81)
    getTen (iconRow9, 91)

# render the icon with the specified scale and invert if applicable
def display(scale):
    char0 = " "
    char1 = "#"
    if invert() == True:
        char0 = "#"
        char1 = " "
    for row in icon:
        i = 0
        while i != scale:
            for element in row:
                if element == 0:
                    element = char0 * scale
                else:
                    element = char1 * scale
                print(element, end=' ')
            print()
            i += 1

# Introduce program
print('\n==========     ICON RENDERING TOOL     ==========\n')
print(''' With this program you can render and manipulate
 a default icon or a custom icon of your own design.
      
 If you choose to render and manipulate a custom icon
 you'll be asked to enter 100 digits as 1s and 0s.
 1s represent character ON and 0s represent character OFF\n''')
print('=================================================')

# begin program
play = True

while play != False:
    
    if custom() == False:
        #set default values
        iconRow0 = [0,0, 0,0, 0,0, 0,0, 0,0]
        iconRow1 = [0,0, 0,0, 0,0, 0,0, 0,0]
        iconRow2 = [0,0, 1,1, 0,0, 1,1, 0,0]
        iconRow3 = [0,1, 1,1, 1,1, 1,1, 1,0]
        iconRow4 = [0,1, 1,1, 1,1, 1,1, 1,0]
        iconRow5 = [0,0, 1,1, 1,1, 1,1, 0,0]
        iconRow6 = [0,0, 0,1, 1,1, 1,0, 0,0]
        iconRow7 = [0,0, 0,0, 1,1, 0,0, 0,0]
        iconRow8 = [0,0, 0,0, 0,0, 0,0, 0,0]
        iconRow9 = [0,0, 0,0, 0,0, 0,0, 0,0]
    else:
        #initiate getData() for custom icon
        getData()
    
    #define icon
    icon = [iconRow0, iconRow1, iconRow2, iconRow3, iconRow4,
            iconRow5, iconRow6,iconRow7, iconRow8, iconRow9]
    
    #run scale/manipulation
    again = True
    
    while again != False:
        size = scale()
        display(size)
        again = manipulateAgain() 
    
    play = startOver()
    
print('\nGoodbye')
