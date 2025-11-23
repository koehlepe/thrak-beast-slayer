import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WAVE_DELAY = 3000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("THRAK: Beast Slayer")
clock = pygame.time.Clock()
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 60), pygame.SRCALPHA)
        # Head
        pygame.draw.circle(self.image, (200, 150, 100), (25, 12), 10)
        # Hair/wild mane
        pygame.draw.circle(self.image, (100, 50, 0), (25, 8), 12)
        pygame.draw.circle(self.image, (100, 50, 0), (18, 10), 8)
        pygame.draw.circle(self.image, (100, 50, 0), (32, 10), 8)
        # Body
        pygame.draw.rect(self.image, (139, 69, 19), (15, 22, 20, 18))
        # Arms
        pygame.draw.line(self.image, (200, 150, 100), (15, 25), (5, 35), 4)
        pygame.draw.line(self.image, (200, 150, 100), (35, 25), (45, 35), 4)
        # Legs
        pygame.draw.line(self.image, (80, 40, 20), (18, 40), (15, 55), 4)
        pygame.draw.line(self.image, (80, 40, 20), (32, 40), (35, 55), 4)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.speed = 5
        self.health = 3
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.rect.width:
            self.rect.x += self.speed

    def shoot(self):
        spear = Spear(self.rect.centerx, self.rect.top)
        all_sprites.add(spear)
        spears.add(spear)

