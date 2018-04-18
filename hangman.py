from sys import argv
from random import randint

height = 30
message = ''

def main():
    global height
    global message

    try:
        words = getWords(argv[1])
    except IndexError:
        print('Name for words file not specified.')
        exit(1)
    
    if len(words) == 0:
        print('Invalid words file')
        exit(1)
        
    try:
        height = int(argv[2])
    except:
        pass
        message = 'Using default height'
        
    again = True
    while (again):
        guessedWord = words[randint(0, len(words) - 1)].upper()
        length = len(guessedWord)
        screen = initScreen(length)

        lifes = 3
        guessed = 0

        while (lifes > 0):
            printMessage()
            print(screen)
            print(getHearts(lifes))
            printEnters(height - 6)

            guess = input()
            if not guess.isalpha() or len(guess) != 1:
                message = 'Invalid input. Try again'
                continue

            result = setScreen(guess, guessedWord, screen, lifes)
            screen = result[0]
            lifes = result[1]
            guessed += result[2]

            if guessed == length:
                break

        again = gameOver(lifes, guessedWord)

    bye()
                    
def getWords(filename):
    try:
        file = open(filename, 'r')
        return [s.strip('\n') for s in file.readlines()]
    except IOError:
        print('Cannot open words file.')
        raise
    

def initScreen(length):
    screen = ''

    i = 0
    while (length > 0):
        screen += '_ '
        length -= 1
    
    return screen

def getHearts(lifes):
    hearts = ''

    while (lifes > 0):
        hearts += '♥'
        lifes -= 1
    
    return hearts

def setScreen(letter, word, screen, lifes):
    letter = letter.upper()
    newScreen = ''
    i = 0
    guessed = 0
    for l in word:
        if l == letter:
            newScreen += letter + ' '
            guessed += 1
        else:
            newScreen += screen[2 * i] + ' '
        i += 1

    if guessed == 0:
        lifes -= 1

    return (newScreen, lifes, guessed)

def printEnters(n):
    print('\n' * n)

def printMessage():
    global message
    print(message + '\n')
    message = ''

def gameOver (lifes, guessedWord):
    if lifes == 0:
        print('Game over!')
    else:
        print('Well done!')
            
    print('The word is: ', guessedWord)
    print('Play again? Y/N')
    printEnters(height - 5)

    a = ''
    while ( a != 'Y' and a != 'N'):
        a = input().upper()

    return a == 'Y'

def bye():
    print('Bye!')
    printEnters(height - 4)

main()


    