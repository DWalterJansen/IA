#Imports
import numpy as np
import random as rd
import os as os
from IPython.display import clear_output

#Variable

#Desenho padrão do campo
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

grid = np.array([rowI, row0, row1, row2, row3, row4, row5, row6, row7, row8, row9])

#Total de partes dos barcos para iniciar o jogo
partsPlayer = 8
partsRobot = 8

#Flag para saber se ainda falta acetar parte de algum barco
parts = False

#Flag para direção de teste para o tiro da máquina
right = False

#Lista para guardar as jogadas já feitas pela máquina
robotShots = list()

# Listas para guardar o início de cada barco posicionado (coordenada mais a esquerda)
leftPlayerCoord = list()
leftRobotCoord = list()

# Coordenadas para a primeira jogada da IA que gera uma sequência de jogadas na horizontal
rowCheckpoint = 0
columnCheckpoint = 0

#Linha e Coluna do barco que ainda tem 1 parte para perder
rowRemain = 0
columnRemain = 0
extraRowRemain = 0
extraColumnRemain = 0

#Campos
campPlayer = np.array([rowI, row0, row1, row2, row3, row4, row5, row6, row7, row8, row9]) #Campo onde o player posiciona seus barcos
campRobot = np.array([rowI, row0, row1, row2, row3, row4, row5, row6, row7, row8, row9]) #Campo onde o robô posiciona seus barcos
campShots = np.array([rowI, row0, row1, row2, row3, row4, row5, row6, row7, row8, row9]) #Campo para guardar os tiros do jogador

#Debug
#campPlayer = grid #Campo onde o player posiciona seus barcos
#campRobot = grid #Campo onde o robô posiciona seus barcos
#campShots = grid #Campo para guardar os tiros do jogador

#Methods
def showCampPlayer():
    global campPlayer 
    print(*campPlayer, sep = '\n')
    
def showCampRobot():
    global campRobot
    print(*campRobot, sep = '\n')
    
def showCampShots():
    global campShots
    print(*campShots, sep = '\n')

def addBoatPlayer(row, column):
    global campPlayer
    campPlayer[row + 1, column + 1] = '*'
    campPlayer[row + 1, column + 2] = '*'
    leftPlayerCoord.append([row, column])
    
def addBoatRobot():
    global campRobot
    while True:
        row = rd.randrange(1, 11)
        column = rd.randrange(1, 10)
        if (campRobot[row, column] != '*' and campRobot[row, column + 1] != '*'):
            campRobot[row, column] = '*'
            campRobot[row, column + 1] ='*'
            leftRobotCoord.append([row, column])
            print(row)
            print(column)
            break
    
def shotPlayer(row, column):
    global campRobot
    global campShots
    global partsRobot   
    if campRobot[row + 1, column + 1] == '*':
        print("Acertou!")
        partsRobot -= 1
        campShots[row + 1, column + 1] = '+'
        campRobot[row + 1, column + 1] = '+'
        # se acertou o lado esquerdo de um barco, verifica se o lado direito já foi atingido
        if ([row + 1, column + 1] in leftRobotCoord) and (campRobot[row + 1, column + 2] == '+'):
            print("Barco afundado!")
        # se acertou o lado direito de um barco, verifica se o lado esquerdo já foi atingido
        elif ([row + 1, column] in leftRobotCoord) and (campRobot[row + 1, column] == '+'):
            print("Barco afundado!")
        return True
    else:
        print("Errou!")
        campShots[row + 1, column + 1] = '-'
        campRobot[row + 1, column + 1] = '-'
        return False

