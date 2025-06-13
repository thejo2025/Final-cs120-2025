# -*- coding: utf-8 -*-
"""
Created on Mon Jun 9 08:11:23 2025

@author: thejo
"""

import pygame, simpleGE, random

class Banana(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("banana.png")
        self.setSize(25, 25)
        self.minSpeed = 3
        self.maxSpeed = 8
        self.reset()

    def reset(self):
        # move to top of screen
        self.y = 10
        # x is random 0 - screen width
        self.x = random.randint(0, self.screenWidth)
        # dy is random minSpeed to maxSpeed
        self.dy = random.randint(self.minSpeed, self.maxSpeed)

    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()

class Snake(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("snake.png")
        self.setSize(25, 25)
        self.minSpeed = 3
        self.maxSpeed = 5
        self.reset()

    def reset(self):
        # move to top of screen
        self.y = 10
        # x is random 0 - screen width
        self.x = random.randint(0, self.screenWidth)
        # dy is random minSpeed to maxSpeed
        self.dy = random.randint(self.minSpeed, self.maxSpeed)

    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
    
class Coconut(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("coconut.png")
        self.setSize(25, 25)
        self.minSpeed = 3
        self.maxSpeed = 3
        self.reset()

    def reset(self):
        # move to top of screen
        self.y = 10
        # x is random 0 - screen width
        self.x = random.randint(0, self.screenWidth)
        # dy is random minSpeed to maxSpeed
        self.dy = random.randint(self.minSpeed, self.maxSpeed)

    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()

class Monkey(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("monkey.png")
        self.setSize(50, 50)
        self.position = (320, 400)
        self.moveSpeed = 6
        
    
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
            

class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)

class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left: 100"
        self.center = (551, 30)

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("jungle.jpg")
        self.sndBanana = simpleGE.Sound("banana.wav")
        self.sndCoconut = simpleGE.Sound("coconut.wav")
        self.sndSnake = simpleGE.Sound("snake.wav")
        self.numBananas = 10
        self.score = 0
        self.lblScore = LblScore()
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 100
        self.lblTime = LblTime()
        self.monkey = Monkey(self)
        self.bananas = []
        self.lives = 3
        self.lblLives = simpleGE.Label()
        self.lblLives.center = (320, 60)
        self.lblLives.text = f"Lives: {self.lives}"
        self.numCoconuts = 2
        self.coconuts = []
        self.numSnakes = 1
        self.snakes = []
        
        for i in range(self.numSnakes):
            self.snakes.append(Snake(self))
        
        for i in range(self.numCoconuts):
            self.coconuts.append(Coconut(self))

        for i in range(self.numBananas):
            self.bananas.append(Banana(self))
        self.sprites = [self.monkey,
                        self.bananas,
                        self.coconuts,
                        self.snakes,
                        self.lblScore,
                        self.lblTime,
                        self.lblLives]
        

    def process(self):
        for banana in self.bananas:
            if banana.collidesWith(self.monkey):
                banana.reset()
                self.sndBanana.play()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
        self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:

            print(f"Score: {self.score}")
            self.stop()
            
        for coconut in self.coconuts:
            if coconut.collidesWith(self.monkey):
                coconut.reset()
                self.lives -= 1
                self.sndCoconut.play()
                self.lblLives.text = f"Lives: {self.lives}"
                if self.lives <= 0:
                    
                    self.stop()
                    
        for snake in self.snakes:
             if snake.collidesWith(self.monkey):
                 snake.reset()
                 self.lives -= 3
                 self.sndSnake.play()
                 self.lblLives.text = f"Lives: {self.lives}"
                 if self.lives <= 0:
                     
                     self.stop()           

class Instructions(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()
        self.prevScore = prevScore
        self.setImage("jungle.jpg")
        self.response = "Quit"
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [

            "TROPICAL TREAT!",

            "Uh Oh! Your stuck in the jungle and need bananas as food!",

            "Move with left and right arrow keys.",

            "But watch out for snakes and coconuts!",
           " Coconuts do 1 life but snakes end the game!",

            "",

            "Good luck! And Be Careful! It's The Jungle!"]

        self.directions.center = (320, 200)
        self.directions.size = (600, 300)
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100, 400)
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540, 400)
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Last score: 0"
        self.lblScore.center = (320, 400)
        self.lblScore.text = f"Last score: {self.prevScore}"

        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]

    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()

        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()

def main():
    pygame.mixer.music.load("jungle.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    
    keepGoing = True
    lastScore = 0

    while keepGoing:
        instructions = Instructions(lastScore)
        instructions.start()
        if instructions.response == "Play":
            game = Game()
            game.start()
            lastScore = game.score
        else:
            keepGoing = False
if __name__ == "__main__":

    main()

