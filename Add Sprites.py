import pygame
import random

# Initialize Pygame
pygame.init()

# Define custom events for color changes
SPRITE_COLOR_CHANGE_EVENT = pygame.USEREVENT + 1
BACKGROUND_COLOR_CHANGE_EVENT = pygame.USEREVENT + 2

# Define some colors
BLUE = pygame.Color('blue')
LIGHTBLUE = pygame.Color('lightblue')
DARKBLUE = pygame.Color('darkblue')
YELLOW = pygame.Color('yellow')
MAGENTA = pygame.Color('magenta')
ORANGE = pygame.Color('orange')
WHITE = pygame.Color('white')

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width, controllable=False):
        super().__init__()
        # Create the sprite image and fill it with the specified color
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # Get the rectangle for positioning the sprite
        self.rect = self.image.get_rect()
        # Randomly choose initial velocity
        self.velocity = [random.choice([-1, 1]), random.choice([-1, 1])]
        # Determine if this sprite can be controlled by the user
        self.controllable = controllable

    def update(self):
        if not self.controllable:
            # Move the sprite by its velocity
            self.rect.move_ip(self.velocity)
            boundary_hit = False

            # Check for collision with screen boundaries
            if self.rect.left <= 0 or self.rect.right >= 500:
                self.velocity[0] = -self.velocity[0]
                boundary_hit = True

            if self.rect.top <= 0 or self.rect.bottom >= 400:
                self.velocity[1] = -self.velocity[1]
                boundary_hit = True

            if boundary_hit:
                # Post events to change sprite and background color if boundary is hit
                pygame.event.post(pygame.event.Event(SPRITE_COLOR_CHANGE_EVENT))
                pygame.event.post(pygame.event.Event(BACKGROUND_COLOR_CHANGE_EVENT))
        else:
            # Get keyboard inputs for controlling the sprite
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= 5
            if keys[pygame.K_RIGHT]:
                self.rect.x += 5
            if keys[pygame.K_UP]:
                self.rect.y -= 5
            if keys[pygame.K_DOWN]:
                self.rect.y += 5

    def change_color(self):
        # Change the sprite color to a random one from the list
        self.image.fill(random.choice([YELLOW, MAGENTA, ORANGE, WHITE]))

def change_background_color():
    global bg_color
    bg_color = random.choice([BLUE, LIGHTBLUE, DARKBLUE])

# Create a group to hold all sprites
all_sprites_list = pygame.sprite.Group()

# Create the first sprite
sp1 = Sprite(WHITE, 20, 30)
sp1.rect.x = random.randint(0, 480)
sp1.rect.y = random.randint(0, 370)
all_sprites_list.add(sp1)

# Create the second controllable sprite
sp2 = Sprite(ORANGE, 20, 30, controllable=True)
sp2.rect.x = random.randint(0, 480)
sp2.rect.y = random.randint(0, 370)
all_sprites_list.add(sp2)

# Set up the display
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Colorful Bounce")
bg_color = BLUE
screen.fill(bg_color)

exit = False
clock = pygame.time.Clock()

# Main game loop
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        elif event.type == SPRITE_COLOR_CHANGE_EVENT:
            sp1.change_color()
        elif event.type == BACKGROUND_COLOR_CHANGE_EVENT:
            change_background_color()

    # Update all sprites
    all_sprites_list.update()

    # Redraw the screen with the new background color and sprites
    screen.fill(bg_color)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
