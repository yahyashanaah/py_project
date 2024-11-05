import pygame
import time

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Game")

# Load assets
car_img = pygame.image.load('car.png')
background_img = pygame.image.load('background.png')

# Game variables
car_x, car_y = width * 0.45, height * 0.8
car_speed = 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle key events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car_speed = -5
            elif event.key == pygame.K_RIGHT:
                car_speed = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                car_speed = 0

    # Update car position
    car_x += car_speed

    # Render game
    window.blit(background_img, (0, 0))
    window.blit(car_img, (car_x, car_y))
    pygame.display.update()

    # Cap the frame rate
    time.sleep(0.01)

pygame.quit()
