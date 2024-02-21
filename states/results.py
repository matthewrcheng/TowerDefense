import pygame
from utils import COLOR

def results_screen(screen, win, levels = 0, time = 0):
    
    # if win, display "Victory!" and show some stats like time elapsed, coins earned, xp gained, and (not implemented yet) what was unlocked

    # if not, display "Better luck next time..." with time elapsed, coins earned, and xp gained

    # coins are earned based on how much of the game was completed (how many levels cleared)
    # xp gained is a combination of levels completed and time elapsed, the less time elapsed, the more xp

    # for now, nothing gets unlocked and coins and xp are displayed, but they do not do anything
    # Set up fonts
    pygame.font.init()
    font_large = pygame.font.Font(None, 60)
    font_medium = pygame.font.Font(None, 40)

    # Calculate time elapsed (for demonstration purposes)
    if not time:
        time_elapsed = 120.5  # Replace this with the actual time elapsed in seconds
    
    # Calculate coins earned based on game completion
    if not levels:
        levels_cleared = 5  # Replace this with the actual number of levels cleared
    
    coins_earned = levels_cleared * 50  # Adjust the coefficient as needed
    
    # Calculate XP gained based on levels completed and time elapsed
    xp_gained = (levels_cleared * 100) - int(time_elapsed)  # Adjust coefficients as needed
    
    # Display victory screen
    if win:
        victory_text = font_large.render("Victory!", True, COLOR.GOLD)
        screen.blit(victory_text, (200, 100))

        # Display statistics
        stats_text = font_medium.render(f"Time Elapsed: {time_elapsed:.2f} seconds", True, COLOR.WHITE)
        screen.blit(stats_text, (200, 200))

        stats_text = font_medium.render(f"Coins Earned: {coins_earned}", True, COLOR.WHITE)
        screen.blit(stats_text, (200, 250))

        stats_text = font_medium.render(f"XP Gained: {xp_gained}", True, COLOR.WHITE)
        screen.blit(stats_text, (200, 300))

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

    pygame.display.flip()