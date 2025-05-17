import pygame
from utils import COLOR, GameState, Map, draw_rect_alpha, GameState
from Tower import *
from enemy_seeds import easy, normal, hard, extreme, impossible, hell, drowned, corrupted

def map_selection_screen(screen):
    # Constants for screen dimensions and fonts
    fonts = pygame.font.Font(None, 36)

    # Map buttons
    # column 1
    field_button = pygame.Rect(50, 150, 200, 50)
    beach_button = pygame.Rect(50, 225, 200, 50)
    moon_button = pygame.Rect(50, 300, 200, 50)

    # column 2
    desert_button = pygame.Rect(300, 150, 200, 50)
    arctic_button = pygame.Rect(300, 225, 200, 50)
    jungle_button = pygame.Rect(300, 300, 200, 50)

    # column 3
    volcano_button = pygame.Rect(550, 150, 200, 50)

    # util buttons 
    current_selection_button = pygame.Rect(300, 50, 350, 50) 
    next_button = pygame.Rect(650, 500, 100, 50)
    back_button = pygame.Rect(50, 500, 100, 50)
    quit_button = pygame.Rect(800, 500, 100, 50)

    # util classes
    field = Map.Field()
    beach = Map.Beach()
    moon = Map.Moon()
    desert = Map.Desert()
    arctic = Map.Arctic()
    jungle = Map.Jungle()
    volcano = Map.Volcano()

    current_map = Map.Field

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, GameState.QUIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button.collidepoint(event.pos):
                    # Transition to the WORLDS screen when "Play" is clicked
                    return current_map, GameState.TOWER_SELECTION
                elif field_button.collidepoint(event.pos):
                    current_map = Map.Field
                elif beach_button.collidepoint(event.pos):
                    current_map = Map.Beach
                elif moon_button.collidepoint(event.pos):
                    current_map = Map.Moon
                elif desert_button.collidepoint(event.pos):
                    current_map = Map.Desert
                elif arctic_button.collidepoint(event.pos):
                    current_map = Map.Arctic
                elif jungle_button.collidepoint(event.pos):
                    current_map = Map.Jungle
                elif volcano_button.collidepoint(event.pos):
                    current_map = Map.Volcano
                elif quit_button.collidepoint(event.pos):  # Handle the "Quit" button
                    return None, GameState.MENU
                elif back_button.collidepoint(event.pos):
                    return None, GameState.MENU
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, GameState.MENU
        screen.fill(COLOR.WHITE)

        # Display username at the top of the screen
        title_text = fonts.render(f"SELECT MAP", True, COLOR.BLACK)
        screen.blit(title_text, (50, 50))

        # Draw the "Next" button
        pygame.draw.rect(screen, COLOR.BLACK, next_button)
        play_text = fonts.render("Next", True, COLOR.WHITE)
        screen.blit(play_text, (next_button.x + 20, next_button.y + 10))

        # Draw the "Back" button
        pygame.draw.rect(screen, COLOR.BLACK, back_button)
        play_text = fonts.render("Back", True, COLOR.WHITE)
        screen.blit(play_text, (back_button.x + 20, back_button.y + 10))

        # Current selection
        pygame.draw.rect(screen, current_map.secondary, current_selection_button)
        current_selection_text = fonts.render(f"Current Selection: {current_map.name}", True, current_map.primary)
        screen.blit(current_selection_text, (current_selection_button.x + 15, current_selection_button.y + 10))

        # Draw the "Quit" button
        pygame.draw.rect(screen, COLOR.BLACK, quit_button) 
        quit_text = fonts.render("Exit", True, COLOR.WHITE)
        screen.blit(quit_text, (quit_button.x + 20, quit_button.y + 10))

        # Draw the map selection buttons
        pygame.draw.rect(screen, field.secondary, field_button)
        collection_text = fonts.render(field.name, True, field.primary)
        screen.blit(collection_text, (field_button.x + 66, field_button.y + 10))

        pygame.draw.rect(screen, beach.secondary, beach_button)
        collection_text = fonts.render(beach.name, True, beach.primary)
        screen.blit(collection_text, (beach_button.x + 66, beach_button.y + 10))

        pygame.draw.rect(screen, moon.secondary, moon_button)
        collection_text = fonts.render(moon.name, True, moon.primary)
        screen.blit(collection_text, (moon_button.x + 66, moon_button.y + 10))

        pygame.draw.rect(screen, desert.secondary, desert_button)
        collection_text = fonts.render(desert.name, True, desert.primary)
        screen.blit(collection_text, (desert_button.x + 66, desert_button.y + 10))

        pygame.draw.rect(screen, arctic.secondary, arctic_button)
        collection_text = fonts.render(arctic.name, True, arctic.primary)
        screen.blit(collection_text, (arctic_button.x + 66, arctic_button.y + 10))

        pygame.draw.rect(screen, jungle.secondary, jungle_button)
        collection_text = fonts.render(jungle.name, True, jungle.primary)
        screen.blit(collection_text, (jungle_button.x + 66, jungle_button.y + 10))

        pygame.draw.rect(screen, volcano.secondary, volcano_button)
        collection_text = fonts.render(volcano.name, True, volcano.primary)
        screen.blit(collection_text, (volcano_button.x + 66, volcano_button.y + 10))

        pygame.display.flip()

