import pygame
from utils import COLOR, GameState, Map
from Tower import Warrior, Archer, Deadeye, Berserker, Assassin, Gunslinger, Dragoon, Farm, Electrocutioner

# Constants for screen dimensions and fonts
fonts = pygame.font.Font(None, 36)
fontl = pygame.font.Font(None, 72)

def map_selection_screen(screen):

    # Button
    play_button = pygame.Rect(300, 150, 200, 100)
    field_button = pygame.Rect(300, 275, 200, 50)
    beach_button = pygame.Rect(300, 350, 200, 50)
    moon_button = pygame.Rect(300, 425, 200, 50)
    current_selection_button = pygame.Rect(300, 50, 350, 50) 
    quit_button = pygame.Rect(600, 500, 100, 50)

    map = Map.Field

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
        screen.blit(collection_text, (field_button.x + 66, field_button.y + 10))
        pygame.draw.rect(screen, COLOR.BLUE, beach_button)
        achievements_text = fonts.render("Beach", True, COLOR.TEAL)
        screen.blit(achievements_text, (beach_button.x + 60, beach_button.y + 10))
        pygame.draw.rect(screen, COLOR.FAINT, moon_button)
        achievements_text = fonts.render("Moon", True, COLOR.GRAY)
        screen.blit(achievements_text, (moon_button.x + 62, moon_button.y + 10))
        pygame.draw.rect(screen, map.secondary, current_selection_button)
        current_selection_text = fonts.render(f"Current Selection: {map.name}", True, map.primary)
        screen.blit(current_selection_text, (current_selection_button.x + 15, current_selection_button.y + 10))
        pygame.draw.rect(screen, COLOR.BLACK, quit_button) 
        quit_text = fonts.render("Quit", True, COLOR.WHITE)
        screen.blit(quit_text, (quit_button.x + 20, quit_button.y + 10))

        pygame.display.flip()

