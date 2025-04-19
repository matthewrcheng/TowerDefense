import pygame
import pygame_widgets
import glob, os
import sys
from pygame.mixer import Sound
from pygame_widgets.dropdown import Dropdown

# Sound('sounds/throw.ogg')

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sound Picker')

# read in all sounds from /sounds/ folder
os.chdir('sounds')
sound_files = glob.glob('*.ogg')

# create a dropdown menu for the user to select a sound
sound_dropdowns = []
times = 1
start = 0
end = 12
while start < len(sound_files):
    sound_dropdowns.append(Dropdown(win=screen, x=50, y=times*50, width=300, height=50, name='Select Sound', 
                                    choices=sound_files[start:end]))
    start += 12
    end += 12
    times += 1

# play button to play the selected sound
play_button = pygame.Rect(400, 50, 100, 50)

selection = 0

next_selection_button = pygame.Rect(650, 500, 100, 50)
prev_selection_button = pygame.Rect(650, 600, 100, 50)

# Game loop
running = True
while running:
    screen.fill(WHITE)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(event.pos):
                # get the selected sound file from the dropdown menu
                selected_sound = sound_dropdowns[selection].getSelected()
                # play the selected sound
                pygame.mixer.Sound(selected_sound).play()

            elif next_selection_button.collidepoint(event.pos):
                selection = (selection + 1) % len(sound_dropdowns)

            elif prev_selection_button.collidepoint(event.pos):
                selection = (selection - 1) % len(sound_dropdowns)

    # Draw play button
    pygame.draw.rect(screen, BLACK, play_button)
    font = pygame.font.Font(None, 36)
    text = font.render('Play Sound', True, WHITE)
    screen.blit(text, (play_button.x + 20, play_button.y + 10))

    # Draw next button
    pygame.draw.rect(screen, BLACK, next_selection_button)
    font = pygame.font.Font(None, 36)
    text = font.render('Next', True, WHITE)
    screen.blit(text, (next_selection_button.x + 20, next_selection_button.y + 10))

    # Draw previous button
    pygame.draw.rect(screen, BLACK, prev_selection_button)
    font = pygame.font.Font(None, 36)
    text = font.render('Previous', True, WHITE)
    screen.blit(text, (prev_selection_button.x + 20, prev_selection_button.y + 10))

    # Draw dropdown menu
    sound_dropdowns[selection].draw()

    # Update display
    pygame_widgets.update(events=events)
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()