import pygame
from utils import COLOR, GameState, Map

def selection_screen(screen):

    # Constants for screen dimensions and fonts
    fonts = pygame.font.Font(None, 36)
    fontl = pygame.font.Font(None, 72)

    # Button
    play_button = pygame.Rect(300, 150, 200, 100)
    field_button = pygame.Rect(300, 275, 200, 50)
    beach_button = pygame.Rect(300, 350, 200, 50)
    moon_button = pygame.Rect(300, 425, 200, 50)
    current_selection_button = pygame.Rect(300, 50, 350, 50) 
    quit_button = pygame.Rect(600, 500, 100, 50)

    map = Map.Beach

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    # Transition to the WORLDS screen when "Play" is clicked
                    return map
                elif field_button.collidepoint(event.pos):
                    map = Map.Field
                elif beach_button.collidepoint(event.pos):
                    map = Map.Beach
                elif moon_button.collidepoint(event.pos):
                    map = Map.Moon
                elif quit_button.collidepoint(event.pos):  # Handle the "Quit" button
                    return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
        screen.fill(COLOR.WHITE)

        # Display username at the top of the screen
        title_text = fonts.render(f"SELECT MAP", True, COLOR.BLACK)
        screen.blit(title_text, (50, 50))

        # Draw the "Play" button
        pygame.draw.rect(screen, COLOR.BLACK, play_button)
        play_text = fontl.render("Play", True, COLOR.WHITE)
        screen.blit(play_text, (play_button.x + 48, play_button.y + 25))
        pygame.draw.rect(screen, COLOR.LIGHT, field_button)
        collection_text = fonts.render("Field", True, COLOR.GREEN)
        screen.blit(collection_text, (field_button.x + 35, field_button.y + 10))
        pygame.draw.rect(screen, COLOR.BLUE, beach_button)
        achievements_text = fonts.render("Beach", True, COLOR.TEAL)
        screen.blit(achievements_text, (beach_button.x + 15, beach_button.y + 10))
        pygame.draw.rect(screen, COLOR.FAINT, moon_button)
        achievements_text = fonts.render("Moon", True, COLOR.GRAY)
        screen.blit(achievements_text, (moon_button.x + 15, moon_button.y + 10))
        pygame.draw.rect(screen, map.secondary, current_selection_button)
        current_selection_text = fonts.render(f"Current Selection: {map.name}", True, map.primary)
        screen.blit(current_selection_text, (current_selection_button.x + 15, current_selection_button.y + 10))
        pygame.draw.rect(screen, COLOR.BLACK, quit_button) 
        quit_text = fonts.render("Quit", True, COLOR.WHITE)
        screen.blit(quit_text, (quit_button.x + 20, quit_button.y + 10))

        pygame.display.flip()