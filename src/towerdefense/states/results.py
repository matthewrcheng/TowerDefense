import pygame
from ..util.utils import COLOR, GameState

def results_screen(screen: pygame.Surface, win: bool, levels: int = 0, time: int = 0):

    # for now, nothing gets unlocked and coins and xp are displayed, but they do not do anything
    # Set up fonts
    pygame.font.init()
    font_large = pygame.font.Font(None, 60)
    font_medium = pygame.font.Font(None, 40)
    background_rect = pygame.Rect(150, 50, 550, 450)
    return_button = pygame.Rect(200, 350, 250, 70)

    # Calculate time elapsed (for demonstration purposes)
    if not time:
        time_elapsed = 120.5  # Replace this with the actual time elapsed in seconds
    
    # Calculate coins earned based on game completion
    if not levels:
        levels_cleared = 5  # Replace this with the actual number of levels cleared
    
    coins_earned = levels_cleared * 50  # Adjust the coefficient as needed
    
    # Calculate XP gained based on levels completed and time elapsed
    xp_gained = (levels_cleared * 100) - int(time_elapsed)  # Adjust coefficients as needed

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_button.collidepoint(event.pos):
                    return GameState.MENU
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameState.MENU
        
        pygame.draw.rect(screen, COLOR.BLACK, background_rect)
    
        # Display victory screen
        if win:
            victory_text = font_large.render("Victory!", True, COLOR.GOLD)
            screen.blit(victory_text, (200, 100))

        # Display defeat screen
        else:
            defeat_text = font_large.render("Better luck next time...", True, COLOR.RED)
            screen.blit(defeat_text, (100, 100))

        # Display statistics
        stats_text = font_medium.render(f"Time Elapsed: {time_elapsed:.2f} seconds", True, COLOR.WHITE)
        screen.blit(stats_text, (200, 200))

        stats_text = font_medium.render(f"Coins Earned: {coins_earned}", True, COLOR.WHITE)
        screen.blit(stats_text, (200, 250))

        stats_text = font_medium.render(f"XP Gained: {xp_gained}", True, COLOR.WHITE)
        screen.blit(stats_text, (200, 300))

        pygame.draw.rect(screen, COLOR.RED, return_button)
        return_text = font_medium.render("Return to Title", True, COLOR.WHITE)
        screen.blit(return_text, (return_button.x + 20, return_button.y + 20))

        pygame.display.flip()