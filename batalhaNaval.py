#Imports
import numpy as np
import random as rd
import time as tm

#Variable

# Desenho padrão do campo
rowI = [' ',0,1,2,3,4,5,6,7,8,9]
row0 = [0,'_','_','_','_','_','_','_','_','_','_']
row1 = [1,'_','_','_','_','_','_','_','_','_','_']
row2 = [2,'_','_','_','_','_','_','_','_','_','_']
row3 = [3,'_','_','_','_','_','_','_','_','_','_']
row4 = [4,'_','_','_','_','_','_','_','_','_','_']
row5 = [5,'_','_','_','_','_','_','_','_','_','_']
row6 = [6,'_','_','_','_','_','_','_','_','_','_']
row7 = [7,'_','_','_','_','_','_','_','_','_','_']
row8 = [8,'_','_','_','_','_','_','_','_','_','_']
row9 = [9,'_','_','_','_','_','_','_','_','_','_']

np.array([rowI, row0, row1, row2, row3, row4, row5, row6, row7, row8, row9])

# Total de partes dos barcos para iniciar o jogo
playerParts = 8
computerParts = 8

# Flag para ver quem começa
startLottery = 0

# Contador de turnos
shift = 1

# Flag para saber se ainda falta acertar parte de algum barco
parts = False

# Flag para direção de teste para o tiro do computador
right = False
down = False
left = False

# Lista para guardar as jogadas já feitas pelo computador
computerShots = list()

