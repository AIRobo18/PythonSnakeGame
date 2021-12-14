from tkinter import *
import random
from tkinter import font

# Constants
GAME_WIDTH = 750
GAME_HEIGHT = 750
SPEED = 80
ASSEST_SIZE = 30

INITIAL_SNAKE_PARTS = 3
SNAKE_COLOR = "pink"

SNACK_COLOR = "purple"
BACKGROUND_COLOR = "black"

class Snake:
    def __init__(self) -> None:
        self.bodySize = INITIAL_SNAKE_PARTS
        self.coordinates = []
        self.squares = []

        # Snake starts at top left corner
        for i in range(0, INITIAL_SNAKE_PARTS):
            self.coordinates.append([0,0])

        # Create each body part of the snake
        for x, y, in self.coordinates:
            square = canvas.create_rectangle(x, y, x+ASSEST_SIZE, y+ASSEST_SIZE, fill=SNAKE_COLOR, tags="snake")
            self.squares.append(square)

    def updateSnakePlacement(self, x, y):
        self.coordinates.insert(0, (x, y))
        square = canvas.create_rectangle(x, y, x+ASSEST_SIZE, y+ASSEST_SIZE, fill=SNAKE_COLOR)
        self.squares.insert(0, square)

    def deleteSnakeTail(self):
        del self.coordinates[-1]
        canvas.delete(self.squares[-1])
        del self.squares[-1]

class Snack:
    def __init__(self) -> None:
        x, y = self.spawnSnack()
        self.coordinates = [x, y]

        # Draw snack
        canvas.create_oval(x, y, x+ASSEST_SIZE, y+ASSEST_SIZE, fill=SNACK_COLOR, tags="snack")

    def spawnSnack(self):
        global snake

        x = random.randint(0, (GAME_WIDTH/ASSEST_SIZE)-1) * ASSEST_SIZE
        y = random.randint(0, (GAME_HEIGHT/ASSEST_SIZE)-1) * ASSEST_SIZE

        # Make sure snack does not spwn on top of snake
        while [x, y] in snake.coordinates:
            x = random.randint(0, (GAME_WIDTH/ASSEST_SIZE)-1) * ASSEST_SIZE
            y = random.randint(0, (GAME_HEIGHT/ASSEST_SIZE)-1) * ASSEST_SIZE
        
        return x, y

def nextRound(snake: Snake, snack: Snack): 
    # Head of snake
    x, y = snake.coordinates[0]

    x, y = move(x, y)

    # move the snake
    snake.updateSnakePlacement(x, y)

    # Check if the snake ate the snack
    if x == snack.coordinates[0] and y == snack.coordinates[1]:
        updateScore()

        # Eat snack and spawn new one
        canvas.delete("snack")
        snack = Snack()
    else:
        # Delete tail of snack so it doesn' infinitly grow
        snake.deleteSnakeTail()

    if checkSnakeCollision(snake):
        gameOver()
    else:
        gameWindow.after(SPEED, nextRound, snake, snack)

def move(x, y):
    global direction
    if direction == "up":
        y -= ASSEST_SIZE
    elif direction == "down":
        y += ASSEST_SIZE
    elif direction == "left":
        x -= ASSEST_SIZE
    elif direction == "right":
        x += ASSEST_SIZE
    
    return x, y

def updateScore():
    global score
    score += 1
    label.config(text="Score:{}".format(score))

def changeDirection(newDirection):
    global direction

    if newDirection == 'up':
        if direction != 'down':
            direction = newDirection
    elif newDirection == 'down':
        if direction != 'up':
            direction = newDirection
    elif newDirection == 'left':
        if direction != 'right':
            direction = newDirection
    elif newDirection == 'right':
        if direction != 'left':
            direction = newDirection

def checkSnakeCollision(snake: Snake):
    # Head of snake
    x, y, = snake.coordinates[0]

    # Snake goes out of bounds
    if x < 0 or x >= GAME_WIDTH:
        return True
    if y < 0 or y >= GAME_HEIGHT:
        return True

    # Snake touches itself
    for bodyPart in snake.coordinates[1:]:
        if x == bodyPart[0] and y == bodyPart[1]:
            return True
    
    return False

def gameOver():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=("Futura", 70), text="GAME OVER", fill="red", tags="gameover")

def centerActualGameWindow():
    gameWindow.update()

    gameWindowWidth = gameWindow.winfo_width()
    gameWindowHeight = gameWindow.winfo_height()
    screenWidth = gameWindow.winfo_screenwidth()
    screenHeight = gameWindow.winfo_screenheight()

    x = int((screenWidth/2) - (gameWindowWidth/2))
    y = int((screenHeight/2) - (gameWindowHeight/2))

    gameWindow.geometry(f"{gameWindowWidth}x{gameWindowHeight}+{x}+{y}")

# Game Renderer
gameWindow = Tk()
gameWindow.title("Snake")
gameWindow.resizable(False, False)

# Game Initials
score = 0
direction = "down"

# Display Score
label = Label(gameWindow, text="Score: {}".format(score), font=('Futura', 40))
label.pack()

# Game area
canvas = Canvas(gameWindow, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Center the actual game window
centerActualGameWindow()

# Bind keys to move snake
gameWindow.bind('<Up>', lambda event: changeDirection('up'))
gameWindow.bind('<Down>', lambda event: changeDirection('down'))
gameWindow.bind('<Left>', lambda event: changeDirection('left'))
gameWindow.bind('<Right>', lambda event: changeDirection('right'))

# Game Objects
snake = Snake()
snack = Snack()

# Run the rounds
nextRound(snake, snack)

# Run Game
gameWindow.mainloop()