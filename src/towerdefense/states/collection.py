import pygame
from ..util.utils import COLOR, GameState

def collection_screen(screen):

    # Constants for screen dimensions and fonts
    fonts = pygame.font.Font(None, 36)
    fontl = pygame.font.Font(None, 72)

    # Button
    quit_button = pygame.Rect(600, 500, 100, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return GameState.MENU
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):  # Handle the "Quit" button
                    return GameState.MENU
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameState.MENU
        screen.fill(COLOR.WHITE)

        # Display username at the top of the screen
        title_text = fontl.render(f"COLLECTION", True, COLOR.BLACK)
        screen.blit(title_text, (50, 50))

        # Draw the "Play" button
        pygame.draw.rect(screen, COLOR.BLACK, quit_button) 
        quit_text = fonts.render("Main Menu", True, COLOR.WHITE)
        screen.blit(quit_text, (quit_button.x + 20, quit_button.y + 10))

        pygame.display.flip()