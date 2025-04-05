import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Color Picker')

# Slider positions and values
slider_positions = {
    "red": 50,
    "green": 50,
    "blue": 50,
    "alpha": 255
}
slider_ranges = {
    "red": (50, 350),
    "green": (50, 350),
    "blue": (50, 350),
    "alpha": (50, 350)
}

slider_colors = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "alpha": (128, 128, 128)
}

dragging = None  # Which slider is being dragged

def draw_sliders():
    """Draw sliders and their current values."""
    font = pygame.font.Font(None, 28)
    
    y_positions = {"red": 50, "green": 120, "blue": 190, "alpha": 260}
    
    for color, y in y_positions.items():
        pygame.draw.line(screen, slider_colors[color], (50, y), (350, y), 5)
        pygame.draw.circle(screen, BLACK, (slider_positions[color], y), 10)
        
        # Draw value text
        text = font.render(f"{color.capitalize()}: {int((slider_positions[color] - 50) * 255 / 300)}", True, BLACK)
        screen.blit(text, (slider_ranges[color][1] + 10, y - 10))

def get_color():
    """Get the selected color based on slider positions."""
    r = int((slider_positions["red"] - 50) * 255 / 300)
    g = int((slider_positions["green"] - 50) * 255 / 300)
    b = int((slider_positions["blue"] - 50) * 255 / 300)
    a = int((slider_positions["alpha"] - 50) * 255 / 300)
    return (r, g, b, a)

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for color, pos_y in {"red": 50, "green": 120, "blue": 190, "alpha": 260}.items():
                if abs(y - pos_y) < 10 and 50 <= x <= 350:
                    dragging = color
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = None
        elif event.type == pygame.MOUSEMOTION and dragging:
            x, _ = event.pos
            slider_positions[dragging] = max(50, min(x, 350))
    
    draw_sliders()

    # Draw the color preview box
    pygame.draw.rect(screen, get_color(), (100, 320, 200, 50))

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
