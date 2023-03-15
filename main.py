import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Snake Game"
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

# Set up the game clock
clock = pygame.time.Clock()

# Set up the game variables
SNAKE_SIZE = 20
APPLE_SIZE = 20
SNAKE_COLOR = (0, 255, 0)  # Green
APPLE_COLOR = (255, 0, 0)  # Red
score = 0


# Define the Snake class
class Snake:
    def __init__(self):
        self.segments = [(0, 0), (SNAKE_SIZE, 0), (SNAKE_SIZE * 2, 0)]
        self.direction = "RIGHT"

    def move(self):
        # Move the snake by adding a new segment in the current direction and removing the tail
        global new_head
        head = self.segments[-1]
        if self.direction == "RIGHT":
            new_head = (head[0] + SNAKE_SIZE, head[1])
        elif self.direction == "LEFT":
            new_head = (head[0] - SNAKE_SIZE, head[1])
        elif self.direction == "UP":
            new_head = (head[0], head[1] - SNAKE_SIZE)
        elif self.direction == "DOWN":
            new_head = (head[0], head[1] + SNAKE_SIZE)
        self.segments.append(new_head)
        self.segments.pop(0)

    def draw(self):
        # Draw each segment of the snake
        for segment in self.segments:
            pygame.draw.rect(game_window, SNAKE_COLOR, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

    def grow(self):
        # Add a new segment to the end of the snake
        global new_tail
        tail = self.segments[0]
        if self.direction == "RIGHT":
            new_tail = (tail[0] - SNAKE_SIZE, tail[1])
        elif self.direction == "LEFT":
            new_tail = (tail[0] + SNAKE_SIZE, tail[1])
        elif self.direction == "UP":
            new_tail = (tail[0], tail[1] + SNAKE_SIZE)
        elif self.direction == "DOWN":
            new_tail = (tail[0], tail[1] - SNAKE_SIZE)
        self.segments.insert(0, new_tail)


# Define the Apple class
class Apple:
    def __init__(self):
        self.position = self.randomize_position()

    def draw(self):
        # Draw the apple
        pygame.draw.rect(game_window, APPLE_COLOR, (self.position[0], self.position[1], APPLE_SIZE, APPLE_SIZE))

    @staticmethod
    def randomize_position():
        # Generate a random position for the apple
        x = random.randint(0, WINDOW_WIDTH - APPLE_SIZE)
        y = random.randint(0, WINDOW_HEIGHT - APPLE_SIZE)
        return x // SNAKE_SIZE * SNAKE_SIZE, y // SNAKE_SIZE * SNAKE_SIZE


# Create the Snake and Apple objects
snake = Snake()
apple = Apple()

# Set up the game loop
game_running = True
clock = pygame.time.Clock()

while game_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                snake.direction = "RIGHT"
            elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                snake.direction = "LEFT"
            elif event.key == pygame.K_UP and snake.direction != "DOWN":
                snake.direction = "UP"
            elif event.key == pygame.K_DOWN and snake.direction != "UP":
                snake.direction = "DOWN"

    # Move the snake
    snake.move()

    # Check if the snake has collided with the wall
    if snake.segments[-1][0] < 0 or snake.segments[-1][0] >= WINDOW_WIDTH or snake.segments[-1][1] < 0 or \
            snake.segments[-1][1] >= WINDOW_HEIGHT:
        game_running = False

    # Check if the snake has collided with the apple
    if snake.segments[-1][0] == apple.position[0] and snake.segments[-1][1] == apple.position[1]:
        apple.position = apple.randomize_position()
        snake.grow()
        score += 10

    # Check if the snake has collided with itself
    for segment in snake.segments[:-1]:
        if snake.segments[-1][0] == segment[0] and snake.segments[-1][1] == segment[1]:
            game_running = False

    # Draw the game objects
    game_window.fill((0, 0, 0))  # Clear the screen
    snake.draw()
    apple.draw()
    pygame.display.set_caption(f"{WINDOW_TITLE} - Score: {score}")
    pygame.display.update()

    # Set the game clock
    clock.tick(10)

# Quit Pygame
pygame.quit()