def tower_selection_screen(screen):

    # util buttons
    play_button = pygame.Rect(300, 150, 200, 100)
    quit_button = pygame.Rect(600, 500, 100, 50)
    current_selection_display = pygame.Rect(300, 50, 350, 50) 

    # tower buttons
    warrior_button = pygame.Rect(300, 275, 200, 50)
    archer_button = pygame.Rect(300, 350, 200, 50)
    deadeye_button = pygame.Rect(300, 425, 200, 50)
    berserker_button = pygame.Rect(300, 500, 200, 50)
    assassin_button = pygame.Rect(300, 575, 200, 50)
    gunslinger_button = pygame.Rect(300, 650, 200, 50)
    dragoon_button = pygame.Rect(300, 725, 200, 50)
    farm_button = pygame.Rect(300, 800, 200, 50)
    electro_button = pygame.Rect(300, 875, 200, 50)
    # add others as needed
    
    # tower selection
    towers = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    if len(towers) < 8:
                        # warn user that they need to select 8 towers
                        pass
                    else:
                        selection = {
                            "Tower1": towers[0],
                            "Tower2": towers[1],
                            "Tower3": towers[2],
                            "Tower4": towers[3],
                            "Tower5": towers[4],
                            "Tower6": towers[5],
                            "Tower7": towers[6],
                            "Tower8": towers[7]
                        }
                        return selection
                elif warrior_button.collidepoint(event.pos):
                    if len(towers) < 8:
                        if Warrior in towers:
                            towers.remove(Warrior)
                        else:
                            towers.append(Warrior)
                elif archer_button.collidepoint(event.pos):
                    if len(towers) < 8:
                        if Archer in towers:
                            towers.remove(Archer)
                        else:
                            towers.append(Archer)
                elif deadeye_button.collidepoint(event.pos):
                    if len(towers) < 8:
                        if Deadeye in towers:
                            towers.remove(Deadeye)
                        else:
                            towers.append(Deadeye)
                elif berserker_button.collidepoint(event.pos):
                    if len(towers) < 8:
                        if Berserker in towers:
                            towers.remove(Berserker)
                        else:
                            towers.append(Berserker)
                elif assassin_button.collidepoint(event.pos):
                    if len(towers) < 8:
                        if Assassin in towers:
                            towers.remove(Assassin)
                        else:
                            towers.append(Assassin)
                elif gunslinger_button.collidepoint(event.pos):
                    if len(towers) < 8:
                        if Gunslinger in towers:    
                            towers.remove(Gunslinger)
                        else:
                            towers.append(Gunslinger)
                elif dragoon_button.collidepoint(event.pos):
                    if len(towers) < 8:
                        if Dragoon in towers:
                            towers.remove(Dragoon)
                        else:
                            towers.append(Dragoon)
                elif farm_button.collidepoint(event.pos):
                    if len(towers) < 8:
                        if Farm in towers:
                            towers.remove(Farm)
                        else:
                            towers.append(Farm)
                elif electro_button.collidepoint(event.pos):
                    if len(towers) < 8:
                        if Electrocutioner in towers:    
                            towers.remove(Electrocutioner)
                        else:    
                            towers.append(Electrocutioner)
                elif quit_button.collidepoint(event.pos):  # Handle the "Quit" button
                    return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
        screen.fill(COLOR.WHITE)

        # Display username at the top of the screen
        title_text = fonts.render(f"SELECT TOWERS", True, COLOR.BLACK)
        screen.blit(title_text, (50, 50))

        # Draw the "Play" button
        pygame.draw.rect(screen, COLOR.BLACK, play_button)
        play_text = fontl.render("Play", True, COLOR.WHITE)
        screen.blit(play_text, (play_button.x + 48, play_button.y + 25))

        # Draw the "Quit" button
        pygame.draw.rect(screen, COLOR.BLACK, quit_button) 
        quit_text = fonts.render("Quit", True, COLOR.WHITE)
        screen.blit(quit_text, (quit_button.x + 20, quit_button.y + 10))

        # Draw the tower buttons
        pygame.draw.rect(screen, COLOR.BLACK, warrior_button)
        warrior_text = fonts.render("Warrior", True, COLOR.WHITE)
        screen.blit(warrior_text, (warrior_button.x + 20, warrior_button.y + 10))

        pygame.draw.rect(screen, COLOR.BLACK, archer_button)
        archer_text = fonts.render("Archer", True, COLOR.WHITE)
        screen.blit(archer_text, (archer_button.x + 20, archer_button.y + 10))

        pygame.draw.rect(screen, COLOR.BLACK, deadeye_button)
        deadeye_text = fonts.render("Deadeye", True, COLOR.WHITE)
        screen.blit(deadeye_text, (deadeye_button.x + 20, deadeye_button.y + 10))

        pygame.draw.rect(screen, COLOR.BLACK, berserker_button)
        berserker_text = fonts.render("Berserker", True, COLOR.WHITE)
        screen.blit(berserker_text, (berserker_button.x + 20, berserker_button.y + 10))

        pygame.draw.rect(screen, COLOR.BLACK, assassin_button)
        assassin_text = fonts.render("Assassin", True, COLOR.WHITE)
        screen.blit(assassin_text, (assassin_button.x + 20, assassin_button.y + 10))

        pygame.draw.rect(screen, COLOR.BLACK, gunslinger_button)
        gunslinger_text = fonts.render("Gunslinger", True, COLOR.WHITE)
        screen.blit(gunslinger_text, (gunslinger_button.x + 20, gunslinger_button.y + 10))

        pygame.draw.rect(screen, COLOR.BLACK, dragoon_button)
        dragoon_text = fonts.render("Dragoon", True, COLOR.WHITE)
        screen.blit(dragoon_text, (dragoon_button.x + 20, dragoon_button.y + 10))

        pygame.draw.rect(screen, COLOR.BLACK, farm_button)
        farm_text = fonts.render("Farm", True, COLOR.WHITE)
        screen.blit(farm_text, (farm_button.x + 20, farm_button.y + 10))

        pygame.draw.rect(screen, COLOR.BLACK, electro_button)
        electro_text = fonts.render("Electrocutioner", True, COLOR.WHITE)
        screen.blit(electro_text, (electro_button.x + 20, electro_button.y + 10))

        pygame.display.flip()