class Spear(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((12, 30), pygame.SRCALPHA)
        # Spear shaft
        pygame.draw.line(self.image, (139, 69, 19), (6, 0), (6, 25), 3)
        # Spear head
        pygame.draw.polygon(self.image, (200, 200, 200), [(6, 0), (2, 8), (6, 5), (10, 8)])
        # Feathers/fletching
        pygame.draw.polygon(self.image, (255, 200, 0), [(3, 20), (6, 28), (9, 20)])
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type
        self.health = 1

        if enemy_type == "tiger":
            self.image = pygame.Surface((60, 50), pygame.SRCALPHA)
            # Body
            pygame.draw.ellipse(self.image, (255, 140, 0), (10, 15, 40, 20))
            # Head
            pygame.draw.circle(self.image, (255, 160, 20), (45, 20), 12)
            # Stripes
            pygame.draw.line(self.image, (200, 80, 0), (15, 18), (20, 28), 2)
            pygame.draw.line(self.image, (200, 80, 0), (25, 15), (30, 28), 2)
            pygame.draw.line(self.image, (200, 80, 0), (35, 15), (38, 28), 2)
            # Fangs
            pygame.draw.line(self.image, (255, 255, 255), (50, 28), (52, 35), 2)
            pygame.draw.line(self.image, (255, 255, 255), (56, 28), (58, 35), 2)
            # Tail
            pygame.draw.line(self.image, (200, 100, 0), (10, 22), (0, 15), 3)
            self.speed = 2.5
            self.points = 100

        elif enemy_type == "wolf":
            self.image = pygame.Surface((55, 45), pygame.SRCALPHA)
            # Body
            pygame.draw.ellipse(self.image, (80, 80, 90), (10, 15, 35, 18))
            # Head
            pygame.draw.circle(self.image, (100, 100, 110), (45, 18), 11)
            # Ears
            pygame.draw.polygon(self.image, (100, 100, 110), [(40, 5), (45, 0), (50, 5)])
            # Snout
            pygame.draw.circle(self.image, (120, 120, 130), (52, 20), 5)
            # Eyes
            pygame.draw.circle(self.image, (255, 200, 0), (48, 14), 2)
            # Tail
            pygame.draw.line(self.image, (80, 80, 90), (10, 18), (0, 10), 3)
            self.speed = 3.5
            self.points = 150

        elif enemy_type == "mammoth":
            self.image = pygame.Surface((80, 65), pygame.SRCALPHA)
            # Body
            pygame.draw.ellipse(self.image, (120, 80, 60), (15, 20, 50, 35))
            # Head
            pygame.draw.circle(self.image, (130, 90, 70), (20, 25), 13)
            # Large tusks
            pygame.draw.line(self.image, (240, 240, 200), (15, 35), (5, 45), 5)
            pygame.draw.line(self.image, (240, 240, 200), (25, 35), (0, 50), 5)
            # Trunk
            pygame.draw.arc(self.image, (100, 60, 40), (18, 30, 15, 20), 0, 3.14, 4)
            # Fur texture
            pygame.draw.line(self.image, (80, 50, 30), (25, 20), (28, 35), 2)
            pygame.draw.line(self.image, (80, 50, 30), (35, 18), (38, 35), 2)
            pygame.draw.line(self.image, (80, 50, 30), (45, 20), (48, 35), 2)
            self.health = 3
            self.speed = 1.5
            self.points = 300

        elif enemy_type == "scorpion":
            self.image = pygame.Surface((50, 55), pygame.SRCALPHA)
            # Body segments
            pygame.draw.circle(self.image, (139, 35, 69), (15, 25), 8)
            pygame.draw.circle(self.image, (139, 35, 69), (25, 32), 8)
            pygame.draw.ellipse(self.image, (139, 35, 69), (20, 35, 15, 12))
            # Head
            pygame.draw.circle(self.image, (180, 50, 100), (10, 15), 8)
            # Pincers
            pygame.draw.line(self.image, (180, 50, 100), (8, 10), (0, 5), 3)
            pygame.draw.line(self.image, (180, 50, 100), (12, 10), (5, 0), 3)
            # Stinger/tail
            pygame.draw.line(self.image, (200, 30, 80), (25, 30), (28, 10), 3)
            pygame.draw.line(self.image, (200, 30, 80), (28, 10), (32, 5), 3)
            pygame.draw.polygon(self.image, (255, 80, 150), [(28, 5), (26, 0), (32, 2), (30, 8)])
            self.speed = 4
            self.points = 120

        elif enemy_type == "pterodactyl":
            self.image = pygame.Surface((65, 45), pygame.SRCALPHA)
            # Wing
            pygame.draw.polygon(self.image, (100, 100, 120), [(10, 20), (0, 15), (5, 30), (25, 25)])
            pygame.draw.polygon(self.image, (120, 120, 140), [(10, 20), (0, 15), (3, 18)])
            # Body
            pygame.draw.circle(self.image, (110, 110, 130), (28, 22), 8)
            # Head
            pygame.draw.polygon(self.image, (130, 130, 150), [(35, 18), (60, 12), (62, 18), (55, 22)])
            # Long beak
            pygame.draw.line(self.image, (150, 150, 170), (62, 15), (65, 15), 3)
            # Eye
            pygame.draw.circle(self.image, (255, 255, 0), (58, 14), 2)
            # Legs
            pygame.draw.line(self.image, (150, 150, 170), (28, 28), (25, 38), 2)
            pygame.draw.line(self.image, (150, 150, 170), (32, 28), (35, 38), 2)
            self.speed = 3
            self.points = 140

        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = random.choice([-1, 1])

    def update(self):
        # Move toward player horizontally
        player_x = player.rect.centerx
        enemy_center = self.rect.centerx
        
        if enemy_center < player_x - 10:
            self.rect.x += self.speed
        elif enemy_center > player_x + 10:
            self.rect.x -= self.speed
        
        # Keep within bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
        # Move down faster - attack pattern
        self.rect.y += 2.5

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return True
        return False
def spawn_wave(wave_num):
    enemy_types = ["tiger", "wolf", "mammoth", "scorpion", "pterodactyl"]
    num_enemies = min(3 + wave_num, 8)
    
    for i in range(num_enemies):
        enemy_type = random.choice(enemy_types)
        x = random.randint(50, SCREEN_WIDTH - 100)
        y = random.randint(-200, -50)
        enemy = Enemy(x, y, enemy_type)
        all_sprites.add(enemy)
        enemies.add(enemy)

def draw_game():
    # Draw cave background with gradient
    for y in range(SCREEN_HEIGHT):
        color_val = int(70 + (y / SCREEN_HEIGHT) * 40)
        pygame.draw.line(screen, (color_val, color_val // 2, 0), (0, y), (SCREEN_WIDTH, y))
    
    # Draw distant cave walls (perspective effect)
    pygame.draw.polygon(screen, (50, 35, 15), [(0, 0), (SCREEN_WIDTH, 0), (SCREEN_WIDTH - 150, 150), (150, 150)])
    
    # Draw scattered rocks and boulders across the cave floor
    rock_positions = [
        (80, 120, 15), (200, 100, 20), (350, 140, 18), (500, 95, 22), (650, 130, 16),
        (120, 200, 12), (300, 220, 25), (550, 210, 14), (700, 240, 19),
        (180, 300, 18), (420, 320, 16), (600, 310, 21),
    ]
    for rock_x, rock_y, rock_size in rock_positions:
        pygame.draw.circle(screen, (50, 30, 15), (rock_x, rock_y), rock_size)
        pygame.draw.circle(screen, (60, 38, 18), (rock_x - 5, rock_y - 5), rock_size - 2)
    
    # Draw bushes/vegetation
    bush_positions = [(150, 180), (400, 200), (700, 160), (250, 320), (550, 280)]
    for bush_x, bush_y in bush_positions:
        # Bush base
        pygame.draw.ellipse(screen, (34, 80, 20), (bush_x - 20, bush_y - 15, 40, 30))
        # Bush highlights
        pygame.draw.circle(screen, (50, 120, 30), (bush_x - 10, bush_y - 10), 12)
        pygame.draw.circle(screen, (50, 120, 30), (bush_x + 10, bush_y - 8), 11)
        pygame.draw.circle(screen, (45, 110, 25), (bush_x, bush_y + 5), 10)
    
    # Draw cave cracks/crevices on ground
    pygame.draw.line(screen, (30, 15, 5), (100, 350), (180, 500), 2)
    pygame.draw.line(screen, (30, 15, 5), (400, 320), (420, 550), 2)
    pygame.draw.line(screen, (30, 15, 5), (700, 380), (650, 550), 2)
    
    # Draw ground/terrain at bottom (darker)
    pygame.draw.polygon(screen, (40, 25, 10), [(0, SCREEN_HEIGHT - 80), (SCREEN_WIDTH, SCREEN_HEIGHT - 80), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)])
    
    # Draw rocky terrain features at bottom
    rock_positions_bottom = [(100, SCREEN_HEIGHT - 60), (250, SCREEN_HEIGHT - 50), (400, SCREEN_HEIGHT - 70), (550, SCREEN_HEIGHT - 55), (700, SCREEN_HEIGHT - 65)]
    for rock_x, rock_y in rock_positions_bottom:
        pygame.draw.circle(screen, (35, 20, 8), (rock_x, rock_y), 28)
        pygame.draw.circle(screen, (45, 28, 12), (rock_x, rock_y), 23)
    
    all_sprites.draw(screen)
    
    # Draw HUD with top-down view indicator
    health_text = font_small.render(f"Health: {player.health}", True, (255, 255, 255))
    score_text = font_small.render(f"Score: {player.score}", True, (255, 255, 255))
    wave_text = font_small.render(f"Wave: {wave_num}", True, (255, 255, 255))
    view_text = font_small.render("TOP-DOWN VIEW", True, (150, 200, 255))
    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 40))
    screen.blit(wave_text, (SCREEN_WIDTH - 150, 10))
    screen.blit(view_text, (SCREEN_WIDTH // 2 - 70, 10))

def draw_menu():
    # Draw night sky background with stars
    screen.fill((20, 15, 40))
    
    # Draw stars
    for i in range(0, SCREEN_WIDTH, 60):
        for j in range(0, 150, 60):
            pygame.draw.circle(screen, (255, 255, 200), (i + random.randint(-20, 20), j + random.randint(-20, 20)), 2)
    
    # Draw moon
    pygame.draw.circle(screen, (240, 240, 180), (SCREEN_WIDTH - 80, 80), 60)
    pygame.draw.circle(screen, (20, 15, 40), (SCREEN_WIDTH - 70, 60), 50)
    
    # Draw mountains/cave entrance silhouette
    pygame.draw.polygon(screen, (30, 20, 10), [(0, SCREEN_HEIGHT), (150, 250), (SCREEN_WIDTH // 2, 200), (SCREEN_WIDTH - 150, 250), (SCREEN_WIDTH, SCREEN_HEIGHT)])
    pygame.draw.polygon(screen, (40, 30, 15), [(150, 250), (SCREEN_WIDTH // 2, 200), (SCREEN_WIDTH - 150, 250)])
    
    title = font_large.render("THRAK", True, (255, 100, 0))
    subtitle = font_medium.render("BEAST SLAYER OF THE STONE AGE", True, (255, 200, 0))
    
    # Backstory text
    backstory_font = pygame.font.Font(None, 18)
    story_line1 = backstory_font.render("The ancient beasts have awakened. Darkness spreads across the land.", True, (200, 200, 200))
    story_line2 = backstory_font.render("Your tribe looks to you, THRAK, their greatest warrior.", True, (200, 200, 200))
    story_line3 = backstory_font.render("With spear in hand and fire in your heart, defend them or perish.", True, (200, 200, 200))
    
    instructions = font_small.render("Press SPACE to Hunt | Arrow Keys to Move | SPACE to Throw Spear", True, (200, 200, 200))
    
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
    screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 160))
    screen.blit(story_line1, (SCREEN_WIDTH // 2 - story_line1.get_width() // 2, 240))
    screen.blit(story_line2, (SCREEN_WIDTH // 2 - story_line2.get_width() // 2, 270))
    screen.blit(story_line3, (SCREEN_WIDTH // 2 - story_line3.get_width() // 2, 300))
    screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, 400))

def draw_game_over():
    # Draw cave background with gradient
    for y in range(SCREEN_HEIGHT):
        color_val = int(70 + (y / SCREEN_HEIGHT) * 40)
        pygame.draw.line(screen, (color_val, color_val // 2, 0), (0, y), (SCREEN_WIDTH, y))
    
    # Draw rocky terrain
    pygame.draw.polygon(screen, (60, 40, 20), [(0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT - 80), (0, SCREEN_HEIGHT - 80)])
    
    game_over = font_large.render("GAME OVER", True, (255, 0, 0))
    score_text = font_medium.render(f"Final Score: {player.score}", True, (255, 255, 255))
    wave_text = font_medium.render(f"Wave Reached: {wave_num}", True, (255, 255, 255))
    restart = font_small.render("Press SPACE to return to menu", True, (200, 200, 200))
    screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, 100))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
    screen.blit(wave_text, (SCREEN_WIDTH // 2 - wave_text.get_width() // 2, 320))
    screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 450))

# Sprite groups
all_sprites = pygame.sprite.Group()
spears = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

game_state = MENU
wave_num = 1
wave_timer = 0
shoot_cooldown = 0
running = True

while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == MENU:
                    game_state = PLAYING
                    wave_num = 1
                    player.health = 3
                    player.score = 0
                    enemies.empty()
                    spears.empty()
                    wave_timer = pygame.time.get_ticks() - WAVE_DELAY
                    spawn_wave(wave_num)
                elif game_state == PLAYING:
                    if shoot_cooldown <= 0:
                        player.shoot()
                        shoot_cooldown = 10
                elif game_state == GAME_OVER:
                    game_state = MENU

    if game_state == PLAYING:
        all_sprites.update()
        shoot_cooldown -= 1

        # Collision detection: spears hitting enemies
        for spear in spears:
            hit_enemies = pygame.sprite.spritecollide(spear, enemies, False)
            for enemy in hit_enemies:
                spear.kill()
                if enemy.take_damage():
                    player.score += enemy.points

        # Collision detection: enemy touching player
        if pygame.sprite.spritecollide(player, enemies, False):
            player.health -= 1
            if player.health <= 0:
                game_state = GAME_OVER

        # Check if wave is complete
        if len(enemies) == 0 and pygame.time.get_ticks() - wave_timer > WAVE_DELAY:
            wave_num += 1
            spawn_wave(wave_num)
            wave_timer = pygame.time.get_ticks()

        draw_game()

    elif game_state == MENU:
        draw_menu()

    elif game_state == GAME_OVER:
        draw_game_over()

    pygame.display.flip()

pygame.quit()