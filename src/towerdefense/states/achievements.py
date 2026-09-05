import pygame
from ..util.utils import COLOR, GameState

def load_achievements() -> list:
    return [('Beat 10 levels', 3, 10), ('Deal 200,000 damage', 134943, 200000), 
            ('Beat Hell difficulty', 0, 1), ('Win 5 times using Farm', 4, 5),
            ('Sample', 2, 10), ('Sample 2', 0, 15), ('sample 3', 7, 8)]

def achievements_screen(screen: pygame.Surface):

    # Constants for screen dimensions and fonts
    fonts = pygame.font.Font(None, 36)
    fontl = pygame.font.Font(None, 72)

    # Buttons
    quit_button = pygame.Rect(screen.get_width()-200, screen.get_height()-50, 200, 50)

    # Achievements menu
    background_rect = pygame.Rect(25, 115, 700, 460)
    ACHIEVEMENT_WIDTH = 700
    ACHIEVEMENT_HEIGHT = 115
    BAR_WIDTH = 300
    BAR_HEIGHT = 30

    achievements = load_achievements()

    scroll = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return GameState.MENU
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):  # Handle the "Quit" button
                    return GameState.MENU
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameState.MENU
            if event.type == pygame.MOUSEWHEEL:
                scroll = scroll - event.y
                if scroll < 0:
                    scroll = 0
                elif scroll >= len(achievements)-3:
                    scroll = len(achievements)-4

        screen.fill(COLOR.BLACK)

        # Display title at the top of the screen
        title_text = fontl.render(f"ACHIEVEMENTS", True, COLOR.WHITE)
        screen.blit(title_text, (50, 50))

        # Draw the "quit" button
        pygame.draw.rect(screen, COLOR.WHITE, quit_button) 
        quit_text = fonts.render("Main Menu", True, COLOR.BLACK)
        screen.blit(quit_text, (quit_button.x + 40, quit_button.y + 10))

        # Draw Achievements menu
        pygame.draw.rect(screen, COLOR.DARK_RED, background_rect)

        for i in range(4):
            idx = (scroll + i) % len(achievements)
            offset = ACHIEVEMENT_HEIGHT*i
            # pygame.draw.rect(screen, COLOR.RED, pygame.Rect(background_rect.topleft[0], 
            #                                                 background_rect.topleft[1]+offset, 
            #                                                 ACHIEVEMENT_WIDTH, 
            #                                                 ACHIEVEMENT_HEIGHT))
            text = fonts.render(achievements[idx][0], True, COLOR.WHITE)
            screen.blit(text, (background_rect.topleft[0]+10, background_rect.topleft[1]+offset+10))
            pygame.draw.rect(screen, COLOR.WHITE, pygame.Rect(background_rect.topleft[0]+350, 
                                                              background_rect.topleft[1]+offset+50, 
                                                              BAR_WIDTH, BAR_HEIGHT))
            pygame.draw.rect(screen, COLOR.YELLOW, pygame.Rect(background_rect.topleft[0]+350, 
                                                              background_rect.topleft[1]+offset+50, 
                                                              round(BAR_WIDTH*(achievements[idx][1]/achievements[idx][2])), 
                                                              BAR_HEIGHT))

        pygame.display.flip()