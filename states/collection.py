import pygame
from utils import COLOR, GameState

def collection_screen(screen):

    # Constants for screen dimensions and fonts
    fonts = pygame.font.Font(None, 36)
    fontl = pygame.font.Font(None, 72)

    # Button
    play_button = pygame.Rect(300, 200, 200, 100)
    collection_button = pygame.Rect(300, 325, 200, 50)
    achievements_button = pygame.Rect(300, 400, 200, 50)
    quit_button = pygame.Rect(600, 500, 100, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return GameState.MENU
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    # Transition to the WORLDS screen when "Play" is clicked
                    return GameState.MAP_SELECTION
                elif collection_button.collidepoint(event.pos):
                    return GameState.COLLECTION
                elif achievements_button.collidepoint(event.pos):
                    return GameState.ACHIEVEMENTS
                elif quit_button.collidepoint(event.pos):  # Handle the "Quit" button
                    return GameState.MENU
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameState.MENU
        screen.fill(COLOR.WHITE)

        # Display username at the top of the screen
        title_text = fonts.render(f"COLLECTION", True, COLOR.BLACK)
        screen.blit(title_text, (50, 50))

        # Draw the "Play" button
        pygame.draw.rect(screen, COLOR.BLACK, play_button)
        play_text = fontl.render("Play", True, COLOR.WHITE)
        screen.blit(play_text, (play_button.x + 48, play_button.y + 25))
        pygame.draw.rect(screen, COLOR.BLACK, collection_button)
        collection_text = fonts.render("Collection", True, COLOR.WHITE)
        screen.blit(collection_text, (collection_button.x + 35, collection_button.y + 10))
        pygame.draw.rect(screen, COLOR.BLACK, achievements_button)
        achievements_text = fonts.render("Achievements", True, COLOR.WHITE)
        screen.blit(achievements_text, (achievements_button.x + 15, achievements_button.y + 10))
        pygame.draw.rect(screen, COLOR.BLACK, quit_button) 
        quit_text = fonts.render("Quit", True, COLOR.WHITE)
        screen.blit(quit_text, (quit_button.x + 20, quit_button.y + 10))

        pygame.display.flip()

    return GameState.MENU