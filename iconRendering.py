# -*- coding: utf-8 -*-
"""
Alissa Horton, SP'21 DAT-129-NC71 Python II

Personality icon manipulation

"""
def icon_getTen(list, start):
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
            print('Please enter a 1 or 0.')

    print('\nYou entered: ', list)
    
    if reEnterTen() == True:
        icon_getTen(list,start)
   
def reEnterTen():
    ask = input('Do you want to re-enter the last 10 digits? (y/n):').lower().strip()
    if ask[0] =='y':
        return True
    elif ask[0] =='n':
        return False
    else:
        print('Invalid input')
        return reEnterTen()

def icon_getData():
    icon_getTen (iconRow0, 1)
    icon_getTen (iconRow1, 11)
    icon_getTen (iconRow2, 21)
    icon_getTen (iconRow3, 31)
    icon_getTen (iconRow4, 41)
    icon_getTen (iconRow5, 51)
    icon_getTen (iconRow6, 61)
    icon_getTen (iconRow7, 71)
    icon_getTen (iconRow8, 81)
    icon_getTen (iconRow9, 91)

def icon_display(scale):
  
    for row in icon:
        i = 0
        while i != scale:
            for element in row:
                if element == 0:
                    element = " " * scale
                else:
                    element = "#" * scale
                print(element, end=' ')
            print()
            i += 1
    

"""Main program begins here"""

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

print('\n==========     ICON RENDERING TOOL     ==========\n')
print(''' This program will ask you to enter 100 digits
 as 1s (ON) and 0s (OFF) to render your icon.\n''')
print('=================================================')
ready = input('Press ENTER when you are ready to begin.')

#icon_getData()

icon = [iconRow0, iconRow1, iconRow2, iconRow3, iconRow4,
        iconRow5, iconRow6,iconRow7, iconRow8, iconRow9]

#input_scale = 0
input_scale = int(input('Enter the scale (as a whole number) to display your icon: '))
#try:
#    while input_scale <= 0:
#        int(input('Please enter a value greater than zero: '))
#except ValueError:
#    print('Scale must be greater than zero.')
      

icon_display(input_scale)
