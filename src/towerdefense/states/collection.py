import pygame
from ..util.utils import COLOR, GameState
from ..entities.Tower import get_all_towers

def load_collection() -> list:
    collection = []
    for tower in get_all_towers():
        tower = tower()
        item = (tower.name, tower.color)
        collection.append(item)
    return collection

def collection_screen(screen):

    # Constants for screen dimensions and fonts
    fonts = pygame.font.Font(None, 36)
    fontl = pygame.font.Font(None, 72)

    # Button
    quit_button = pygame.Rect(screen.get_width()-200, 0, 200, 50)

    # Collection
    COLL_ITEM_WIDTH = 150
    COLL_ITEM_HEIGHT = 150
    COLL_START_X = 25
    COLL_START_Y = 115
    COLL_NUM_COL = 6

    collection = load_collection()

    scroll = 0

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
            if event.type == pygame.MOUSEWHEEL:
                scroll = scroll - event.y
                rows = int(len(collection) / COLL_NUM_COL)+1
                if scroll < 0:
                    scroll = 0
                elif scroll >= rows-2:
                    scroll = rows-3
                print(rows, scroll)
        screen.fill(COLOR.WHITE)

        # Display username at the top of the screen
        title_text = fontl.render(f"COLLECTION", True, COLOR.BLACK)
        screen.blit(title_text, (50, 50))

        # Draw the "Play" button
        pygame.draw.rect(screen, COLOR.BLACK, quit_button) 
        quit_text = fonts.render("Main Menu", True, COLOR.WHITE)
        screen.blit(quit_text, (quit_button.x + 40, quit_button.y + 10))

        # Draw collection items
        for i in range(18):
            row = int(i / COLL_NUM_COL)
            col = i % COLL_NUM_COL
            try:
                item = collection[i+(scroll*6)]
            except:
                item = ["", COLOR.WHITE]
            pygame.draw.rect(screen, item[1], pygame.Rect(COLL_START_X+(COLL_ITEM_WIDTH*col), COLL_START_Y+(COLL_ITEM_HEIGHT*row), COLL_ITEM_WIDTH, COLL_ITEM_HEIGHT))

        pygame.display.flip()