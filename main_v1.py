'''
GAVE UP
'''








import pygame
import random
import time
from sys import exit

class App:
    def addToLog(self, enemyX, enemyY, playerX, playerY, dmg, isCrit, isPlayer):
        if isPlayer:
            if isCrit:
                self.fightLog.append(f'{self.characterNames[self.inventory[self.playerTeam[playerX][playerY]]]} critted {self.characterNames[self.enemyTeam[enemyX][enemyY]]} with {dmg} dmg')
            else:
                self.fightLog.append(f'{self.characterNames[self.inventory[self.playerTeam[playerX][playerY]]]} attacked {self.characterNames[self.enemyTeam[enemyX][enemyY]]} with {dmg} dmg')
        
        if self.logSlot == 6:
            '''for log in range(6):
                self.fightLogTxt[self.logSlot + self.slotReduction - log] = self.font.render(self.fightLog[len(self.fightLog) - 1 - log], False, self.textColor)
            self.slotReduction += 1''' #BROKEN
        else:
            self.fightLogTxt[self.logSlot] = self.font.render(self.fightLog[len(self.fightLog) - 1], False, self.textColor)
        self.logSlot += 1
        
    def updateHp(self):
        for x in range(3):
            for y in range(3):
                if self.playerTeam[x][y] != 9:
                    self.playerHpTxt[x][y] = self.smallFont.render(f'{self.playerTeamHp[x][y]} / {self.stats[self.inventory[self.playerTeam[x][y]]][1]}', False, self.textColor)
                    # 50 - ((currentHp / maxHp * 100)) * .5)
                    self.playerHealthOffset[x][y] = 50 - ((self.playerTeamHp[x][y] / self.stats[self.inventory[self.playerTeam[x][y]]][1] * 100) * .5)
                else:
                    self.playerHpTxt[x][y] = self.smallFont.render('', False, self.textColor)
                if self.enemyTeam[x][y] != 9:
                    self.enemyHpTxt[x][y]  = self.smallFont.render(f'{self.enemyTeamHp[x][y]} / {self.stats[self.enemyTeam[x][y]][1]}', False, self.textColor)
                    self.enemyHealthOffset[x][y] = 50 - ((self.enemyTeamHp[x][y] / self.stats[self.enemyTeam[x][y]][1] * 100) * .5)
                else:
                    self.enemyHpTxt[x][y]  = self.smallFont.render('', False, self.textColor)
    
    def returnHp(self, x, y, isPlayer):
        if isPlayer:
            if self.playerTeam[x][y] != 9:
                return self.stats[self.inventory[self.playerTeam[x][y]]][1]
            else:
                return 0
        else:
            if self.enemyTeam[x][y] != 9:
                return self.stats[self.enemyTeam[x][y]][1]
            else:
                return 0
    
    def takeFirst(self, elem):
        return elem[0]
    
    def preFightSetup(self):
        # sort playorder from highest speed to lowest
        self.playOrder = []
        for x in range(3):
            for y in range(3):
                if self.playerTeam[x][y] != 9:
                    self.playOrder.append([self.stats[self.inventory[self.playerTeam[x][y]]][5], x, y, 'player'])
                if self.enemyTeam[x][y] != 9:
                    self.playOrder.append([self.stats[self.enemyTeam[x][y]][5], x, y, 'enemy'])
        # speed, x, y, team
        self.playOrder.sort(key=self.takeFirst, reverse=True)
        print(self.playOrder)
        
        # setup both teams hp stats
        self.playerTeamHp = [[self.returnHp(0, 0, True), self.returnHp(0, 1, True), self.returnHp(0, 2, True)],
                             [self.returnHp(1, 0, True), self.returnHp(1, 1, True), self.returnHp(1, 2, True)],
                             [self.returnHp(2, 0, True), self.returnHp(2, 1, True), self.returnHp(2, 2, True)]]
        self.enemyTeamHp = [[self.returnHp(0, 0, False), self.returnHp(0, 1, False), self.returnHp(0, 2, False)],
                             [self.returnHp(1, 0, False), self.returnHp(1, 1, False), self.returnHp(1, 2, False)],
                             [self.returnHp(2, 0, False), self.returnHp(2, 1, False), self.returnHp(2, 2, False)]]
        self.updateHp()
    
    def playMove(self):
        self.playerToEnemyRange = [[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]]
        self.enemyToPlayerRange = [[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]]
        self.attackedSlots = []
        
        if self.playOrder[self.moveNum][3] == 'player':
            # set player pov range
            if self.playOrder[self.moveNum][1] == 0:
                count = 0
                for y in range(3):
                    for x in range(3):
                        self.playerToEnemyRange[x][y] = count
                        count += 1
            elif self.playOrder[self.moveNum][1] == 1:
                count = 0
                for y in range(3):
                    self.playerToEnemyRange[self.playOrder[self.moveNum][1] - 1][y] = 1 + count
                    self.playerToEnemyRange[self.playOrder[self.moveNum][1]][y] = 0 + count
                    self.playerToEnemyRange[self.playOrder[self.moveNum][1] + 1][y] = 1 + count
                    count += 1
            elif self.playOrder[self.moveNum][1] == 2:
                count = 0
                for y in range(3):
                    for x in reversed(range(3)):
                        self.playerToEnemyRange[x][y] = count
                        count += 1
            # player move
            if self.characterMoves[self.inventory[self.playerTeam[self.playOrder[self.moveNum][1]][self.playOrder[self.moveNum][2]]]][self.roundNum][0] == 'front':
                for _ in range(self.characterMoves[self.inventory[self.playerTeam[self.playOrder[self.moveNum][1]][self.playOrder[self.moveNum][2]]]][self.roundNum][1]):
                    for i in range(9):
                        for x in range(3):
                            for y in range(3):
                                if self.playerToEnemyRange[x][y] == i and (x, y) not in self.attackedSlots and self.enemyTeamHp[x][y] != 0 and len(self.attackedSlots) != self.characterMoves[self.inventory[self.playerTeam[self.playOrder[self.moveNum][1]][self.playOrder[self.moveNum][2]]]][self.roundNum][1]:
                                    self.attackedSlots.append((x, y))
                                    self.enemyTeamHp[x][y] -= (self.characterMoves[self.inventory[self.playerTeam[self.playOrder[self.moveNum][1]][self.playOrder[self.moveNum][2]]]][self.roundNum][2] / 100) * self.stats[self.inventory[self.playerTeam[self.playOrder[self.moveNum][1]][self.playOrder[self.moveNum][2]]]][0]
                                    self.addToLog(x, y, self.playOrder[self.moveNum][1], self.playOrder[self.moveNum][2], (self.characterMoves[self.inventory[self.playerTeam[self.playOrder[self.moveNum][1]][self.playOrder[self.moveNum][2]]]][self.roundNum][2] / 100) * self.stats[self.inventory[self.playerTeam[self.playOrder[self.moveNum][1]][self.playOrder[self.moveNum][2]]]][0], False, True)
                                    
            elif self.characterMoves[self.inventory[self.playerTeam[self.playOrder[self.moveNum][1]][self.playOrder[self.moveNum][2]]]][self.roundNum][0] == 'back':
                print('back')
            elif self.characterMoves[self.inventory[self.playerTeam[self.playOrder[self.moveNum][1]][self.playOrder[self.moveNum][2]]]][self.roundNum][0] == 'all':
                print('all')
            elif self.characterMoves[self.inventory[self.playerTeam[self.playOrder[self.moveNum][1]][self.playOrder[self.moveNum][2]]]][self.roundNum][0] == 'heal':
                print('heal')
            elif self.characterMoves[self.inventory[self.playerTeam[self.playOrder[self.moveNum][1]][self.playOrder[self.moveNum][2]]]][self.roundNum][0] == 'random':
                print('random')
        else:
            # set enemy pov range
            if self.playOrder[self.moveNum][1] == 0:
                count = 0
                for y in reversed(range(3)):
                    for x in range(3):
                        self.enemyToPlayerRange[x][y] = count
                        count += 1
            elif self.playOrder[self.moveNum][1] == 1:
                count = 0
                for y in reversed(range(3)):
                    self.enemyToPlayerRange[self.playOrder[self.moveNum][1] - 1][y] = 1 + count
                    self.enemyToPlayerRange[self.playOrder[self.moveNum][1]][y] = 0 + count
                    self.enemyToPlayerRange[self.playOrder[self.moveNum][1] + 1][y] = 1 + count
            elif self.playOrder[self.moveNum][1] == 2:
                count = 0
                for y in reversed(range(3)):
                    for x in reversed(range(3)):
                        self.enemyToPlayerRange[x][y] = count
                        count += 1
            # enemy move
            
        
        self.updateHp()
        self.moveNum += 1
        if self.moveNum == len(self.playOrder):
            self.moveNum = 0
            self.roundNum += 1
            if self.roundNum == 4:
                self.roundNum = 0
        if self.playMoveInstantly:
            self.playMoveInstantly = False
        else:
            self.startTime += self.delay
    
    def showLockedStages(self):
        for stage in range(6):
            if self.completedStages >= stage:
                self.stageTxt[stage] = self.font.render(f'Stage {stage + 1}', False, self.textColor)
            else:
                self.stageTxt[stage] = self.font.render(f'Stage {stage + 1}', False, self.lockedColor)
    
    def trainRandomChar(self):
        randomChar = random.randrange(4, 8)
        randomStat = random.randrange(5)
        statNames     = ['Attack', 'Health', 'Defence %', 'Crit %', 'Crit Dmg %']
        statIncreases = [5, 5, 5, 5, 10]
        self.characterTrainedTxt = self.font.render(f'{self.characterNames[randomChar]} trained {statNames[randomStat]} by +{statIncreases[randomStat]}', False, self.textColor)
        self.stats[randomChar][randomStat] += statIncreases[randomStat]
    
    def closeButtonEvent(self):
        self.screen = pygame.display.set_mode((500, 800))
        self.clickedSlot = len(self.inventory)
        self.teamTextsNum = 0
    
    def showCharacterStats(self, slot):
        self.screen = pygame.display.set_mode((1000, 800))
        self.teamTextsNum = 1
        self.characterName = self.font.render(self.characterNames[self.inventory[slot]], False, self.textColor)
        self.dmgStatNum    = self.font.render(str(self.stats[self.inventory[slot]][0]), False, self.textColor)
        self.hpStatNum     = self.font.render(str(self.stats[self.inventory[slot]][1]), False, self.textColor)
        self.defStatNum    = self.font.render(str(self.stats[self.inventory[slot]][2]) + '%', False, self.textColor)
        self.critCStatNum  = self.font.render(str(self.stats[self.inventory[slot]][3]) + '%', False, self.textColor)
        self.critDStatNum  = self.font.render(str(self.stats[self.inventory[slot]][4]) + '%', False, self.textColor)
        self.speedStatNum  = self.font.render(str(self.stats[self.inventory[slot]][5]), False, self.textColor)
        
        self.moveDescTxt[0] = self.font.render(self.characterMovesTxt[self.inventory[slot]][0], False, self.textColor)
        self.moveDescTxt[1] = self.font.render(self.characterMovesTxt[self.inventory[slot]][1], False, self.textColor)
        self.moveDescTxt[2] = self.font.render(self.characterMovesTxt[self.inventory[slot]][2], False, self.textColor)
        self.moveDescTxt[3] = self.font.render(self.characterMovesTxt[self.inventory[slot]][3], False, self.textColor)
    
    def startGame(self):
        while True:
            # events
            for event in pygame.event.get():
                # close game event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # click events
                if event.type == pygame.MOUSEBUTTONUP:
                    # Menu screen
                    if self.gameState == 'Menu':
                        # fight button
                        if self.fightBtn.collidepoint(event.pos):
                            self.screen = pygame.display.set_mode((440, 335))
                            self.gameState = 'Fights'
                            self.showLockedStages()
                        # train button
                        elif self.trainBtn.collidepoint(event.pos):
                            self.screen = pygame.display.set_mode((500, 650))
                            self.gameState = 'Train'
                        # team button
                        elif self.teamBtn.collidepoint(event.pos):
                            self.screen = pygame.display.set_mode((500, 800))
                            self.gameState = 'Team'
                    # Fights screen
                    elif self.gameState == 'Fights':
                        # stage buttons
                        for stage in range(6):
                            if self.stageBtns[stage].collidepoint(event.pos) and self.completedStages >= stage and self.playerTeam != [[9, 9, 9],
                                                                                                                                       [9, 9, 9],
                                                                                                                                       [9, 9, 9]]:
                                self.gameState = 'Stages'
                                self.enemyTeam = self.stageLayouts[stage]
                                self.stageNumTxt = self.font.render(f'Stage {stage + 1}', False, self.textColor)
                                self.screen = pygame.display.set_mode((800, 800))
                                self.startTime = round(time.time() * 1000)
                                self.preFightSetup()
                        # back button
                        if self.backBtn1.collidepoint(event.pos):
                            self.gameState = 'Menu'
                            self.screen = pygame.display.set_mode((235, 350))
                    # Team screen
                    elif self.gameState == 'Team':
                        # back button
                        if self.backBtn2.collidepoint(event.pos):
                            self.gameState = 'Menu'
                            self.screen = pygame.display.set_mode((235, 350))
                        # unequip button
                        elif self.unequipBtn.collidepoint(event.pos) and self.unequipBtnBool == True:
                            self.inTeam[self.playerTeam[self.clickedSlot3x3[0]][self.clickedSlot3x3[1]]] = False
                            self.playerTeam[self.clickedSlot3x3[0]][self.clickedSlot3x3[1]] = 9
                            self.closeButtonEvent()
                        # change formation
                        elif self.formationBtn.collidepoint(event.pos):
                            self.clickedSlot = len(self.inventory)
                            self.teamTextsNum = 0
                            self.screen = pygame.display.set_mode((1000, 800))
                        # close button
                        elif self.closeBtn.collidepoint(event.pos):
                            self.closeButtonEvent()
                        # click inv slots
                        for slot in range(8):
                            if self.invBtns[slot].collidepoint(event.pos) and self.inTeam[slot] == False:
                                self.clickedSlot = slot
                                self.showCharacterStats(slot)
                                self.unequipBtnBool = False
                        # change formation
                        for formation in range(6):
                            if self.chooseFormation[formation].collidepoint(event.pos):
                                self.formation = formation
                                self.playerTeam = [[9, 9, 9],
                                                   [9, 9, 9],
                                                   [9, 9, 9]]
                                for num in range(8):
                                    self.inTeam[num] = False
                        # click formation slots
                        for x in range(3):
                            for y in range(3):
                                if self.formationBtns[x][y].collidepoint(event.pos) and self.formations[self.formation][x][y] == 1 and self.clickedSlot < len(self.inventory) and self.playerTeam[x][y] == 9:
                                    self.playerTeam[x][y] = self.clickedSlot
                                    self.inTeam[self.clickedSlot] = True
                                    self.closeButtonEvent()
                                elif self.formationBtns[x][y].collidepoint(event.pos) and self.playerTeam[x][y] != 9:
                                    self.showCharacterStats(self.playerTeam[x][y])
                                    self.clickedSlot = len(self.inventory)
                                    self.unequipBtnBool = True
                                    self.clickedSlot3x3 = (x, y)
                    # Train screen
                    elif self.gameState == 'Train':
                        # train button
                        if self.trainBtn2.collidepoint(event.pos):
                            self.trainRandomChar()
                        # back button
                        elif self.backBtn3.collidepoint(event.pos):
                            self.gameState = 'Menu'
                            self.screen = pygame.display.set_mode((235, 350))
                    # Stages screen
                    elif self.gameState == 'Stages':
                        # abandon button
                        if self.abandonBtn.collidepoint(event.pos):
                            self.gameState = 'Menu'
                            self.screen = pygame.display.set_mode((235, 350))
                            self.playMoveInstantly = True
                            self.roundNum = 0
                            self.moveNum = 0
                            self.slotReduction = 0
                            self.fightLog = []
                            
            self.screen.fill('black')
            #draw game
            if self.gameState == 'Menu':
                self.screen.blit(self.BtnBgColorBox, (50, 50))
                self.screen.blit(self.fightTxt, (50 + 40, 50 + 12))
                self.screen.blit(self.BtnBgColorBox, (50, 150))
                self.screen.blit(self.trainTxt, (50 + 40, 150 + 12))
                self.screen.blit(self.BtnBgColorBox, (50, 250))
                self.screen.blit(self.teamTxt, (50 + 40, 250 + 12))
            elif self.gameState == 'Fights':
                self.screen.blit(self.BtnBgColorBox, (50, 30))
                self.screen.blit(self.stageTxt[0], (50 + 30, 30 + 12))
                self.screen.blit(self.BtnBgColorBox, (50, 100))
                self.screen.blit(self.stageTxt[1], (50 + 30, 100 + 12))
                self.screen.blit(self.BtnBgColorBox, (50, 170))
                self.screen.blit(self.stageTxt[2], (50 + 30, 170 + 12))
                
                self.screen.blit(self.BtnBgColorBox, (250, 30))
                self.screen.blit(self.stageTxt[3], (250 + 30, 30 + 12))
                self.screen.blit(self.BtnBgColorBox, (250, 100))
                self.screen.blit(self.stageTxt[4], (250 + 30, 100 + 12))
                self.screen.blit(self.BtnBgColorBox, (250, 170))
                self.screen.blit(self.stageTxt[5], (250 + 30, 170 + 12))
                
                self.screen.blit(self.BtnBgColorBox, (250, 260))
                self.screen.blit(self.backTxt, (250 + 40, 260 + 12))
            elif self.gameState == 'Team':
                self.screen.blit(self.formationImgs[self.formation], (225, 20))
                
                xAdd = 0
                yAdd = 0
                count = 0
                for y in range(2):
                    for x in range(4):
                        if self.clickedSlot == count:
                            self.screen.blit(self.activeSlot, (75 + xAdd, 500 + yAdd))
                        elif self.inTeam[count] == False:
                            self.screen.blit(self.usableSlot, (75 + xAdd, 500 + yAdd))
                        else:
                            self.screen.blit(self.lockedSlot, (75 + xAdd, 500 + yAdd))
                        self.screen.blit(self.characters[self.inventory[count]], (75 + xAdd, 500 + yAdd))
                        self.invBtns[count] = pygame.Rect(75 + xAdd, 500 + yAdd, 50, 50)
                        count += 1
                        xAdd += 100
                    xAdd = 0
                    yAdd = 100
                
                self.screen.blit(self.BtnBgColorBox, (350, 740))
                self.screen.blit(self.backTxt, (350 + 40, 740 + 12))
                
                self.screen.blit(self.screenSplit, (500, 0))
                
                for x in range(3):
                    for y in range (3):
                        if self.formations[self.formation][x][y] == 1:
                            self.screen.blit(self.usableSlot, self.slotCoords[y][x])
                            if self.playerTeam[x][y] < 9:
                                self.screen.blit(self.characters[self.inventory[self.playerTeam[x][y]]], self.slotCoords[y][x])
                        else:
                            self.screen.blit(self.lockedSlot, self.slotCoords[y][x])
                            
                self.screen.blit(self.teamTexts[self.teamTextsNum], (670, 20))
                if self.teamTextsNum == 0:
                    self.screen.blit(self.formationImgs[0], (630, 150))
                    self.screen.blit(self.formationImgs[1], (730, 150))
                    self.screen.blit(self.formationImgs[2], (830, 150))
                    self.screen.blit(self.formationImgs[3], (630, 250))
                    self.screen.blit(self.formationImgs[4], (730, 250))
                    self.screen.blit(self.formationImgs[5], (830, 250))
                else:
                    self.screen.blit(self.characterName, (725, 50))
                    
                    self.screen.blit(self.dmgStatText, (550, 200))
                    self.screen.blit(self.hpStatText, (550, 230))
                    self.screen.blit(self.defStatText, (550, 260))
                    self.screen.blit(self.critCStatText, (550, 290))
                    self.screen.blit(self.critDStatText, (550, 320))
                    self.screen.blit(self.speedStatText, (550, 350))
                    
                    self.screen.blit(self.dmgStatNum, (900, 200))
                    self.screen.blit(self.hpStatNum, (900, 230))
                    self.screen.blit(self.defStatNum, (900, 260))
                    self.screen.blit(self.critCStatNum, (900, 290))
                    self.screen.blit(self.critDStatNum, (900, 320))
                    self.screen.blit(self.speedStatNum, (900, 350))
                    
                    self.screen.blit(self.infoText, (550, 120))
                self.screen.blit(self.moveInfoTxt[0], (550, 400))
                self.screen.blit(self.moveInfoTxt[1], (550, 475))
                self.screen.blit(self.moveInfoTxt[2], (550, 550))
                self.screen.blit(self.moveInfoTxt[3], (550, 625))
                self.screen.blit(self.moveDescTxt[0], (550, 400 + 30))
                self.screen.blit(self.moveDescTxt[1], (550, 475 + 30))
                self.screen.blit(self.moveDescTxt[2], (550, 550 + 30))
                self.screen.blit(self.moveDescTxt[3], (550, 625 + 30))
                if self.unequipBtnBool == True:
                    self.screen.blit(self.BtnBgColorBox, (515, 740))
                    self.screen.blit(self.unequipTxt, (515 + 30, 740 + 12))
                self.screen.blit(self.BtnBgColorBox, (850, 740))
                self.screen.blit(self.closeTxt, (850 + 40, 740 + 12))
            elif self.gameState == 'Train':
                self.screen.blit(self.magicalTreeImg, (60, 20))
                self.screen.blit(self.trainInfoTxt, (5, 410))
                self.screen.blit(self.BtnBgColorBox, (180, 450))
                self.screen.blit(self.trainTxt, (180 + 40, 450 + 12))
                self.screen.blit(self.characterTrainedTxt, (110, 530))
                self.screen.blit(self.BtnBgColorBox, (350, 590))
                self.screen.blit(self.backTxt, (350 + 40, 590 + 12))
            elif self.gameState == 'Stages':
                self.screen.blit(self.stageNumTxt, (365, 20))
                self.screen.blit(self.usableSlot, (375, 175))
                for x in range(3):
                    for y in range (3):
                        # player slot
                        if self.playerTeam[x][y] < 9:
                            self.screen.blit(self.usableSlot, (self.slotCoords[y][x][0] - 100, self.slotCoords[y][x][1] - 50))
                            self.screen.blit(self.playerHpTxt[x][y], (self.slotCoords[y][x][0] - 100, self.slotCoords[y][x][1] - 80))
                            self.screen.blit(self.playerHealthBarsBg[x][y], (self.slotCoords[y][x][0] - 100, self.slotCoords[y][x][1] - 65))
                            self.screen.blit(self.playerHealthBars[x][y], (self.slotCoords[y][x][0] - 100 - self.playerHealthOffset[x][y], self.slotCoords[y][x][1] - 65))
                            self.screen.blit(self.playerHealthFiller[x][y], (self.slotCoords[y][x][0] - 150, self.slotCoords[y][x][1] - 65))
                            if x == self.playOrder[self.moveNum - 1][1] and y == self.playOrder[self.moveNum - 1][2] and self.playOrder[self.moveNum - 1][3] == 'player':
                                self.screen.blit(self.characters[self.inventory[self.playerTeam[x][y]]], (375, 175))
                            else:
                                self.screen.blit(self.characters[self.inventory[self.playerTeam[x][y]]], (self.slotCoords[y][x][0] - 100, self.slotCoords[y][x][1] - 50))
                        else:
                            self.screen.blit(self.lockedSlot, (self.slotCoords[y][x][0] - 100, self.slotCoords[y][x][1] - 50))
                        # enemy slot
                        if self.enemyTeam[x][y] != 9:
                            self.screen.blit(self.usableSlot, (self.slotCoords[y][x][0] + 400, self.slotCoords[y][x][1] - 50))
                            self.screen.blit(self.enemyHpTxt[x][y], (self.slotCoords[y][x][0] + 400, self.slotCoords[y][x][1] - 80))
                            self.screen.blit(self.enemyHealthBarsBg[x][y], (self.slotCoords[y][x][0] + 400, self.slotCoords[y][x][1] - 65))
                            self.screen.blit(self.enemyHealthBars[x][y], (self.slotCoords[y][x][0] + 400 - self.enemyHealthOffset[x][y], self.slotCoords[y][x][1] - 65))
                            self.screen.blit(self.enemyHealthFiller[x][y], (self.slotCoords[y][x][0] + 350, self.slotCoords[y][x][1] - 65))
                            if x == self.playOrder[self.moveNum - 1][1] and y == self.playOrder[self.moveNum - 1][2] and self.playOrder[self.moveNum - 1][3] == 'enemy':
                                self.screen.blit(self.characters[self.enemyTeam[x][y]], (375, 175))
                            else:
                                self.screen.blit(self.characters[self.enemyTeam[x][y]], (self.slotCoords[y][x][0] + 400, self.slotCoords[y][x][1] - 50))
                        else:
                            self.screen.blit(self.lockedSlot, (self.slotCoords[y][x][0] + 400, self.slotCoords[y][x][1] - 50))
                
                self.screen.blit(self.fightLogBg, (50 - 10, 400 - 10))
                self.screen.blit(self.fightLogTxt[0], (50, 400))
                self.screen.blit(self.fightLogTxt[1], (50, 450))
                self.screen.blit(self.fightLogTxt[2], (50, 500))
                self.screen.blit(self.fightLogTxt[3], (50, 550))
                self.screen.blit(self.fightLogTxt[4], (50, 600))
                self.screen.blit(self.fightLogTxt[5], (50, 650))
                
                self.screen.blit(self.BtnBgColorBox, (650, 740))
                self.screen.blit(self.abandonTxt, (650 + 25, 740 + 12))
                
                if self.playMoveInstantly:
                    self.playMove()
                if self.startTime + self.delay <= round(time.time() * 1000):
                    self.playMove()
                        
            # update game 60fps
            pygame.display.update()
            self.clock.tick(60)
                
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.display.set_caption('Dmg game')
        # set variables
        self.screen = pygame.display.set_mode((1000, 800))
        self.clock = pygame.time.Clock()
        self.font =      pygame.font.Font('./fonts/Pixeltype.ttf', 35)
        self.smallFont = pygame.font.Font('./fonts/Pixeltype.ttf', 20)
        self.formationImgs = [0] * 6
        for i in range(6):
            self.formationImgs[i] = pygame.image.load(f'./images/formation{i}.png')
        self.formations = [0] * 6
        self.formations[0] = [[1, 1, 0],
                              [0, 0, 1],
                              [1, 1, 0]]
        self.formations[1] = [[0, 1, 1],
                              [1, 0, 0],
                              [0, 1, 1]]
        self.formations[2] = [[0, 1, 0],
                              [1, 1, 1],
                              [0, 1, 0]]
        self.formations[3] = [[1, 0, 1],
                              [0, 1, 0],
                              [1, 0, 1]]
        self.formations[4] = [[0, 0, 1],
                              [1, 1, 1],
                              [0, 0, 1]]
        self.formations[5] = [[1, 0, 0],
                              [1, 1, 1],
                              [1, 0, 0]]
        self.slotCoords = [[(125, 125), (125, 225), (125, 325)],
                           [(225, 125), (225, 225), (225, 325)],
                           [(325, 125), (325, 225), (325, 325)]]
        self.characters = [0] * 8
        self.characters[0] = pygame.image.load('./images/bandit.png')
        self.characters[1] = pygame.image.load('./images/banditBoss.png')
        self.characters[2] = pygame.image.load('./images/monke.png')
        self.characters[3] = pygame.image.load('./images/gorilla.png')
        self.characters[4] = pygame.image.load('./images/playerDef.png')
        self.characters[5] = pygame.image.load('./images/playerHealer.png')
        self.characters[6] = pygame.image.load('./images/playerMelee.png')
        self.characters[7] = pygame.image.load('./images/playerRange.png')
        self.characterDead = pygame.image.load('./images/characterDead.png')
        self.characterNames = ['Bandit', 'Bandit Boss', 'Monkey', 'Gorilla', 'Tank', 'Healer', 'Melee', 'Ranger']
        self.textColor = 'forestgreen'
        self.buttonBgColor = 'grey25'
        self.lockedColor = 'grey10'
        self.gameState = 'Menu'
        self.formation = 0
        self.teamTextsNum = 0
        self.completedStages = 0
        self.unequipBtnBool = False
        self.playerTeam = [[2, 4, 9],
                           [9, 9, 0],
                           [6, 5, 9]]
        self.inventory = [4, 4, 5, 5, 6, 6, 7, 7]
        self.invBtns = [0] * 8
        self.inTeam = [True, False, True, False, True, True, True, False]
        #              atk, hp, def%, crit%, critDmg%, speed
        self.stats = [[10, 100,  0,  10, 50, 3],
                      [20, 200, 10, 20, 50, 2],
                      [30, 200, 10, 10, 50, 5],
                      [40, 300, 20, 20, 50, 1],
                      [5,  200, 15, 10, 50, 1],
                      [10, 100,  0,  10, 50, 2],
                      [15, 100,  7,  10, 40, 3],
                      [10, 60,  0,  40, 90, 4]]
        self.clickedSlot = len(self.inventory)
        self.stageTxt = [0] * 6
        self.stageLayouts = [0] * 6
        self.stageLayouts[0] = [[9, 0, 9],
                                [0, 0, 0],
                                [9, 0, 9]]
        self.stageLayouts[1] = [[9, 0, 0],
                                [1, 9, 9],
                                [9, 0, 0]]
        self.stageLayouts[2] = [[1, 0, 9],
                                [9, 9, 1],
                                [1, 0, 9]]
        self.stageLayouts[3] = [[9, 2, 9],
                                [2, 2, 2],
                                [9, 2, 9]]
        self.stageLayouts[4] = [[9, 2, 2],
                                [3, 9, 9],
                                [9, 2, 2]]
        self.stageLayouts[5] = [[3, 2, 9],
                                [9, 9, 3],
                                [3, 2, 9]]
        self.stageBuff = 0
        
        self.characterMovesTxt = [['attacks closest enemy with 100% dmg',# bandit
                                   'attacks closest enemy with 100% dmg',
                                   'attacks closest enemy with 100% dmg',
                                   'attacks all enemies with 200% dmg'],
                                  ['attacks closest enemy with 100% dmg',# bandit boss
                                   'attacks 3 random enemies with 100% dmg',
                                   'attacks 3 random enemies with 100% dmg',
                                   'attacks closest enemy with 300% dmg'],
                                  ['attacks closest enemy with 100% dmg',# monke
                                   'attacks 2 furthest enemies with 150% dmg',
                                   'attacks 2 furthest enemies with 150% dmg',
                                   'attacks closest enemy with 400% dmg'],
                                  ['attacks closest enemy with 100% dmg',# gorilla
                                   'attacks 2 closest enemies with 150% dmg',
                                   'attacks 2 closest enemies with 150% dmg',
                                   'attacks all enemy with 300% dmg'],
                                  ['attacks closest enemy with 100% dmg',# tank
                                   'attacks closest enemy with 100% dmg',
                                   'attacks closest enemy with 100% dmg',
                                   'attacks closest 3 enemies with 200% dmg'],
                                  ['attacks closest enemy with 100% dmg',# healer
                                   'heals lowest health ally with 200% dmg',
                                   'heals lowest health ally with 200% dmg',
                                   'heals 3 lowest health allies with 400% dmg'],
                                  ['attacks closest enemy with 100% dmg',# melee
                                   'attacks closest enemy with 100% dmg',
                                   'attacks 3 closest enemies with 200% dmg',
                                   'attacks all enemy with 300% dmg'],
                                  ['attacks closest enemy with 100% dmg',# ranger
                                   'attacks 2 furthest enemies with 150% dmg',
                                   'attacks 2 random enemies with 150% dmg',
                                   'attacks 4 furthest enemies with 200% dmg']]
        
        self.characterMoves = [[['front',  1, 100],# bandit
                                ['front',  1, 100],
                                ['front',  1, 100],
                                ['all',    9, 200]],
                               [['front',  1, 100],# bandit boss
                                ['random', 3, 100],
                                ['random', 3, 100],
                                ['front',  1, 300]],
                               [['front',  1, 100],# monke
                                ['back',   2, 150],
                                ['back',   2, 150],
                                ['front',  1, 400]],
                               [['front',  1, 100],# gorilla
                                ['front',  2, 150],
                                ['front',  2, 150],
                                ['all',    9, 300]],
                               [['front',  1, 100],# tank
                                ['front',  1, 100],
                                ['front',  1, 100],
                                ['front',  3, 200]],
                               [['front',  1, 100],# healer
                                ['heal',   1, 200],
                                ['heal',   1, 200],
                                ['heal',   3, 400]],
                               [['front',  1, 100],# melee
                                ['front',  1, 100],
                                ['front',  3, 200],
                                ['all',    9, 300]],
                               [['front',  1, 100],# ranger
                                ['back',   2, 150],
                                ['random', 2, 150],
                                ['back',   4, 200]]]
        self.delay = 2000 # ms
        self.moveNum = 0
        self.playerHpTxt = [[0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]]
        self.enemyHpTxt = [[0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]]
        self.roundNum = 0
        self.playerHealthOffset = [[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]]
        self.enemyHealthOffset =  [[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]]
        self.playMoveInstantly = True
        self.fightLog = []
        self.logSlot = 0
        self.slotReduction = 0
        
        self.BtnBgColorBox = pygame.Surface((135, 45))
        self.BtnBgColorBox.fill(self.buttonBgColor)
        
        # create menu screen
        self.fightTxt = self.font.render('Fight', False, self.textColor)
        self.fightBtn = pygame.Rect(50, 50, 135, 45)
        
        self.trainTxt = self.font.render('Train', False, self.textColor)
        self.trainBtn = pygame.Rect(50, 150, 135, 45)
        
        self.teamTxt = self.font.render('Team', False, self.textColor)
        self.teamBtn = pygame.Rect(50, 250, 135, 45)
        
        # create fights screen
        self.showLockedStages()
        self.stageBtns = [0] * 6
        self.stageBtns[0] = pygame.Rect(50, 50, 135, 45)
        self.stageBtns[1] = pygame.Rect(50, 100, 135, 45)
        self.stageBtns[2] = pygame.Rect(50, 170, 135, 45)
        self.stageBtns[3] = pygame.Rect(250, 30, 135, 45)
        self.stageBtns[4] = pygame.Rect(250, 100, 135, 45)
        self.stageBtns[5] = pygame.Rect(250, 170, 135, 45)
        
        self.backTxt = self.font.render('Back', False, self.textColor)
        self.backBtn1 = pygame.Rect(250, 260, 135, 45)
        
        # create team screen
        self.formationBtn = pygame.Rect(225, 20, 50, 50)
        self.backBtn2 = pygame.Rect(350, 740, 135, 45)
        
        self.usableSlot = pygame.Surface((50, 50))
        self.usableSlot.fill(self.buttonBgColor)
        self.lockedSlot = pygame.Surface((50, 50))
        self.lockedSlot.fill(self.lockedColor)
        self.activeSlot = pygame.Surface((50, 50))
        self.activeSlot.fill(self.textColor)
        
        self.formationBtns = [[0, 0, 0],
                              [0, 0, 0],
                              [0, 0, 0]]
        for x in range(3):
            for y in range(3):
                self.formationBtns[x][y] = pygame.Rect(self.slotCoords[y][x][0], self.slotCoords[y][x][1], 50, 50)
        self.screenSplit = pygame.Surface((1, 800))
        self.screenSplit.fill(self.buttonBgColor)
        
        self.teamTexts = [0, 0]
        self.teamTexts[0] = self.font.render('Choose formation', False, self.textColor)
        self.teamTexts[1] = self.font.render('Character stats', False, self.textColor)
        
        self.infoText = self.font.render('click slot to equip', False, self.textColor)
        
        self.dmgStatText   = self.font.render('Damage:', False, self.textColor)
        self.hpStatText    = self.font.render('Health:', False, self.textColor)
        self.defStatText   = self.font.render('Defence:', False, self.textColor)
        self.critCStatText = self.font.render('Crit Chance:', False, self.textColor)
        self.critDStatText = self.font.render('Crit Damage:', False, self.textColor)
        self.speedStatText = self.font.render('Speed:', False, self.textColor)
        
        self.chooseFormation = [0] * 6
        self.chooseFormation[0] = pygame.Rect(630, 150, 50, 50)
        self.chooseFormation[1] = pygame.Rect(730, 150, 50, 50)
        self.chooseFormation[2] = pygame.Rect(830, 150, 50, 50)
        self.chooseFormation[3] = pygame.Rect(630, 250, 50, 50)
        self.chooseFormation[4] = pygame.Rect(730, 250, 50, 50)
        self.chooseFormation[5] = pygame.Rect(830, 250, 50, 50)
        
        self.moveInfoTxt = [0] * 4
        self.moveInfoTxt[0] = self.font.render('Move 1: ', False, self.textColor)
        self.moveInfoTxt[1] = self.font.render('Move 2: ', False, self.textColor)
        self.moveInfoTxt[2] = self.font.render('Move 3: ', False, self.textColor)
        self.moveInfoTxt[3] = self.font.render('Move 4: ', False, self.textColor)
        
        self.moveDescTxt = [0] * 4
        self.moveDescTxt[0] = self.font.render('Test', False, self.textColor)
        self.moveDescTxt[1] = self.font.render('Test', False, self.textColor)
        self.moveDescTxt[2] = self.font.render('Test', False, self.textColor)
        self.moveDescTxt[3] = self.font.render('Test', False, self.textColor)
        
        self.unequipTxt = self.font.render('Unequip', False, self.textColor)
        self.unequipBtn = pygame.Rect(515, 740, 135, 45)
        
        self.closeTxt = self.font.render('Close', False, self.textColor)
        self.closeBtn = pygame.Rect(850, 740, 135, 45)

        # create train screen
        self.magicalTreeImg = pygame.image.load('./images/magicalTree.png')
        self.trainInfoTxt = self.font.render('Train random character under the magical tree', False, self.textColor)
        self.trainBtn2 = pygame.Rect(180, 450, 135, 45)
        self.characterTrainedTxt = self.font.render('', False, self.textColor)
        self.backBtn3 = pygame.Rect(350, 590, 135, 45)
        
        # create stages screen
        self.fightLogBg = pygame.Surface((650, 290))
        self.fightLogBg.fill(self.lockedColor)
        
        self.playerHealthBars =   [[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]]
        self.playerHealthBarsBg = [[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]]
        self.playerHealthFiller = [[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]]
        self.enemyHealthBars =    [[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]]
        self.enemyHealthBarsBg =  [[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]]
        self.enemyHealthFiller =  [[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]]
        for x in range(3):
            for y in range(3):
                self.playerHealthBars[x][y] = pygame.Surface((50, 10))
                self.playerHealthBars[x][y].fill('red')
                self.playerHealthBarsBg[x][y] = pygame.Surface((50, 10))
                self.playerHealthBarsBg[x][y].fill(self.lockedColor)
                self.playerHealthFiller[x][y] = pygame.Surface((50, 10))
                self.playerHealthFiller[x][y].fill('black')
                
                self.enemyHealthBars[x][y] = pygame.Surface((50, 10))
                self.enemyHealthBars[x][y].fill('red')
                self.enemyHealthBarsBg[x][y] = pygame.Surface((50, 10))
                self.enemyHealthBarsBg[x][y].fill(self.lockedColor)
                self.enemyHealthFiller[x][y] = pygame.Surface((50, 10))
                self.enemyHealthFiller[x][y].fill('black')
        
        self.fightLogTxt = [0] * 6
        self.fightLogTxt[0] = self.font.render('Log 1', False, self.textColor)
        self.fightLogTxt[1] = self.font.render('Log 2', False, self.textColor)
        self.fightLogTxt[2] = self.font.render('Log 3', False, self.textColor)
        self.fightLogTxt[3] = self.font.render('Log 4', False, self.textColor)
        self.fightLogTxt[4] = self.font.render('Log 5', False, self.textColor)
        self.fightLogTxt[5] = self.font.render('Log 6', False, self.textColor)
        
        self.abandonTxt = self.font.render('Abandon', False, self.textColor)
        self.abandonBtn = pygame.Rect(650, 740, 135, 45)
        
        # run game loop
        self.screen = pygame.display.set_mode((235, 350))
        self.startGame()

if __name__ == "__main__":
    app = App()