#Basic IA
def shotRobot():
    global robotShots
    global campPlayer
    global partsPlayer
    global parts
    global right
    global rowRemain
    global columnRemain
    global rowCheckpoint
    global columnCheckpoint
    if parts == False:
        while True:
            row = rd.randrange(1, 10)
            column = rd.randrange(1, 10)
            if [row, column] not in robotShots:
                robotShots.append([row, column])
                break
        print("IF: Tiro em %d, %d" %(row - 1, column - 1))
        rowCheckpoint = row
        columnCheckpoint = column
        if campPlayer[row, column] == '*':
            print("Acertou!")
            partsPlayer -= 1
            campPlayer[row, column] = '+'
            rowRemain = row
            columnRemain = column
            parts = True
            return True
        else:
            print("Errou!")
            campPlayer[row, column] = '-'
            return True
    elif right == False: # se acertou anteriormente um navio que não foi afundado e ainda não checou a direita
        print("ELIF: Tiro em %d, %d" %(rowRemain - 1, columnRemain)) # chuta a coordenada imediatamente a direita
        if (columnRemain + 1) < 11 and campPlayer[rowRemain, columnRemain + 1] == '*':
            robotShots.append([rowRemain, columnRemain + 1])
            print("Acertou!")
            partsPlayer -= 1
            campPlayer[rowRemain, columnRemain + 1] = '+'
            # se acertou o lado direito de um barco, verifica se o lado esquerdo já foi atingido
            if ([rowRemain + 1, columnRemain - 1] in leftPlayerCoord) and (campPlayer[rowRemain + 1, columnRemain] == '+'):
                parts = False
                right = False
                rowRemain = 0
                columnRemain = 0
                print("Barco afundado!")
            else:
                parts = True
                right = True
                rowCheckpoint = rowRemain
                columnCheckpoint = columnRemain - 1
                print("row %d, column %d" %(rowRemain, columnRemain))
            return True
        elif (columnRemain + 1) < 11:
            robotShots.append([rowRemain, columnRemain + 1])
            print("Errou!")
            campPlayer[rowRemain, columnRemain + 1] = '-'
            right = True
            rowCheckpoint = rowRemain
            columnCheckpoint = columnRemain - 1
        else:
            print("Fora dos limites")
            right = True
            rowCheckpoint = rowRemain
            columnCheckpoint = columnRemain - 1
    else: # quando o barco mais a direita estiver afundado ou não for possível atingir a direita, acerta o checkpoint
        # tem que ter outro passo aqui, pois passa direto pro checkpoint sem antes destruir a posição mais a direita
        # do barco mais a direita
        print("ELSE: Tiro em %d, %d" %(rowCheckpoint, columnCheckpoint))
        robotShots.append([rowCheckpoint, columnCheckpoint])
        if (columnCheckpoint) > 0 and campPlayer[rowCheckpoint, columnCheckpoint] == '*':
            print("Acertou!")
            partsPlayer -= 1
            campPlayer[rowCheckpoint, columnCheckpoint] = '+'
            # se acertou o lado esquerdo de um barco, verifica se o lado direito já foi atingido
            if ([rowCheckpoint, columnCheckpoint] in leftPlayerCoord) and (campPlayer[rowCheckpoint + 1, columnCheckpoint + 2] == '+'):
                parts = False
                right = False
                rowRemain = 0
                columnRemain = 0
                print("Barco afundado! finalmente")
        return True

#global campShots
print("\nPosicione seus navios...")

for i in range(1,5):
    showCampPlayer()
    print("\n\n%dº barco:" %i)
    row = int(input("\tLinha: "))
    column = int(input("\tColuna: "))
    #input("\npressione qualquer tecla para continuar...")
    while True:
        if [row, column] in leftPlayerCoord:
            print("Coordenada já utilizada, favor selecionar uma coordenada diferente.\n")
            row = int(input("\tLinha: "))
            column = int(input("\tColuna: "))
        else:
            break
    addBoatPlayer(row, column)
    addBoatRobot()
    #os.system('cls' if os.name == 'nt' else 'clear')
    clear_output()

showCampPlayer()

while True:
    #Vez do Jogador
    print("INICIANDO JOGADAS")
    print("Visão atual do campo inimigo:")
    showCampShots()
    print("Inicie sua jogada:")
    row = int(input("\tLinha:"))
    column = int(input("\tColuna:"))
    shotPlayer(row, column)

    print("Partes Robot %d" %partsRobot)
    if partsRobot == 0 :
        print("Você Ganhou!")
        break

    #Vez da máquina
    print("Jogada da máquina:")
    shotRobot()
    showCampPlayer()
    print("Partes Player %d" %partsPlayer)
    if partsPlayer == 0 :
        print("Robot Ganhou!")
        break

    #input("\npressione qualquer tecla para continuar...")
    
    #Descomente a linha abaixo para limpar a tela a cada iterção
    #clear_output()
    
print(*campRobot, sep='\n')