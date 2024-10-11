import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)

# Load images
player_image = pygame.image.load("player.png")  # Replace with your player image file
player_image = pygame.transform.scale(player_image, (50, 50))  # Resize to fit

apple_image = pygame.image.load("apple.png")  # Replace with your apple image file
apple_image = pygame.transform.scale(apple_image, (30, 30))  # Resize to fit

background_image = pygame.image.load("background.png")  # Replace with your background image file
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Resize to fit

# Load sound effects
collect_sound = pygame.mixer.Sound("collect.mp3")  # Replace with your collect sound file
game_over_sound = pygame.mixer.Sound("game_over.mp3")  # Replace with your game over sound file

# Game variables
player_pos = [WIDTH // 2, HEIGHT - 60]
apples = [[random.randint(0, WIDTH - 30), 0] for _ in range(5)]
score = 0
fall_speeds = [random.randint(2, 5) for _ in range(5)]
missed_apples = 0
max_missed = 5

# Font for score display
font = pygame.font.Font(None, 36)

# Game loop
def game_loop():
    global apples, score, missed_apples
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Apple Collecting Game")
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(background_image, (0, 0))  # Draw the background

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 10
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - 50:
            player_pos[0] += 10

        # Apples falling
        for i in range(len(apples)):
            apples[i][1] += fall_speeds[i]
            if apples[i][1] > HEIGHT:
                apples[i] = [random.randint(0, WIDTH - 30), 0]  # Reset apple position
                missed_apples += 1

            # Collision detection
            if (apples[i][0] < player_pos[0] + 50 and
                apples[i][0] + 30 > player_pos[0] and
                apples[i][1] < player_pos[1] + 50 and
                apples[i][1] + 30 > player_pos[1]):
                score += 1
                collect_sound.play()
                apples[i] = [random.randint(0, WIDTH - 30), 0]  # Reset apple position

        # Check for game over
        if missed_apples >= max_missed:
            game_over_sound.play()
            print(f"Game Over! Your score: {score}")
            running = False

        # Draw player and apples
        screen.blit(player_image, (player_pos[0], player_pos[1]))
        for apple_pos in apples:
            screen.blit(apple_image, (apple_pos[0], apple_pos[1]))

        # Display score and missed apples
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        missed_text = font.render(f"Missed: {missed_apples}/{max_missed}", True, (255, 0, 0))
        screen.blit(missed_text, (10, 40))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