# Lista para as possibilidades de jogadas feitas pelo jogador
possiblePlayerShots = list(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"))

# Linha e coluna do barco que ainda tem 1 parte para perder
remainingRow = 0
remainingColumn = 0

# Flag para marcar se o navio será posicionado verticalmente
vertical = "n"

# Campos
campPlayer = np.array([rowI, row0, row1, row2, row3, row4, row5, row6, row7, row8, row9]) # Campo do jogador
campComputer = np.array([rowI, row0, row1, row2, row3, row4, row5, row6, row7, row8, row9]) # Campo do computador
campShots = np.array([rowI, row0, row1, row2, row3, row4, row5, row6, row7, row8, row9]) # Campo para guardar os tiros do jogador

#Methods
def clear():
    print('\n' * 100)

def showCampPlayer():
    global campPlayer
    #print(*campPlayer, sep='\n')
    for i in range(11):
        print("[", end='')
        for j in range(10):
            if(campPlayer[i,j] == '-'):
                print("\x1b[44m'-'\x1b[0m,", end='')                
            elif(campPlayer[i,j] == '*'):
                print("\x1b[42m'*'\x1b[0m,", end='')                
            elif(campPlayer[i,j] == '+'):
                print("\x1b[41m'+'\x1b[0m,", end='')                
            else:
                print("\x1b[47m'%s'\x1b[0m," %campPlayer[i,j], end='')
        #Última coluna
        if(campPlayer[i,10] == '-'):
                print("\x1b[44m'-'\x1b[0m", end='')          
        elif(campPlayer[i,10] == '*'):
            print("\x1b[42m'*'\x1b[0m", end='')
        elif(campPlayer[i,10] == '+'):
            print("\x1b[41m'+'\x1b[0m", end='')
        else:
            print("\x1b[47m'%s'\x1b[0m" %campPlayer[i,10], end='')
        print("]")
    
def showCampComputer():
    global campComputer
    #print(*campComputer, sep='\n')
    for i in range(11):
        print("[", end='')
        for j in range(10):
            if(campComputer[i,j] == '-'):
                print("\x1b[44m'-'\x1b[0m,", end='')                
            elif(campComputer[i,j] == '*'):
                print("\x1b[42m'*'\x1b[0m,", end='')                
            elif(campComputer[i,j] == '+'):
                print("\x1b[41m'+'\x1b[0m,", end='')                
            else:
                print("\x1b[47m'%s'\x1b[0m," %campComputer[i,j], end='')
                
        #Última coluna
        if(campComputer[i,10] == '-'):
                print("\x1b[44m'-'\x1b[0m", end='')          
        elif(campComputer[i,10] == '*'):
            print("\x1b[42m'*'\x1b[0m", end='')
        elif(campComputer[i,10] == '+'):
            print("\x1b[41m'+'\x1b[0m", end='')
        else:
            print("\x1b[47m'%s'\x1b[0m" %campComputer[i,10], end='')
        print("]")
    
def showCampShots():
    global campShots
    #print(*campShots, sep='\n')
    for i in range(11):
        print("[", end='')
        for j in range(10):
            if(campShots[i,j] == '-'):
                print("\x1b[44m'-'\x1b[0m,", end='')                
            elif(campShots[i,j] == '*'):
                print("\x1b[42m'*'\x1b[0m,", end='')                
            elif(campShots[i,j] == '+'):
                print("\x1b[41m'+'\x1b[0m,", end='')                
            else:
                print("\x1b[47m'%s'\x1b[0m," %campShots[i,j], end='')
                
        #Última coluna
        if(campShots[i,10] == '-'):
                print("\x1b[44m'-'\x1b[0m", end='')          
        elif(campShots[i,10] == '*'):
            print("\x1b[42m'*'\x1b[0m", end='')
        elif(campShots[i,10] == '+'):
            print("\x1b[41m'+'\x1b[0m", end='')
        else:
            print("\x1b[47m'%s'\x1b[0m" %campShots[i,10], end='')
        print("]")

def addVerticalPlayerShip(row, column):
    global campPlayer
    campPlayer[row + 1, column + 1] = '*'
    campPlayer[row + 2, column + 1] = '*'
    
def addHorizontalPlayerShip(row, column):
    global campPlayer
    campPlayer[row + 1, column + 1] = '*'
    campPlayer[row + 1, column + 2] = '*'
    
def addVerticalComputerShip(row, column):
    global campComputer
    campComputer[row + 1, column + 1] = '*'
    campComputer[row + 2, column + 1] = '*'
    
def addHorizontalComputerShip(row, column):
    global campComputer
    campComputer[row + 1, column + 1] = '*'
    campComputer[row + 1, column + 2] = '*'
    
def addComputerShip():
    global campComputer
    while True:
        posLottery = rd.randrange(1, 3)
        if (posLottery == 1): # posicionamento vertical
            row = rd.randrange(0, 9)
            column = rd.randrange(0, 10)
            # verifica se o navio será posicionado totalmente dentro dos limites
            if (row < 9 and row > -1 and column < 10 and column > -1):
                # verifica se também não está sobrepondo algum outro navio
                if (campComputer[row + 1, column + 1] != '*' and campComputer[row + 2, column + 1] != '*'):
                    # verifica se também não está colado em outro navio
                    if (row > 0 and campComputer[row, column + 1] != '*' and row < 8 and campComputer[row + 3, column + 1] != '*'):
                        if (column > 0 and campComputer[row + 1, column] != '*' and campComputer[row + 2, column] != '*' and column < 9 and campComputer[row + 1, column + 2] != '*' and campComputer[row + 2, column + 2] != '*'):
                            addVerticalComputerShip(row, column)
                            break
                        elif (column == 0 and campComputer[row + 1, column + 2] != '*' and campComputer[row + 2, column + 2] != '*'):
                            addVerticalComputerShip(row, column)
                            break
                        elif (column == 9 and campComputer[row + 1, column] != '*' and campComputer[row + 2, column] != '*'):
                            addVerticalComputerShip(row, column)
                            break
                        else:
                            print("Posição inválida")
                    elif (row == 0 and campComputer[row + 3, column + 1] != '*'):
                        if (column > 0 and campComputer[row + 1, column] != '*' and campComputer[row + 2, column] != '*' and column < 9 and campComputer[row + 1, column + 2] != '*' and campComputer[row + 2, column + 2] != '*'):
                            addVerticalComputerShip(row, column)
                            break
                        elif (column == 0 and campComputer[row + 1, column + 2] != '*' and campComputer[row + 2, column + 2] != '*'):
                            addVerticalComputerShip(row, column)
                            break
                        elif (column == 9 and campComputer[row + 1, column] != '*' and campComputer[row + 2, column] != '*'):
                            addVerticalComputerShip(row, column)
                            break
                        else:
                            print("Posição inválida")
                    elif (column == 8 and campComputer[row + 1, column] != '*'):
                        if (row > 0 and campComputer[row, column + 1] != '*' and campComputer[row, column + 2] != '*' and row < 9 and campComputer[row + 2, column + 1] != '*' and campComputer[row + 2, column + 2] != '*'):
                            addVerticalComputerShip(row, column)
                            break
                        elif (row == 0 and campComputer[row + 2, column + 1] != '*' and campComputer[row + 2, column + 2] != '*'):
                            addVerticalComputerShip(row, column)
                            break
                        elif (row == 9 and campComputer[row, column + 1] != '*' and campComputer[row, column + 2] != '*'):
                            addVerticalComputerShip(row, column)
                            break
                        else:
                            print("Posição inválida")
                    else:
                        print("Posição inválida")
                else:
                    print("Posição inválida")                   
            else:
                print("Posição inválida")
        elif (posLottery == 2): # posicionamento horizontal
            row = rd.randrange(0, 10)
            column = rd.randrange(0, 9)
            # verifica se o navio será posicionado totalmente dentro dos limites
            if (row < 10 and row > -1 and column < 9 and column > -1):
                # verifica se também não está sobrepondo algum outro navio
                if (campComputer[row + 1, column + 1] != '*' and campComputer[row + 1, column + 2] != '*'):
                    # verifica se também não está colado em outro navio
                    if (column > 0 and campComputer[row + 1, column] != '*' and column < 8 and campComputer[row + 1, column + 3] != '*'):
                        if (row > 0 and campComputer[row, column + 1] != '*' and campComputer[row, column + 2] != '*' and row < 9 and campComputer[row + 2, column + 1] != '*' and campComputer[row + 2, column + 2] != '*'):
                            addHorizontalComputerShip(row, column)
                            break
                        elif (row == 0 and campComputer[row + 2, column + 1] != '*' and campComputer[row + 2, column + 2] != '*'):
                            addHorizontalComputerShip(row, column)
                            break
                        elif (row == 9 and campComputer[row, column + 1] != '*' and campComputer[row, column + 2] != '*'):
                            addHorizontalComputerShip(row, column)
                            break
                        else:
                            print("Posição inválida")
                    elif (column == 0 and campComputer[row + 1, column + 3] != '*'):
                        if (row > 0 and campComputer[row, column + 1] != '*' and campComputer[row, column + 2] != '*' and row < 9 and campComputer[row + 2, column + 1] != '*' and campComputer[row + 2, column + 2] != '*'):
                            addHorizontalComputerShip(row, column)
                            break
                        elif (row == 0 and campComputer[row + 2, column + 1] != '*' and campComputer[row + 2, column + 2] != '*'):
                            addHorizontalComputerShip(row, column)
                            break
                        elif (row == 9 and campComputer[row, column + 1] != '*' and campComputer[row, column + 2] != '*'):
                            addHorizontalComputerShip(row, column)
                            break
                        else:
                            print("Posição inválida")
                    elif (column == 8 and campComputer[row + 1, column] != '*'):
                        if (row > 0 and campComputer[row, column + 1] != '*' and campComputer[row, column + 2] != '*' and row < 9 and campComputer[row + 2, column + 1] != '*' and campComputer[row + 2, column + 2] != '*'):
                            addHorizontalComputerShip(row, column)
                            break
                        elif (row == 0 and campComputer[row + 2, column + 1] != '*' and campComputer[row + 2, column + 2] != '*'):
                            addHorizontalComputerShip(row, column)
                            break
                        elif (row == 9 and campComputer[row, column + 1] != '*' and campComputer[row, column + 2] != '*'):
                            addHorizontalComputerShip(row, column)
                            break
                        else:
                            print("Posição inválida")
                    else:
                        print("Posição inválida")
                else:
                    print("Posição inválida")                   
            else:
                print("Posição inválida")
                
def shotPlayer(row, column):
    global campComputer
    global campShots
    global computerParts
    if campComputer[row + 1, column + 1] == '*':
        print("Acertou!")
        computerParts -= 1
        campShots[row + 1, column + 1] = '+'
        campComputer[row + 1, column + 1] = '+'
        return True
    else:
        print("Errou!")
        campShots[row + 1, column + 1] = '-'
        campComputer[row + 1, column + 1] = '-'
        return False

# IA básico
def shotComputer():
    #Tempo de espera em segundos
    tm.sleep(2)
    global computerShots
    global campPlayer
    global playerParts
    global parts
    global right
    global down
    global left
    global remainingRow
    global remainingColumn
    if (parts == False):
        while (True):
            row = rd.randrange(1, 11)
            column = rd.randrange(1, 11)
            if ([row, column] not in computerShots):
                computerShots.append([row,column])
                break
        print("Tiro em %d, %d" %(row - 1,column - 1))
        if (campPlayer[row, column] == '*'):
            print("Acertou!")
            playerParts -= 1
            campPlayer[row, column] = '+'
            remainingRow = row
            remainingColumn = column
            parts = True
            return True
        else:
            print("Errou!")
            campPlayer[row, column] = '-'
            return True
    elif (right == False):
        if (remainingColumn + 1 < 11):
            print("Tiro em %d, %d" %(remainingRow - 1, remainingColumn))
            if campPlayer[remainingRow, remainingColumn + 1] == '*':
                computerShots.append([remainingRow, remainingColumn + 1])
                print("Afundou!")
                playerParts -= 1
                campPlayer[remainingRow, remainingColumn + 1] = '+'
                parts = False
                #right = False
                return True
            else:
                computerShots.append([remainingRow, remainingColumn + 1])
                print("Errou!")
                campPlayer[remainingRow, remainingColumn + 1] = '-'
                right = True
        else:
            right = True
    elif (down == False):
        if (remainingRow + 1 < 11):
            print("Tiro em %d, %d" %(remainingRow, remainingColumn - 1))
            if campPlayer[remainingRow + 1, remainingColumn] == '*':
                computerShots.append([remainingRow + 1, remainingColumn])
                print("Afundou!")
                playerParts -= 1
                campPlayer[remainingRow + 1, remainingColumn] = '+'
                parts = False
                right = False
                return True
            else:
                computerShots.append([remainingRow + 1, remainingColumn])
                print("Errou!")
                campPlayer[remainingRow + 1, remainingColumn] = '-'
                down = True
        else:
            down = True
    elif (left == False):
        if (remainingColumn - 1 > 1):
            print("Tiro em %d, %d" %(remainingRow, remainingColumn - 1))
            if campPlayer[remainingRow, remainingColumn - 1] == '*':
                computerShots.append([remainingRow, remainingColumn - 1])
                print("Afundou!")
                playerParts -= 1
                campPlayer[remainingRow, remainingColumn - 1] = '+'
                parts = False
                right = False
                down = False
                return True
            else:
                computerShots.append([remainingRow, remainingColumn - 1])
                print("Errou!")
                campPlayer[remainingRow, remainingColumn - 1] = '-'
                left = True
        else:
            left = True
    else:            
        print("Tiro em %d, %d" %(remainingRow - 1, remainingColumn))
        computerShots.append([remainingRow - 1, remainingColumn])
        print("Afundou!")
        playerParts -= 1
        campPlayer[remainingRow - 1, remainingColumn] = '+'
        parts = False
        right = False
        down = False
        left = False
        return True

# posicionamento dos navios
print("\nPosicione seus navios...")
for i in range(1, 5):
    showCampPlayer()
    while True:
        print("\n\n%dº navio:" %i)
        vertical = str(input("\tVertical (s/n): "))
        vertical = vertical[0]
        if vertical == 's':
            print("Posicionando navio vertical...")
            row = int(input("\tLinha: "))
            column = int(input("\tColuna: "))
            # verifica se o navio será posicionado totalmente dentro dos limites
            if (row < 9 and row > -1 and column < 10 and column > -1):
                # verifica se também não está sobrepondo algum outro navio
                if (campPlayer[row + 1, column + 1] != '*' and campPlayer[row + 2, column + 1] != '*'):
                    # verifica se também não está colado em outro navio
                    if (row > 0 and campPlayer[row, column + 1] != '*' and row < 8 and campPlayer[row + 3, column + 1] != '*'):
                        if (column > 0 and campPlayer[row + 1, column] != '*' and campPlayer[row + 2, column] != '*' and column < 9 and campPlayer[row + 1, column + 2] != '*' and campPlayer[row + 2, column + 2] != '*'):
                            addVerticalPlayerShip(row, column)
                            break
                        elif (column == 0 and campPlayer[row + 1, column + 2] != '*' and campPlayer[row + 2, column + 2] != '*'):
                            addVerticalPlayerShip(row, column)
                            break
                        elif (column == 9 and campPlayer[row + 1, column] != '*' and campPlayer[row + 2, column] != '*'):
                            addVerticalPlayerShip(row, column)
                            break
                        else:
                            print("Posição inválida")
                    elif (row == 0 and campPlayer[row + 3, column + 1] != '*'):
                        if (column > 0 and campPlayer[row + 1, column] != '*' and campPlayer[row + 2, column] != '*' and column < 9 and campPlayer[row + 1, column + 2] != '*' and campPlayer[row + 2, column + 2] != '*'):
                            addVerticalPlayerShip(row, column)
                            break
                        elif (column == 0 and campPlayer[row + 1, column + 2] != '*' and campPlayer[row + 2, column + 2] != '*'):
                            addVerticalPlayerShip(row, column)
                            break
                        elif (column == 9 and campPlayer[row + 1, column] != '*' and campPlayer[row + 2, column] != '*'):
                            addVerticalPlayerShip(row, column)
                            break
                        else:
                            print("Posição inválida")
                    elif (row == 8 and campPlayer[row + 1, column] != '*'):
                        if (column > 0 and campPlayer[row, column + 1] != '*' and campPlayer[row, column + 2] != '*' and column < 9 and campPlayer[row + 2, column + 1] != '*' and campPlayer[row + 2, column + 2] != '*'):
                            addVerticalPlayerShip(row, column)
                            break
                        elif (column == 0 and campPlayer[row + 2, column + 1] != '*' and campPlayer[row + 2, column + 2] != '*'):
                            addVerticalPlayerShip(row, column)
                            break
                        elif (column == 9 and campPlayer[row, column + 1] != '*' and campPlayer[row, column + 2] != '*'):
                            addVerticalPlayerShip(row, column)
                            break
                        else:
                            print("Posição inválida")
                    else:
                        print("Posição inválida")
                else:
                    print("Posição inválida")                   
            else:
                print("Posição inválida")
        elif vertical == 'n':
            print("Posicionando navio horizontal...")
            row = int(input("\tLinha: "))
            column = int(input("\tColuna: "))
            # verifica se o navio será posicionado totalmente dentro dos limites
            if (row < 10 and row > -1 and column < 9 and column > -1):
                # verifica se também não está sobrepondo algum outro navio
                if (campPlayer[row + 1, column + 1] != '*' and campPlayer[row + 1, column + 2] != '*'):
                    # verifica se também não está colado em outro navio
                    if (column > 0 and campPlayer[row + 1, column] != '*' and column < 8 and campPlayer[row + 1, column + 3] != '*'):
                        if (row > 0 and campPlayer[row, column + 1] != '*' and campPlayer[row, column + 2] != '*' and row < 9 and campPlayer[row + 2, column + 1] != '*' and campPlayer[row + 2, column + 2] != '*'):
                            addHorizontalPlayerShip(row, column)
                            break
                        elif (row == 0 and campPlayer[row + 2, column + 1] != '*' and campPlayer[row + 2, column + 2] != '*'):
                            addHorizontalPlayerShip(row, column)
                            break
                        elif (row == 9 and campPlayer[row, column + 1] != '*' and campPlayer[row, column + 2] != '*'):
                            addHorizontalPlayerShip(row, column)
                            break
                        else:
                            print("Posição inválida")
                    elif (column == 0 and campPlayer[row + 1, column + 3] != '*'):
                        if (row > 0 and campPlayer[row, column + 1] != '*' and campPlayer[row, column + 2] != '*' and row < 9 and campPlayer[row + 2, column + 1] != '*' and campPlayer[row + 2, column + 2] != '*'):
                            addHorizontalPlayerShip(row, column)
                            break
                        elif (row == 0 and campPlayer[row + 2, column + 1] != '*' and campPlayer[row + 2, column + 2] != '*'):
                            addHorizontalPlayerShip(row, column)
                            break
                        elif (row == 9 and campPlayer[row, column + 1] != '*' and campPlayer[row, column + 2] != '*'):
                            addHorizontalPlayerShip(row, column)
                            break
                        else:
                            print("Posição inválida")
                    elif (column == 8 and campPlayer[row + 1, column] != '*'):
                        if (row > 0 and campPlayer[row, column + 1] != '*' and campPlayer[row, column + 2] != '*' and row < 9 and campPlayer[row + 2, column + 1] != '*' and campPlayer[row + 2, column + 2] != '*'):
                            addHorizontalPlayerShip(row, column)
                            break
                        elif (row == 0 and campPlayer[row + 2, column + 1] != '*' and campPlayer[row + 2, column + 2] != '*'):
                            addHorizontalPlayerShip(row, column)
                            break
                        elif (row == 9 and campPlayer[row, column + 1] != '*' and campPlayer[row, column + 2] != '*'):
                            addHorizontalPlayerShip(row, column)
                            break
                        else:
                            print("Posição inválida")
                    else:
                        print("Posição inválida")
                else:
                    print("Posição inválida")                   
            else:
                print("Posição inválida")
        else:
            print("Posição inválida")
    addComputerShip()
    clear()

# exibe a grelha do jogador
showCampPlayer()

# exibe a grelha do computador
#showCampComputer()

# sorteio de quem começa
print("\nSorteando quem começa...")
tm.sleep(2)
startLottery = rd.randrange(1,3)
if (startLottery == 1):
    print("\nVocê começa jogando!")
else:
    print("\nO computador começa jogando!") 

# início do jogo
input("Pressione Enter para dar inicio às jogadas...")
print(clear)

while True:
    # se o jogador começa
    if (startLottery == 1):
        # Vez do jogador
        print("\nINICIANDO TURNO %d" %shift)
        print("\nVisão atual do campo inimigo:")
        showCampShots()
        while True:
            print("\nInicie sua jogada:")
            row = input("\tLinha: ")
            column = input("\tColuna: ")
            if (row in possiblePlayerShots and column in possiblePlayerShots):
                row = int(row)
                column = int(column)
                break
            else:
                print("Posição inválida!\n")
                
        shotPlayer(row, column)
        print("Partes restantes do computador: %d" %computerParts)
        if computerParts == 0 :
            print("Você ganhou!")
            break
        # Vez do computador
        print("\n\nJOGADA DO COMPUTADOR:")
        shotComputer()
        print("Seu campo")
        showCampPlayer()
        print("Suas partes restantes: %d" %playerParts)
        if (playerParts == 0):
            print("Computador ganhou!")
            break
        shift = shift + 1
        input("pressione 'Enter' para a próxima rodada...")
        clear()
    # se o computador começa
    else:
        # Vez do computador
        print("\nINICIANDO TURNO %d" %shift)
        print("\n\nJOGADA DO COMPUTADOR:")
        shotComputer()
        print("Seu campo:")
        showCampPlayer()
        print("Suas partes restantes: %d" %playerParts)
        if (playerParts == 0):
            print("Computador ganhou!")
            break   
        # Vez do jogador
        print("\nVisão atual do campo inimigo:")
        showCampShots()
        while True:
            print("\nInicie sua jogada:")
            row = input("\tLinha: ")
            column = input("\tColuna: ")
            if (row in possiblePlayerShots and column in possiblePlayerShots):
                row = int(row)
                column = int(column)
                break
            else:
                print("Posição inválida!\n")
        shotPlayer(row, column)
        print("Unidades partes do computador: %d" %computerParts)
        if computerParts == 0 :
            print("Você ganhou!")
            break
        shift = shift + 1
        input("pressione 'Enter' para a próxima rodada...")
        clear()