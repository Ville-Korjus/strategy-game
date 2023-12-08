import pygame
import random
import time
from sys import exit

class App:
    def updateEnemyHealth(self, enemy, dmg):
        self.enemies[enemy][5] -= dmg
        self.enemyHealths[enemy] = pygame.Surface((self.enemies[enemy][5] / self.enemies[enemy][6] * 50, 4))
        self.enemyHealths[enemy].fill('red')
    
    def moveBullets(self):
        for bullet in range(self.bullets):
            self.bulletCoords[bullet][0] += self.bulletMovements[bullet][0]
            self.bulletCoords[bullet][1] += self.bulletMovements[bullet][1]
            self.bulletRects[bullet] = pygame.Rect(495 + self.bulletCoords[bullet][0], 470 + self.bulletCoords[bullet][1], 30, 30)
    
    def calculateBulletMovement(self):
        print(self.bulletDestinations)
        endX, endY = self.bulletDestinations[len(self.bulletDestinations) - 1]
        startX = 495
        startY = 470
        if startX < endX: # left
            if startY < endY: # up
                if endX - startX > endY - startY: # more left than up
                    y = (endY - startY) / (endX - startX) * self.bulletSpeed
                    x = (1 - (endY - startY) / (endX - startX)) * self.bulletSpeed
                elif endX - startX < endY - startY: # more up than left
                    y = (1 - (endX - startX) / (endY - startY)) * self.bulletSpeed
                    x = (endX - startX) / (endY - startY) * self.bulletSpeed
            elif startY > endY: # down
                if endX - startX > ((endY - startY) * -1): # more left than down
                    y = (endY - startY) / (endX - startX) * self.bulletSpeed
                    x = (1 - (endY - startY) / (endX - startX)) * self.bulletSpeed
                elif endX - startX < ((endY - startY) * -1): # more down than left
                    y = (1 - (endX - startX) / (endY - startY)) * self.bulletSpeed
                    x = (endX - startX) / (endY - startY) * self.bulletSpeed
            else: # left
                x = self.bulletSpeed
        elif startX > endX: # right
            if startY < endY: # up
                if ((endX - startX) * -1) > endY - startY: # more right than up
                    y = (endY - startY) / (endX - startX) * self.bulletSpeed
                    x = (1 - (endY - startY) / (endX - startX)) * self.bulletSpeed
                elif ((endX - startX) * -1) < endY - startY: # more up than right
                    y = (1 - (endX - startX) / (endY - startY)) * self.bulletSpeed
                    x = (endX - startX) / (endY - startY) * self.bulletSpeed
            elif startY > endY: # down
                if ((endX - startX) * -1) > ((endY - startY) * -1): # more right than down
                    y = (endY - startY) / (endX - startX) * self.bulletSpeed
                    x = (1 - (endY - startY) / (endX - startX)) * self.bulletSpeed
                elif ((endX - startX) * -1) < ((endY - startY) * -1): # more down than right
                    y = (1 - (endX - startX) / (endY - startY)) * self.bulletSpeed
                    x = (endX - startX) / (endY - startY) * self.bulletSpeed
            else: # right
                x = self.bulletSpeed
        elif startY < endY: # up
            y = self.bulletSpeed
        elif startY > endY: # down
            y = self.bulletSpeed
        self.bulletMovements.append((x, y))
    
    def checkClosestEnemy(self):
        closestEnemyNum = 99999
        bestCoords = (0, 0)
        for enemy in self.enemies:
            enemyX = self.enemySpawns[enemy[1]][0] + self.x - enemy[2]
            enemyY = self.enemySpawns[enemy[1]][1] + self.y - enemy[3]
            # top left
            if enemyX > 475 and enemyY > 450:
                if closestEnemyNum > (enemyX - 475) + (enemyY - 450):
                    closestEnemyNum = (enemyX - 475) + (enemyY - 450)
                    bestCoords = (enemyX, enemyY)
            # top right
            elif enemyX < 475 and enemyY > 450:
                if closestEnemyNum > (enemyX * -1 + 475) + (enemyY - 450):
                    closestEnemyNum = (enemyX * -1 + 475) + (enemyY - 450)
                    bestCoords = (enemyX, enemyY)
            # bottom left
            elif enemyX > 475 and enemyY < 450:
                if closestEnemyNum > (enemyX - 475) + (enemyY * -1 + 450):
                    closestEnemyNum = (enemyX - 475) + (enemyY * -1 + 450)
                    bestCoords = (enemyX, enemyY)
            # bottom right
            elif enemyX < 475 and enemyY < 450:
                if closestEnemyNum > (enemyX * -1 + 475) + (enemyY * -1 + 450):
                    closestEnemyNum = (enemyX * -1 + 475) + (enemyY * -1 + 450)
                    bestCoords = (enemyX, enemyY)
            # left
            elif enemyX > 475:
                if closestEnemyNum > enemyX - 475:
                    closestEnemyNum = enemyX - 475
                    bestCoords = (enemyX, enemyY)
            # right
            elif enemyX < 475:
                if closestEnemyNum > enemyX * -1 - 475:
                    closestEnemyNum = enemyX * -1 - 475
                    bestCoords = (enemyX, enemyY)
            # top
            elif enemyY > 450:
                if closestEnemyNum > enemyY - 450:
                    closestEnemyNum = enemyY - 450
                    bestCoords = (enemyX, enemyY)
            # bottom
            elif enemyY < 450:
                if closestEnemyNum > enemyY * -1 - 450:
                    closestEnemyNum = enemyY * -1 - 450
                    bestCoords = (enemyX, enemyY)
        return bestCoords
    
    def menuButton(self):
        self.screen = pygame.display.set_mode((235, 370))
        self.gameState = 'Menu'
        self.x = -100
        self.y = -100
        self.wKeyEvent = False
        self.aKeyEvent = False
        self.sKeyEvent = False
        self.dKeyEvent = False
        self.playerHp = self.playerMaxHp
        self.updateHealth()
        self.enemies = []
        self.enemyHealths = []
        self.enemyRects = []
        self.bulletCoords = []
        self.bulletDestinations = []
        self.bulletMovements = []
        self.bulletRects = []
        self.bullets = 0
        for ability in self.ownedAbilities:
            self.abilityCds[ability] = self.abilityMaxCds[ability]
            self.abilityCdsBool[ability] = False
        self.enemiesLeft = self.enemyNum
            
    def updateXp(self):
        self.playerXpColorBox = pygame.Surface((self.xp / self.maxXp * 400, 20))
        self.playerXpColorBox.fill('red')
        self.playerXpTxt = self.font.render(f'experience        {self.xp} / {self.maxXp}', False, 'white')
    
    def updateHealth(self):
        self.playerHpTxt = self.font.render(f'health                      {self.playerHp} / {self.playerMaxHp}', False, 'white')
        self.playerHpColorBox = pygame.Surface((self.playerHp / self.playerMaxHp * 400, 20))
        self.playerHpColorBox.fill('red')
        
    def spawnEnemy(self):
        # spawn enemies
        if self.enemiesLeft != 0 and self.gameState == 'Grind':
            if self.spawnTime + self.spawnDelay <= round(time.time() * 1000):
                self.spawnTime += self.spawnDelay
                randomSpawn = random.randint(0, 11)
                randomEnemy = random.randint(1, 100)
                print('spawn enemy')
                if randomEnemy >= 1 and randomEnemy <= 60:      # 60%                                dmg hp maxHp
                    self.enemies.append([self.enemyImgs[0], randomSpawn, self.x + 100, self.y + 100, 5, 10, 10])
                elif randomEnemy >= 61 and randomEnemy <= 85:   # 25%
                    self.enemies.append([self.enemyImgs[1], randomSpawn, self.x + 100, self.y + 100, 10, 20, 20])
                elif randomEnemy >= 86 and randomEnemy <= 95:   # 10%
                    self.enemies.append([self.enemyImgs[2], randomSpawn, self.x + 100, self.y + 100, 15, 30, 30])
                elif randomEnemy >= 96 and randomEnemy <= 100:  # 5%
                    self.enemies.append([self.enemyImgs[3], randomSpawn, self.x + 100, self.y + 100, 20, 70, 70])
                self.enemyRects.append(pygame.Rect(self.enemySpawns[randomSpawn][0] + self.x - self.x + 100, self.enemySpawns[randomSpawn][1] + self.y - self.y + 100, 30, 30))
                self.enemyHealths.append(pygame.Surface((50, 4)))
                self.enemyHealths[len(self.enemyHealths) - 1].fill('red')
                self.enemiesLeft -= 1
        
    def moveEnemies(self):
        # enemy move towards player
        if self.gameState == 'Grind':
            if self.enemyMovementTime + self.enemyWalkDelay <= round(time.time() * 1000):
                self.enemyMovementTime += self.enemyWalkDelay
                count = 0
                for enemy in self.enemies:
                    enemyX = self.enemySpawns[enemy[1]][0] + self.x - enemy[2]
                    enemyY = self.enemySpawns[enemy[1]][1] + self.y - enemy[3]
                    if 475 < enemyX: # left
                        if 450 < enemyY: # up
                            if enemyX - 475 > enemyY - 450: # more left than up
                                enemy[3] += (enemyY - 450) / (enemyX - 475) * self.enemySpeed
                                enemy[2] += (1 - (enemyY - 450) / (enemyX - 475)) * self.enemySpeed
                            elif enemyX - 475 < enemyY - 450: # more up than left
                                enemy[3] += (1 - (enemyX - 475) / (enemyY - 450)) * self.enemySpeed
                                enemy[2] += (enemyX - 475) / (enemyY - 450) * self.enemySpeed
                        elif 450 > enemyY: # down
                            if enemyX - 475 > ((enemyY - 450) * -1): # more left than down
                                enemy[3] -= ((enemyY - 450) * -1) / (enemyX - 475) * self.enemySpeed
                                enemy[2] += (1 - ((enemyY - 450) * -1) / (enemyX - 475)) * self.enemySpeed
                            elif enemyX - 475 < ((enemyY - 450) * -1): # more down than left
                                enemy[3] -= (1 - (enemyX - 475) / ((enemyY - 450) * -1)) * self.enemySpeed
                                enemy[2] += (enemyX - 475) / ((enemyY - 450) * -1) * self.enemySpeed
                        else:
                            enemy[2] += self.enemySpeed
                    elif 475 > enemyX: # right
                        if 450 < enemyY: # up
                            if ((enemyX - 475) * -1) > enemyY - 450: # more right than up
                                enemy[3] += (enemyY - 450) / ((enemyX - 475) * -1) * self.enemySpeed
                                enemy[2] -= (1 - (enemyY - 450) / ((enemyX - 475) * -1)) * self.enemySpeed
                            elif ((enemyX - 475) * -1) < enemyY - 450: # more up than right
                                enemy[3] += (1 - ((enemyX - 475) * -1) / (enemyY - 450)) * self.enemySpeed
                                enemy[2] -= ((enemyX - 475) * -1) / (enemyY - 450) * self.enemySpeed
                        elif 450 > enemyY: # down
                            if ((enemyX - 475) * -1) > ((enemyY - 450) * -1): # more right than down
                                enemy[3] -= ((enemyY - 450) * -1) / ((enemyX - 475) * -1) * self.enemySpeed
                                enemy[2] -= (1 - ((enemyY - 450) * -1) / ((enemyX - 475) * -1)) * self.enemySpeed
                            elif ((enemyX - 475) * -1) < ((enemyY - 450) * -1): # more down than right
                                enemy[3] -= (1 - ((enemyX - 475) * -1) / ((enemyY - 450) * -1)) * self.enemySpeed
                                enemy[2] -= ((enemyX - 475) * -1) / ((enemyY - 450) * -1) * self.enemySpeed
                        else:
                            enemy[2] -= self.enemySpeed
                    elif 450 < enemyY: # up
                        enemy[3] += self.enemySpeed
                    elif 450 > enemyY: # down
                        enemy[3] -= self.enemySpeed
                    
                    self.enemyRects[count] = pygame.Rect(enemyX, enemyY, 30, 30)
                    count += 1
                    
    
    def resetGrass(self):
        for y in range(12):
            for x in range(12):
                if self.grassTileNums[x][y] == 3:
                    randNum = random.randint(0, 2)
                    self.grassTileNums[x][y] = randNum
                self.grassTiles[x][y] = self.grassImgs[self.grassTileNums[x][y]]
    
    def walkCycle(self):
        if self.walkCycleNum == 0:
            self.walkCycleOutput = 1
        elif self.walkCycleNum == 1:
            self.walkCycleOutput = 0
        elif self.walkCycleNum == 2:
            self.walkCycleOutput = 2
        elif self.walkCycleNum == 3:
            self.walkCycleOutput = 0
            
        if self.walkCycleNum != 3:
            self.walkCycleNum += 1
        else:
            self.walkCycleNum = 0
            
    def startGame(self):
        while True:
            # events
            for event in pygame.event.get():
                # close game event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # click events
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Menu screen
                    if self.gameState == 'Menu':
                        # grind button
                        if self.grindBtn.collidepoint(event.pos):
                            self.screen = pygame.display.set_mode((1000, 950))
                            self.gameState = 'Grind'
                        # save button
                        elif self.saveBtn.collidepoint(event.pos):
                            print('save')
                        # load button
                        elif self.loadBtn.collidepoint(event.pos):
                            print('load')
                        # info button
                        elif self.infoBtn.collidepoint(event.pos):
                            self.screen = pygame.display.set_mode((1000, 950))
                            self.gameState = 'Info'
                    # Grind screen
                    elif self.gameState == 'Grind':
                        # menu button
                        if self.menuBtn.collidepoint(event.pos):
                            self.menuButton()
                        # ability buttons
                        for btn in range(len(self.abilityCds)):
                            if self.abilityBtns[btn].collidepoint(event.pos) and self.playerHp != 0 and self.abilityCdsBool[btn]:
                                print(f'pressed ability {btn}')
                    # Info screen
                    elif self.gameState == 'Info':
                        # menu button
                        if self.menuBtn.collidepoint(event.pos):
                            self.menuButton()
                # keyboard down events
                elif event.type == pygame.KEYDOWN:
                    # Grind screen
                    if self.gameState == 'Grind':
                        # w button
                        if event.key == pygame.K_w and self.playerHp != 0:
                            self.wKeyEvent = True
                        # a button
                        if event.key == pygame.K_a and self.playerHp != 0:
                            self.aKeyEvent = True
                        # s button
                        if event.key == pygame.K_s and self.playerHp != 0:
                            self.sKeyEvent = True
                        # d button
                        if event.key == pygame.K_d and self.playerHp != 0:
                            self.dKeyEvent = True
                # keyboard up events
                elif event.type == pygame.KEYUP:
                    # Grind screen
                    if self.gameState == 'Grind':
                        # w button
                        if event.key == pygame.K_w:
                            self.wKeyEvent = False
                        # a button
                        if event.key == pygame.K_a:
                            self.aKeyEvent = False
                        # s button
                        if event.key == pygame.K_s:
                            self.sKeyEvent = False
                        # d button
                        if event.key == pygame.K_d:
                            self.dKeyEvent = False
                            
            # if any of movement keys is pressed turn on walk animation
            if self.wKeyEvent == True or self.aKeyEvent == True or self.sKeyEvent == True or self.dKeyEvent == True:
                self.walkCycleBool = True
            else:
                self.walkCycleBool = False
                self.walkCycleOutput = 0
                            
            # movement key events
            if self.wKeyEvent == True:
                self.y += self.speed
                self.playerState = 0
            if self.aKeyEvent == True:
                self.x += self.speed
                self.playerState = 3
            if self.sKeyEvent == True:
                self.y += -self.speed
                self.playerState = 0
            if self.dKeyEvent == True:
                self.x += -self.speed
                self.playerState = 3
                
            # check if you moved 100 pixels in any direction then move tiles
            # left
            if self.x >= self.xFromMid + 100:
                self.xFromMid += 100
                for y in range(12):
                    for x in reversed(range(12)):
                        if x == 0:
                            self.grassTileNums[x][y] = 3
                        else:
                            self.grassTileNums[x][y] = self.grassTileNums[x - 1][y]
                self.resetGrass()
            # right
            elif self.x <= self.xFromMid - 100:
                self.xFromMid -= 100
                for y in range(12):
                    for x in range(12):
                        if x == 11:
                            self.grassTileNums[x][y] = 3
                        else:
                            self.grassTileNums[x][y] = self.grassTileNums[x + 1][y]
                self.resetGrass()
            # up
            if self.y >= self.yFromMid + 100:
                self.yFromMid += 100
                for y in reversed(range(12)):
                    for x in range(12):
                        if y == 0:
                            self.grassTileNums[x][y] = 3
                        else:
                            self.grassTileNums[x][y] = self.grassTileNums[x][y - 1]
                self.resetGrass()
            # down
            elif self.y <= self.yFromMid - 100:
                self.yFromMid -= 100
                for y in range(12):
                    for x in range(12):
                        if y == 11:
                            self.grassTileNums[x][y] = 3
                        else:
                            self.grassTileNums[x][y] = self.grassTileNums[x][y + 1]
                self.resetGrass()
                
            # if moving in an intercardinal direction change character direction accordingly
            if self.wKeyEvent == True and self.aKeyEvent == True or self.dKeyEvent == True and self.sKeyEvent == True:
                self.playerState = 6
            elif self.wKeyEvent == True and self.dKeyEvent == True or self.aKeyEvent == True and self.sKeyEvent == True:
                self.playerState = 9
                
            # run walkCycle every time self.delay ms have passed
            if self.walkCycleBool:
                if self.enemyTime + self.walkDelay <= round(time.time() * 1000):
                    self.enemyTime = round(time.time() * 1000)
                    self.walkCycle()
                    
            self.spawnEnemy()
            self.moveEnemies()
            
            # update health
            count = 0
            for enemy in self.enemies:
                if self.playerRect.colliderect(self.enemyRects[count]):
                    if self.iFrameTime + self.iFrames <= round(time.time() * 1000):
                        self.iFrameTime = round(time.time() * 1000)
                        if self.playerHp <= enemy[4]:
                            self.playerHp = 0
                            self.wKeyEvent = False
                            self.aKeyEvent = False
                            self.sKeyEvent = False
                            self.dKeyEvent = False
                        else:
                            self.playerHp -= enemy[4]
                        self.updateHealth()
                count += 1
                
            # update ability timers every 100 ms
            if self.gameState == 'Grind':
                if self.updateAbilities + 100 <= round(time.time() * 1000):
                    self.updateAbilities += 100
                    for ability in self.ownedAbilities:
                        if self.abilityCds[ability] != 0:
                            self.abilityCds[ability] -= .1
                            if self.abilityCds[ability] < 0:
                                self.abilityCds[ability] = 0
                            self.abilityCdsTxt[ability] = self.font.render(f'{round(self.abilityCds[ability], 1)}s', False, 'red')
                        else:
                            self.abilityCdsBool[ability] = True
                            
            # check when to shoot bullet
            if self.gameState == 'Grind' and self.enemies != [] and self.playerHp != 0:
                if self.bulletCreateTime + self.bulletCd <= round(time.time() * 1000):
                    self.bulletCreateTime = round(time.time() * 1000)
                    self.bullets += 1
                    self.bulletRects.append(pygame.Rect(495, 470, 30, 30))
                    self.bulletCoords.append([0, 0])
                    self.bulletDestinations.append(self.checkClosestEnemy())
                    self.calculateBulletMovement()
                    
            # move bullets
            if self.gameState == 'Grind' and self.bullets != 0:
                if self.bulletMoveTime + self.bulletDelay <= round(time.time() * 1000):
                    self.bulletMoveTime = round(time.time() * 1000)
                    self.moveBullets()
                    
            # check if bullets hit
            if self.gameState == 'Grind' and self.bullets != 0:
                for bullet in range(self.bullets):
                    for enemy in range(len(self.enemyHealths)):
                        if self.enemyRects[enemy].colliderect(self.bulletRects[bullet]):
                            self.bullets -= 1
                            self.bulletCoords.pop(bullet)
                            self.bulletDestinations.pop(bullet)
                            self.bulletMovements.pop(bullet)
                            self.bulletRects.pop(bullet)
                            self.updateEnemyHealth(enemy, 1)
                            break
                    else:
                        continue
                    break
                    
            self.screen.fill('black')
            # draw game
            if self.gameState == 'Menu':
                # grind button
                self.screen.blit(self.BtnBgColorBox, (50, 50))
                self.screen.blit(self.grindTxt, (50 + 40, 50 + 12))
                # save button
                self.screen.blit(self.BtnBgColorBox, (50, 125))
                self.screen.blit(self.saveTxt, (50 + 12, 125 + 12))
                # load button
                self.screen.blit(self.BtnBgColorBox, (50, 200))
                self.screen.blit(self.loadTxt, (50 + 12, 200 + 12))
                # info button
                self.screen.blit(self.BtnBgColorBox, (50, 275))
                self.screen.blit(self.infoTxt, (50 + 40, 275 + 12))
            elif self.gameState == 'Grind':
                count = 0
                xOffset = 0
                yOffset = 0
                # grass
                for y in range(12):
                    for x in range(12):
                        self.screen.blit(self.grassTiles[x][y], (0 + xOffset + self.x - self.xFromMid - 100, 0 + yOffset + self.y - self.yFromMid - 100))
                        count += 1
                        xOffset += 100
                    yOffset += 100
                    xOffset = 0
                # enemies and their health bars
                count = 0
                for enemy in self.enemies:
                    self.screen.blit(enemy[0], (self.enemySpawns[enemy[1]][0] + self.x - enemy[2], self.enemySpawns[enemy[1]][1] + self.y - enemy[3]))
                    self.screen.blit(self.enemyBarBg, (self.enemySpawns[enemy[1]][0] + self.x - enemy[2] - 1, self.enemySpawns[enemy[1]][1] + self.y - enemy[3] - 1))
                    self.screen.blit(self.enemyHealths[count], (self.enemySpawns[enemy[1]][0] + self.x - enemy[2], self.enemySpawns[enemy[1]][1] + self.y - enemy[3]))
                    count += 1
                # top text
                self.screen.blit(self.enemiesLeftTxt, (455, 40))
                self.screen.blit(self.waveNumTxt, (450, 10))
                # player
                self.screen.blit(self.playerImgs[self.playerState + self.walkCycleOutput], (475, 450))
                # player hp, xp bars and level
                self.screen.blit(self.playerBarBg, (10, 920))
                self.screen.blit(self.playerHpColorBox, (13, 923))
                self.screen.blit(self.playerHpTxt, (20, 924))
                self.screen.blit(self.playerBarBg, (10, 889))
                self.screen.blit(self.playerXpColorBox, (13, 892))
                self.screen.blit(self.playerXpTxt, (20, 893))
                self.screen.blit(self.playerLevelTxt, (160, 860))
                # bullets
                for bullet in range(self.bullets):
                    self.screen.blit(self.bulletImg, (495 + self.bulletCoords[bullet][0], 470 + self.bulletCoords[bullet][1]))
                # abilities
                count = 0
                for ability in self.ownedAbilities:
                    self.screen.blit(self.abilityColorBoxFrame, (430 + count - 3, 892 - 3))
                    if self.abilityCdsBool[ability] == False:
                        self.screen.blit(self.abilityColorBoxOff, (430 + count, 892))
                        self.screen.blit(self.abilityIcons[ability], (430 + count, 892))
                        self.screen.blit(self.abilityCdsTxt[ability], (440 + count, 907))
                    else:
                        self.screen.blit(self.abilityColorBoxOn, (430 + count, 892))
                        self.screen.blit(self.abilityIcons[ability], (430 + count, 892))
                    count += 100
                # menu button
                self.screen.blit(self.BtnBgColorBox, (850, 900))
                self.screen.blit(self.menuTxt, (850 + 40, 900 + 12))
                # loss text
                if self.playerHp == 0:
                    self.screen.blit(self.lossTxt, (250, 420))
            elif self.gameState == 'Info':
                # menu button
                self.screen.blit(self.BtnBgColorBox, (850, 900))
                self.screen.blit(self.menuTxt, (850 + 40, 900 + 12))
                        
            # update game 60fps
            pygame.display.update()
            self.clock.tick(60)
                
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.display.set_caption('Get OP Simulator')
        # set variables
        self.screen = pygame.display.set_mode((1000, 950))
        self.clock = pygame.time.Clock()
        self.megaFont =  pygame.font.Font('./fonts/Pixeltype.ttf', 200)
        self.bigFont =   pygame.font.Font('./fonts/Pixeltype.ttf', 50)
        self.font =      pygame.font.Font('./fonts/Pixeltype.ttf', 35)
        self.font2 =     pygame.font.Font('./fonts/Pixeltype.ttf', 37)
        self.smallFont = pygame.font.Font('./fonts/Pixeltype.ttf', 20)
        self.playerImgs = [0] * 12
        self.playerImgs[0] =  pygame.image.load('./images/characterUpStill.png')
        self.playerImgs[1] =  pygame.image.load('./images/characterUpMove1.png')
        self.playerImgs[2] =  pygame.image.load('./images/characterUpMove2.png')
        self.playerImgs[3] =  pygame.image.load('./images/characterLeftStill.png')
        self.playerImgs[4] =  pygame.image.load('./images/characterLeftMove1.png')
        self.playerImgs[5] =  pygame.image.load('./images/characterLeftMove2.png')
        self.playerImgs[6] =  pygame.image.load('./images/characterTopLeftStill.png')
        self.playerImgs[7] =  pygame.image.load('./images/characterTopLeftMove1.png')
        self.playerImgs[8] =  pygame.image.load('./images/characterTopLeftMove2.png')
        self.playerImgs[9] =  pygame.image.load('./images/characterTopRightStill.png')
        self.playerImgs[10] = pygame.image.load('./images/characterTopRightMove1.png')
        self.playerImgs[11] = pygame.image.load('./images/characterTopRightMove2.png')
        self.grassImgs = [0] * 3
        self.grassImgs[0] = pygame.image.load('./images/grass1.png')
        self.grassImgs[1] = pygame.image.load('./images/grass2.png')
        self.grassImgs[2] = pygame.image.load('./images/grass3.png')
        self.enemyImgs = [0] * 4
        self.enemyImgs[0] = pygame.image.load('./images/enemy1.png')
        self.enemyImgs[1] = pygame.image.load('./images/enemy2.png')
        self.enemyImgs[2] = pygame.image.load('./images/enemy3.png')
        self.enemyImgs[3] = pygame.image.load('./images/enemy4.png')
        self.bulletImg = pygame.image.load('./images/bullet.png')
        self.rocketImg = pygame.image.load('./images/rocket.png')
        self.abilityImgs =    [0] * 1
        self.abilityIcons =   [0] * 1
        self.abilityCds =     [0] * 1
        self.abilityMaxCds =  [0] * 1
        self.abilityCdsBool = [0] * 1
        self.abilityCdsTxt =  [0] * 1
        self.abilityBtns =    [0] * 1
        self.abilityImgs[0] = pygame.image.load('./images/bomb.png')
        self.abilityIcons[0] = pygame.image.load('./images/bigbomb.png')
        self.abilityCds[0] =    10 # s
        self.abilityMaxCds[0] = 10 # s
        self.abilityCdsBool[0] = False
        self.textColor = 'forestgreen'
        self.buttonBgColor = 'grey25'
        self.lockedColor = 'grey10'
        self.gameState = 'Menu'
        self.walkDelay =     200 # ms
        self.spawnDelay =   5000 # ms
        self.enemyWalkDelay = 10 # ms
        self.bulletDelay =    10 # ms
        self.iFrames =       500 # ms
        self.bulletCd =     1000 # ms
        self.rocketCd =     5000 # ms
        self.waveBuff = 0
        self.waveNum = 1
        self.x = -100
        self.y = -100
        self.playerState = 0
        self.wKeyEvent = False
        self.aKeyEvent = False
        self.sKeyEvent = False
        self.dKeyEvent = False
        self.speed = 2
        self.enemySpeed = 2
        self.walkCycleBool = False
        self.enemyTime =         round(time.time() * 1000)
        self.spawnTime =         round(time.time() * 1000)
        self.enemyMovementTime = round(time.time() * 1000)
        self.iFrameTime =        round(time.time() * 1000)
        self.updateAbilities =   round(time.time() * 1000)
        self.bulletCreateTime =  round(time.time() * 1000)
        self.bulletMoveTime =    round(time.time() * 1000)
        self.walkCycleOutput = 0
        self.walkCycleNum = 0
        self.xFromMid = -100
        self.yFromMid = -100
        self.enemyNum = 2
        self.enemiesLeft = self.enemyNum
        self.enemySpawns = [(0, 200), (0, 500), (0, 800), (1100, 200), (1100, 500), (1100, 800), (200, 0), (500, 0), (800, 0), (200, 1100), (500, 1100), (800, 1100)]
        self.enemies = []
        self.enemyHealths = []
        self.enemyRects = []
        self.bulletRects = []
        self.playerHp = 100
        self.playerMaxHp = 100
        self.ownedAbilities = [0]
        self.xp = 0
        self.maxXp = 100
        self.range = 5
        self.bullets = 0
        self.level = 1
        self.bulletCoords = []
        self.bulletDestinations = []
        self.bulletMovements = []
        self.bulletSpeed = 5
        
        self.BtnBgColorBox = pygame.Surface((135, 45)) # normal button bg
        self.BtnBgColorBox.fill(self.buttonBgColor)
        
        self.abilityColorBoxFrame = pygame.Surface((56, 56)) # ability button frame
        self.abilityColorBoxFrame.fill('black')
        self.abilityColorBoxOn = pygame.Surface((50, 50)) # on ability button bg
        self.abilityColorBoxOn.fill(self.buttonBgColor)
        self.abilityColorBoxOff = pygame.Surface((50, 50)) # off ability button bg
        self.abilityColorBoxOff.fill(self.lockedColor)
        
        self.playerRect = pygame.Rect(475, 450, 30, 30)
        
        '''--------------------------------create menu screen--------------------------------'''
        self.grindTxt = self.font.render('Grind', False, self.textColor)
        self.grindBtn = pygame.Rect(50, 50, 135, 45)
        
        self.saveTxt = self.font.render('Save game', False, self.textColor)
        self.saveBtn = pygame.Rect(50, 125, 135, 45)
        
        self.loadTxt = self.font.render('Load save', False, self.textColor)
        self.loadBtn = pygame.Rect(50, 200, 135, 45)
        
        self.infoTxt = self.font.render('Info', False, self.textColor)
        self.infoBtn = pygame.Rect(50, 275, 135, 45)
        
        '''-------------------------------create grind screen-------------------------------'''
        # grass tiles
        self.grassTiles =    [[0 for _ in range(12)] for _ in range(12)]
        self.grassTileNums = [[0 for _ in range(12)] for _ in range(12)]
        for y in range(12):
            for x in range(12):
                randNum = random.randint(0, 2)
                self.grassTiles[x][y] = self.grassImgs[randNum]
                self.grassTileNums[x][y] = randNum
                
        # top text
        self.waveNumTxt = self.bigFont.render(f'Wave: {self.waveNum}', False, 'black')
        self.enemiesLeftTxt = self.smallFont.render(f'Enemies left: {self.enemiesLeft}', False, 'black')
        
        # player bar background
        self.playerBarBg = pygame.Surface((406, 26))
        self.playerBarBg.fill('black')
        
        # player health
        self.playerHpColorBox = pygame.Surface((400, 20))
        self.playerHpColorBox.fill('red')
        self.playerHpTxt = self.font.render(f'health                      {self.playerHp} / {self.playerMaxHp}', False, 'white')
        
        # player xp
        self.playerXpColorBox = pygame.Surface((self.xp / self.maxXp * 400, 20))
        self.playerXpColorBox.fill('green')
        self.playerXpTxt = self.font.render(f'experience        {self.xp} / {self.maxXp}', False, 'white')
        self.playerLevelTxt = self.bigFont.render(f'Level {self.level}', False, 'black') # level
        
        # player abilities
        count = 0
        for ability in range(len(self.abilityCds)):
            self.abilityBtns[ability] = pygame.Rect(430 + count, 892, 50, 50)
            count += 100
        self.abilityCdsTxt[0] = self.font.render('10s', False, 'red')
        
        # enemy health background
        self.enemyBarBg = pygame.Surface((52, 6))
        self.enemyBarBg.fill('black')
        
        # menu button
        self.menuTxt = self.font.render('Menu', False, self.textColor)
        self.menuBtn = pygame.Rect(850, 900, 135, 45)
        
        # loss text
        self.lossTxt = self.megaFont.render('YOU DIED', False, 'red')
        
        # run game loop
        self.screen = pygame.display.set_mode((235, 370))
        self.startGame()

if __name__ == "__main__":
    app = App()
    
    
""" 
| TO NOT DO list
V
add emp ebility that stuns enemies
add auto shooting
add shop when you level up
add enemies dropping xp
add saving game
add loading saves

| Changes compared to last version
V

ADDED:
self.range
self.bulletMovements
self.bulletDestinations
self.bulletCoords
self.bullets
checkClosestEnemy()
menuButton()

REMOVED:

CHANGE:
FIX moveEnemies() to also go straight it 4 main directions if needed
compressed spawnEnemy() code
"""