def tower_selection_screen(screen):
    # Constants for screen dimensions and fonts
    fonts = pygame.font.Font(None, 36)

    # util buttons
    play_button = pygame.Rect(650, 500, 100, 50)
    quit_button = pygame.Rect(800, 500, 100, 50)
    back_button = pygame.Rect(50, 500, 100, 50)

    # temporary select default towers button for quick testing
    default_button = pygame.Rect(200, 500, 100, 50)

    # util classes
    selection_blocks = [pygame.Rect(300+50*i, 25, 50, 50) for i in range(8)] 

    # tower buttons
    # column 1
    warrior_button = pygame.Rect(50, 100, 250, 50)
    archer_button = pygame.Rect(50, 175, 250, 50)
    deadeye_button = pygame.Rect(50, 250, 250, 50)
    berserker_button = pygame.Rect(50, 325, 250, 50)
    assassin_button = pygame.Rect(50, 400, 250, 50)
    # column 2
    gunslinger_button = pygame.Rect(350, 100, 250, 50)
    bard_button = pygame.Rect(350, 175, 250, 50)
    mage_button = pygame.Rect(350, 250, 250, 50)
    artisan_button = pygame.Rect(350, 325, 250, 50)
    alchemist_button = pygame.Rect(350, 400, 250, 50)
    # column 3
    dragoon_button = pygame.Rect(650, 100, 250, 50)
    farm_button = pygame.Rect(650, 175, 250, 50)
    electro_button = pygame.Rect(650, 250, 250, 50)
    general_button = pygame.Rect(650, 325, 250, 50)
    # add others as needed

    # tower classes
    warrior = Warrior()
    archer = Archer()
    deadeye = Deadeye()
    berserker = Berserker()
    assassin = Assassin()
    gunslinger = Gunslinger()
    dragoon = Dragoon()
    farm = Farm()
    electro = Electrocutioner()
    general = General()
    bard = Bard()
    mage = Mage()
    artisan = Artisan()
    alchemist = Alchemist()
    # add others as needed
    
    # tower selection
    towers = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, GameState.QUIT
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
                        return selection, GameState.DIFFICULTY_SELECTION
                elif warrior_button.collidepoint(event.pos):
                    if Warrior in towers:
                        towers.remove(Warrior)
                        # unhighlight warrior button
                        pass
                    elif len(towers) < 8:
                        towers.append(Warrior)
                        # highlight warrior button
                        pass
                elif archer_button.collidepoint(event.pos):
                    if Archer in towers:
                        towers.remove(Archer)
                        # unhighlight archer button
                        pass
                    elif len(towers) < 8:
                        towers.append(Archer)
                        # highlight archer button
                        pass
                elif deadeye_button.collidepoint(event.pos):    
                    if Deadeye in towers:
                        towers.remove(Deadeye)
                        # unhighlight deadeye button
                        pass
                    elif len(towers) < 8:
                        towers.append(Deadeye)
                        # highlight deadeye button
                        pass
                elif berserker_button.collidepoint(event.pos):
                    if Berserker in towers: 
                        towers.remove(Berserker)
                        # unhighlight berserker button
                        pass
                    elif len(towers) < 8:
                        towers.append(Berserker)
                        # highlight berserker button
                        pass
                elif assassin_button.collidepoint(event.pos):
                    if Assassin in towers:
                        towers.remove(Assassin)
                        # unhighlight assassin button
                        pass
                    elif len(towers) < 8:
                        towers.append(Assassin)
                        # highlight assassin button
                        pass
                elif gunslinger_button.collidepoint(event.pos):
                    if Gunslinger in towers:
                        towers.remove(Gunslinger)
                        # unhighlight gunslinger button
                        pass
                    elif len(towers) < 8:
                        towers.append(Gunslinger)
                        # highlight gunslinger button
                        pass
                elif dragoon_button.collidepoint(event.pos):
                    if Dragoon in towers:
                        towers.remove(Dragoon)
                        # unhighlight dragoon button
                        pass
                    elif len(towers) < 8:
                        towers.append(Dragoon)
                        # highlight dragoon button
                        pass
                elif farm_button.collidepoint(event.pos):
                    if Farm in towers:
                        towers.remove(Farm)
                        # unhighlight farm button
                        pass
                    elif len(towers) < 8:
                        towers.append(Farm)
                        # highlight farm button
                        pass
                elif electro_button.collidepoint(event.pos):
                    if Electrocutioner in towers:
                        towers.remove(Electrocutioner)
                        # unhighlight electro button
                        pass    
                    elif len(towers) < 8:
                        towers.append(Electrocutioner)
                        # highlight electro button
                        pass
                elif general_button.collidepoint(event.pos):
                    if General in towers:
                        towers.remove(General)
                        # unhighlight general button
                        pass
                    elif len(towers) < 8:
                        towers.append(General)
                        # highlight general button
                        pass
                elif bard_button.collidepoint(event.pos):
                    if Bard in towers:
                        towers.remove(Bard)
                        # unhighlight bard button
                        pass
                    elif len(towers) < 8:
                        towers.append(Bard)
                        # highlight bard button
                        pass
                elif mage_button.collidepoint(event.pos):
                    if Mage in towers:
                        towers.remove(Mage)
                        # unhighlight mage button
                        pass
                    elif len(towers) < 8:
                        towers.append(Mage)
                        # highlight mage button
                        pass
                elif artisan_button.collidepoint(event.pos):
                    if Artisan in towers:
                        towers.remove(Artisan)
                        # unhighlight artisan button
                        pass
                    elif len(towers) < 8:
                        towers.append(Artisan)
                        # highlight artisan button
                        pass
                elif alchemist_button.collidepoint(event.pos):
                    if Alchemist in towers:
                        towers.remove(Alchemist)
                        # unhighlight alchemist button
                        pass
                    elif len(towers) < 8:
                        towers.append(Alchemist)
                        # highlight alchemist button
                        pass
                elif default_button.collidepoint(event.pos):  # Handle the "Default" button
                    towers = [Warrior, Archer, Deadeye, Berserker, Assassin, Gunslinger, Dragoon, Farm]
                elif quit_button.collidepoint(event.pos):  # Handle the "Quit" button
                    return None, GameState.MENU
                elif back_button.collidepoint(event.pos):  # Handle the "Back" button
                    return None, GameState.MAP_SELECTION
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, GameState.MENU
        screen.fill(COLOR.WHITE)

        # selected towers
        title_text = fonts.render(f"SELECT TOWERS", True, COLOR.BLACK)
        screen.blit(title_text, (50, 50))
        for i,tower in enumerate(towers):
            draw_rect_alpha(screen, tower().color, selection_blocks[i])

        # Draw the "Play" button
        pygame.draw.rect(screen, COLOR.BLACK, play_button)
        play_text = fonts.render("Play", True, COLOR.WHITE)
        screen.blit(play_text, (play_button.x + 20, play_button.y + 10))

        # Draw the "Quit" button
        pygame.draw.rect(screen, COLOR.BLACK, quit_button) 
        quit_text = fonts.render("Exit", True, COLOR.WHITE)
        screen.blit(quit_text, (quit_button.x + 20, quit_button.y + 10))

        # Draw the "Back" button
        pygame.draw.rect(screen, COLOR.BLACK, back_button)
        back_text = fonts.render("Back", True, COLOR.WHITE)
        screen.blit(back_text, (back_button.x + 20, back_button.y + 10))

        # default button
        pygame.draw.rect(screen, COLOR.BLACK, default_button)
        default_text = fonts.render("Default", True, COLOR.WHITE)
        screen.blit(default_text, (default_button.x + 20, default_button.y + 10))

        # Draw the tower buttons
        pygame.draw.rect(screen, warrior.color if Warrior in towers else COLOR.LIGHT_GRAY, warrior_button)
        warrior_text = fonts.render(warrior.name, True, warrior.text_color if Warrior in towers else COLOR.DARK_GRAY)
        screen.blit(warrior_text, (warrior_button.x + 20, warrior_button.y + 10))

        pygame.draw.rect(screen, archer.color if Archer in towers else COLOR.LIGHT_GRAY, archer_button)
        archer_text = fonts.render(archer.name, True, archer.text_color if Archer in towers else COLOR.DARK_GRAY)
        screen.blit(archer_text, (archer_button.x + 20, archer_button.y + 10))

        pygame.draw.rect(screen, deadeye.color if Deadeye in towers else COLOR.LIGHT_GRAY, deadeye_button)
        deadeye_text = fonts.render(deadeye.name, True, deadeye.text_color if Deadeye in towers else COLOR.DARK_GRAY)
        screen.blit(deadeye_text, (deadeye_button.x + 20, deadeye_button.y + 10))

        pygame.draw.rect(screen, berserker.color if Berserker in towers else COLOR.LIGHT_GRAY, berserker_button)
        berserker_text = fonts.render(berserker.name, True, berserker.text_color if Berserker in towers else COLOR.DARK_GRAY)
        screen.blit(berserker_text, (berserker_button.x + 20, berserker_button.y + 10))

        pygame.draw.rect(screen, assassin.color if Assassin in towers else COLOR.LIGHT_GRAY, assassin_button)
        assassin_text = fonts.render(assassin.name, True, assassin.text_color if Assassin in towers else COLOR.DARK_GRAY)
        screen.blit(assassin_text, (assassin_button.x + 20, assassin_button.y + 10))

        pygame.draw.rect(screen, gunslinger.color if Gunslinger in towers else COLOR.LIGHT_GRAY, gunslinger_button)
        gunslinger_text = fonts.render(gunslinger.name, True, gunslinger.text_color if Gunslinger in towers else COLOR.DARK_GRAY)
        screen.blit(gunslinger_text, (gunslinger_button.x + 20, gunslinger_button.y + 10))

        pygame.draw.rect(screen, dragoon.color if Dragoon in towers else COLOR.LIGHT_GRAY, dragoon_button)
        dragoon_text = fonts.render(dragoon.name, True, dragoon.text_color if Dragoon in towers else COLOR.DARK_GRAY)
        screen.blit(dragoon_text, (dragoon_button.x + 20, dragoon_button.y + 10))

        pygame.draw.rect(screen, farm.color if Farm in towers else COLOR.LIGHT_GRAY, farm_button)
        farm_text = fonts.render(farm.name, True, farm.text_color if Farm in towers else COLOR.DARK_GRAY)
        screen.blit(farm_text, (farm_button.x + 20, farm_button.y + 10))

        pygame.draw.rect(screen, electro.color if Electrocutioner in towers else COLOR.LIGHT_GRAY, electro_button)
        electro_text = fonts.render(electro.name, True, electro.text_color if Electrocutioner in towers else COLOR.DARK_GRAY)
        screen.blit(electro_text, (electro_button.x + 20, electro_button.y + 10))

        pygame.draw.rect(screen, general.color if General in towers else COLOR.LIGHT_GRAY, general_button)
        general_text = fonts.render(general.name, True, general.text_color if General in towers else COLOR.DARK_GRAY)
        screen.blit(general_text, (general_button.x + 20, general_button.y + 10))

        pygame.draw.rect(screen, bard.color if Bard in towers else COLOR.LIGHT_GRAY, bard_button)
        bard_text = fonts.render(bard.name, True, bard.text_color if Bard in towers else COLOR.DARK_GRAY)
        screen.blit(bard_text, (bard_button.x + 20, bard_button.y + 10))
        
        pygame.draw.rect(screen, mage.color if Mage in towers else COLOR.LIGHT_GRAY, mage_button)
        mage_text = fonts.render(mage.name, True, mage.text_color if Mage in towers else COLOR.DARK_GRAY)
        screen.blit(mage_text, (mage_button.x + 20, mage_button.y + 10))

        pygame.draw.rect(screen, artisan.color if Artisan in towers else COLOR.LIGHT_GRAY, artisan_button)
        artisan_text = fonts.render(artisan.name, True, artisan.text_color if Artisan in towers else COLOR.DARK_GRAY)
        screen.blit(artisan_text, (artisan_button.x + 20, artisan_button.y + 10))

        pygame.draw.rect(screen, alchemist.color if Alchemist in towers else COLOR.LIGHT_GRAY, alchemist_button)
        alchemist_text = fonts.render(alchemist.name, True, alchemist.text_color if Alchemist in towers else COLOR.DARK_GRAY)
        screen.blit(alchemist_text, (alchemist_button.x + 20, alchemist_button.y + 10))

        pygame.display.flip()

