import pygame
from pygame.locals import *
import time
import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
BLOCK_SIZE = 40
BORDER_COLOR = (255, 105, 180)  # Pink
BORDER_THICKNESS = 4

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("data/apple.jpg").convert()
        self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))
        self.move()

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = random.randint(1, (SCREEN_WIDTH // BLOCK_SIZE) - 2) * BLOCK_SIZE
        self.y = random.randint(1, (SCREEN_HEIGHT // BLOCK_SIZE) - 2) * BLOCK_SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("data/block.jpg").convert()
        self.block = pygame.transform.scale(self.block, (BLOCK_SIZE, BLOCK_SIZE))
        self.x = [BLOCK_SIZE, 0, 0]
        self.y = [BLOCK_SIZE, 0, 0]
        self.direction = 'RIGHT'
        self.length = 1

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill((0, 80, 50))  # Dark green background
        pygame.draw.rect(self.parent_screen, BORDER_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), BORDER_THICKNESS)

        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def move_left(self):
        self.direction = 'LEFT'

    def move_right(self):
        self.direction = 'RIGHT'

    def move_up(self):
        self.direction = 'UP'

    def move_down(self):
        self.direction = 'DOWN'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'LEFT':
            self.x[0] -= BLOCK_SIZE
        elif self.direction == 'RIGHT':
            self.x[0] += BLOCK_SIZE
        elif self.direction == 'UP':
            self.y[0] -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            self.y[0] += BLOCK_SIZE

        self.draw()

    def collision_with_self(self):
        for i in range(1, self.length):
            if self.x[0] == self.x[i] and self.y[0] == self.y[i]:
                return True
        return False

    def boundary_hit(self):
        if self.x[0] < BORDER_THICKNESS or self.x[0] >= SCREEN_WIDTH - BORDER_THICKNESS:
            return True
        if self.y[0] < BORDER_THICKNESS or self.y[0] >= SCREEN_HEIGHT - BORDER_THICKNESS:
            return True
        return False

def play_background_music():
    pygame.mixer.music.load("data/bg_music.mp3")
    pygame.mixer.music.play(-1)

def sound_effect(file):
    sound = pygame.mixer.Sound(file)
    sound.play()

def show_game_over(screen, message):
    font = pygame.font.SysFont('arial', 48, bold=True)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def main():
    pygame.init()
    pygame.mixer.init()
    play_background_music()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake And Apple Game")
    clock = pygame.time.Clock()

    snake = Snake(screen)
    apple = Apple(screen)

    running = True
    pause = False

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_RETURN:
                    pause = False
                if not pause:
                    if event.key == K_LEFT:
                        snake.move_left()
                    elif event.key == K_RIGHT:
                        snake.move_right()
                    elif event.key == K_UP:
                        snake.move_up()
                    elif event.key == K_DOWN:
                        snake.move_down()
            elif event.type == QUIT:
                running = False

        if not pause:
            snake.walk()
            apple.draw()
            pygame.display.flip()

            # Collision with apple
            if abs(snake.x[0] - apple.x) < BLOCK_SIZE and abs(snake.y[0] - apple.y) < BLOCK_SIZE:
                sound_effect("data/ding.mp3")
                snake.increase_length()
                apple.move()

            # Collision with wall or self
            if snake.boundary_hit():
                sound_effect("data/crash.mp3")
                pygame.mixer.music.stop()
                show_game_over(screen, "GAME OVER! Hit Wall - Press Enter to Restart")
                pause = True
                snake = Snake(screen)
                apple = Apple(screen)

            elif snake.collision_with_self():
                sound_effect("data/crash.mp3")
                pygame.mixer.music.stop()
                show_game_over(screen, "GAME OVER! Bit Itself - Press Enter to Restart")
                pause = True
                snake = Snake(screen)
                apple = Apple(screen)

            time.sleep(0.15)
            clock.tick(30)

if __name__ == "__main__":
    main()