def difficulty_selection_screen(screen):

    # Constants for screen dimensions and fonts
    fonts = pygame.font.Font(None, 36)

    # util buttons
    play_button = pygame.Rect(650, 500, 100, 50)
    quit_button = pygame.Rect(800, 500, 100, 50)
    back_button = pygame.Rect(50, 500, 100, 50)

    # util classes
    selection_block = pygame.Rect(50, 50, 200, 50)  

    # difficulty buttons
    # standard difficulties
    easy_button = pygame.Rect(50, 150, 200, 50)
    normal_button = pygame.Rect(50, 225, 200, 50)
    hard_button = pygame.Rect(50, 300, 200, 50)
    extreme_button = pygame.Rect(50, 375, 200, 50)
    impossible_button = pygame.Rect(50, 455, 200, 50)

    # special difficulties
    hell_button = pygame.Rect(300, 150, 200, 50)
    drowned_button = pygame.Rect(300, 225, 200, 50)
    corrupted_button = pygame.Rect(300, 300, 200, 50)

    # selected difficulty seed
    selection = easy

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, GameState.QUIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    if selection is None:
                        # warn user that they need to select a difficulty
                        pass
                    else:
                        return selection,GameState.GAME
                elif easy_button.collidepoint(event.pos):
                    selection = easy
                elif normal_button.collidepoint(event.pos):
                    selection = normal
                elif hard_button.collidepoint(event.pos):
                    selection = hard
                elif extreme_button.collidepoint(event.pos):
                    selection = extreme
                elif impossible_button.collidepoint(event.pos):
                    selection = impossible
                elif hell_button.collidepoint(event.pos):
                    selection = hell
                elif drowned_button.collidepoint(event.pos):
                    selection = drowned
                elif corrupted_button.collidepoint(event.pos):
                    selection = corrupted
                elif quit_button.collidepoint(event.pos):  # Handle the "Quit" button
                    return None,GameState.MENU
                elif back_button.collidepoint(event.pos):  # Handle the "Back" button
                    return None,GameState.TOWER_SELECTION
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None,GameState.MENU
        screen.fill(COLOR.WHITE)

        # selected difficulty
        pygame.draw.rect(screen, selection.get("color", COLOR.DARK_GRAY), selection_block)
        selection_text = fonts.render(selection.get("name", "Select a difficulty"), True, selection.get("text_color", COLOR.LIGHT_GRAY))
        screen.blit(selection_text, (selection_block.x + 20, selection_block.y + 10))

        # difficulty buttonss
        pygame.draw.rect(screen, COLOR.LIGHT_GRAY, easy_button)
        easy_text = fonts.render(easy.get("name"), True, COLOR.DARK_GRAY)
        screen.blit(easy_text, (easy_button.x + 20, easy_button.y + 10))

        pygame.draw.rect(screen, COLOR.LIGHT_GRAY, normal_button)
        normal_text = fonts.render(normal.get("name"), True, COLOR.DARK_GRAY)
        screen.blit(normal_text, (normal_button.x + 20, normal_button.y + 10))

        pygame.draw.rect(screen, COLOR.LIGHT_GRAY, hard_button)
        hard_text = fonts.render(hard.get("name"), True, COLOR.DARK_GRAY)
        screen.blit(hard_text, (hard_button.x + 20, hard_button.y + 10))

        pygame.draw.rect(screen, COLOR.LIGHT_GRAY, extreme_button)
        extreme_text = fonts.render(extreme.get("name"), True, COLOR.DARK_GRAY)
        screen.blit(extreme_text, (extreme_button.x + 20, extreme_button.y + 10))

        pygame.draw.rect(screen, COLOR.LIGHT_GRAY, impossible_button)
        impossible_text = fonts.render(impossible.get("name"), True, COLOR.DARK_GRAY)
        screen.blit(impossible_text, (impossible_button.x + 20, impossible_button.y + 10))

        pygame.draw.rect(screen, COLOR.LIGHT_GRAY, hell_button)
        hell_text = fonts.render(hell.get("name"), True, COLOR.DARK_GRAY)
        screen.blit(hell_text, (hell_button.x + 20, hell_button.y + 10))    

        pygame.draw.rect(screen, COLOR.LIGHT_GRAY, drowned_button)
        drowned_text = fonts.render(drowned.get("name"), True, COLOR.DARK_GRAY)
        screen.blit(drowned_text, (drowned_button.x + 20, drowned_button.y + 10))

        pygame.draw.rect(screen, COLOR.LIGHT_GRAY, corrupted_button)
        corrupted_text = fonts.render(corrupted.get("name"), True, COLOR.DARK_GRAY)        
        screen.blit(corrupted_text, (corrupted_button.x + 20, corrupted_button.y + 10))

        # util buttons
        pygame.draw.rect(screen, COLOR.LIGHT_GRAY, play_button)
        play_text = fonts.render("Play", True, COLOR.DARK_GRAY)
        screen.blit(play_text, (play_button.x + 20, play_button.y + 10))

        pygame.draw.rect(screen, COLOR.LIGHT_GRAY, quit_button)
        quit_text = fonts.render("Exit", True, COLOR.DARK_GRAY)
        screen.blit(quit_text, (quit_button.x + 20, quit_button.y + 10))        

        pygame.draw.rect(screen, COLOR.LIGHT_GRAY, back_button)
        back_text = fonts.render("Back", True, COLOR.DARK_GRAY)
        screen.blit(back_text, (back_button.x + 20, back_button.y + 10))

        pygame.display.flip()