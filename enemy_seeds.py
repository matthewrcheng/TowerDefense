from Enemy import *
from utils import COLOR

easy = {
    "name": "Easy",
    "color": COLOR.LIGHT_GREEN,
    "text_color": COLOR.WHITE,
    "final_level": 10,
    1: [(Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60)],
    2: [(Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60)],
    3: [(Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60)],
    4: [(Bandit, 60), (Bandit, 60), (Bandit, 60), (Bandit, 60)],
    5: [(Bandit, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Bandit, 60), (Bandit, 60), (Bandit, 60)],
    6: [(Thug, 60), (Thug, 60), (Thug, 60), (Thug, 60), (Thug, 60)],
    7: [(Thug, 60), (Thug, 60), (Thug, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Bandit, 60), (Bandit, 60), (Bandit, 60)],
    8: [(Brute, 30)],
    9: [(Thug, 60), (Thug, 60), (Brute, 30), (Bandit, 60)],
    10: [(Bandit, 60), (Bandit, 60), (Bandit, 60), (Bandit, 60), (Bandit, 60), (Brute, 30), (Brute, 60), (Brute, 60), (Brute, 60), (Brute, 60)],
}

normal = {
    "name": "Normal",
    "color": COLOR.GREEN,
    "text_color": COLOR.WHITE,
    "final_level": 25,
    1: [(Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60)],
    2: [(Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60)],
    3: [(Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60)],
    4: [(Bandit, 60), (Bandit, 60), (Bandit, 60), (Bandit, 60)],
    5: [(Bandit, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Bandit, 60), (Bandit, 60), (Bandit, 60)],
    6: [(Thug, 60), (Thug, 60), (Thug, 60), (Thug, 60), (Thug, 60)],
    7: [(Thug, 60), (Thug, 60), (Thug, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Bandit, 60), (Bandit, 60), (Bandit, 60)],
    8: [(Brute, 30)],
    9: [(Thug, 60), (Thug, 60), (Brute, 30), (Bandit, 60)],
    10: [(Bandit, 60), (Bandit, 60), (Bandit, 60), (Bandit, 60), (Bandit, 60), (PirateGunner, 30), (Pirate, 60), (Pirate, 60), (Pirate, 60), (Pirate, 60)],
    11: [(Brute, 30), (Brute, 30), (Brute, 30), (Brute, 30), (PirateGunner, 30), (Pirate, 15), (Pirate, 15), (Pirate, 15), (Pirate, 15)],
    12: [(Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (Bandit, 15), (PirateGunner, 30), (PirateGunner, 30)],
    13: [(Ghost, 20), (Ghost, 20), (Ghost, 20), (Ghost, 20), (Ghost, 20), (Ghost, 20)],
    14: [(Ghost, 20), (Ghost, 20), (Ghost, 20), (PirateGunner, 45), (Brute, 60), (Brute, 30), (Brute, 30), (Brute, 30), (Brute, 30), (Brute, 30), (Brute, 30), (Brute, 30), (Brute, 30), (Brute, 30), (Paratrooper, 90)],
    15: [(Ghost, 20), (Ghost, 20), (Ghost, 20), (Phantom, 10), (PirateGunner, 45), (PirateGunner, 45), (PirateGunner, 45)],
    16: [(PirateGunner, 30), (PirateGunner, 30), (PirateGunner, 30), (PirateGunner, 30), (PirateGunner, 30), (PirateGunner, 30), (PirateGunner, 30), (PirateMate, 60)],
    17: [(PirateMate, 30), (PirateMate, 30), (PirateMate, 30), (Phantom, 20), (Phantom, 20), (Phantom, 20), (Phantom, 20), (Juggernaut, 30)],
    18: [(Paratrooper, 10), (Paratrooper, 10), (Paratrooper, 10), (Paratrooper, 10), (Paratrooper, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Hooligan, 10), (Juggernaut, 30), (Juggernaut, 30), (Juggernaut, 30)],
    19: [(Marauder, 30), (Marauder, 30), (Marauder, 30), (Marauder, 30), (Marauder, 30), (PirateMate, 30), (PirateMate, 30), (PirateMate, 30), (PirateMate, 30), (PirateMate, 30), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10), (Phantom, 10)],
    20: [(Pirate, 30), (PirateGunner, 30), (PirateMate, 30), (PirateCaptain, 30), (PirateMate, 30), (PirateMate, 30), (PirateGunner, 30), (PirateGunner, 30), (PirateGunner, 30), (PirateGunner, 30), (Pirate, 30), (Pirate, 30), (Pirate, 30), (Pirate, 30), (Pirate, 30), (Pirate, 30), (Pirate, 30), (Pirate, 30)],
    21: [(PirateCaptain, 30), (PirateCaptain, 10), (PirateCaptain, 10), (Juggernaut, 30), (Phantom, 10), (Juggernaut, 10), (Phantom, 10), (Juggernaut, 10), (Phantom, 10), (Juggernaut, 10), (Phantom, 10), (Juggernaut, 10), (Phantom, 10), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5)],
    22: [(Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Marauder, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (Phantom, 5), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10)],
    23: [(Smuggler, 3), (Smuggler, 3), (Smuggler, 3), (Smuggler, 3), (Smuggler, 3), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10)],
    24: [(Raider, 5), (Raider, 5), (Raider, 5), (Raider, 5), (Raider, 5), (PirateCaptain, 10), (PirateCaptain, 10), (PirateCaptain, 10), (Smuggler, 3), (Smuggler, 3), (Smuggler, 3), (Smuggler, 3), (Smuggler, 3)],
    25: [(Pirate, 90), (PirateGunner, 30), (PirateMate, 30), (PirateCaptain, 30), (DreadPirate, 30)]
}

hard = {
    "name": "Hard",
    "color": COLOR.DARK_GREEN,
    "text_color": COLOR.WHITE,
    "final_level": 1,
    1: [(Pirate, 90), (PirateGunner, 30), (PirateMate, 30), (PirateCaptain, 30), (DreadPirate, 30)]
}

extreme = {
    "name": "Extreme",
    "color": COLOR.DARK_PURPLE,
    "text_color": COLOR.WHITE,
    "final_level": 1,
    1: [(Pirate, 90), (PirateGunner, 30), (PirateMate, 30), (PirateCaptain, 30), (DreadPirate, 30)]
}

impossible = {
    "name": "Impossible",
    "color": COLOR.BLACK,
    "text_color": COLOR.WHITE,
    "final_level": 1,
    1: [(Pirate, 90), (PirateGunner, 30), (PirateMate, 30), (PirateCaptain, 30), (DreadPirate, 30)]
}

hell = {
    "name": "Hell",
    "color": COLOR.DARK_RED,
    "text_color": COLOR.YELLOW,
    "final_level": 40,
    1: [(Undead, 100), (Undead, 30), (Undead, 30), (Undead, 30)],
    2: [(Undead, 100), (Undead, 30), (Undead, 30), (Undead, 30), (Undead, 30), (Undead, 30), (Undead, 30)],
    3: [(Demon, 100), (Demon, 50), (Demon, 50)],
    # fill in more levels as needed
    20: [(DemonPriest, 50)],
    25: [(Cerberus, 100)], 
    28: [(DemonPrince, 100)],
    30: [(Titan, 100)],
    39: [(Titan, 100), (Titan, 80), (Titan, 80), (Titan, 80)],
    40: [(Conquest, 100), (War, 100), (Famine, 100), (Death, 100), (Cerberus, 95), (Hades, 5)]
}

drowned = {
    "name": "Drowned",
    "color": COLOR.DARK_BLUE,
    "text_color": COLOR.TEAL,
    "final_level": 35,
    1: [(Drowned, 100), (Drowned, 30), (Drowned, 30), (Drowned, 30)],
    2: [(Drowned, 100), (Drowned, 30), (Drowned, 30), (Drowned, 30), (Drowned, 30), (Drowned, 30), (Drowned, 30)],
    3: [(Mermaid, 100)],
    10: [(DrownedGunner, 100)],
    13: [(Siren, 100)],
    15: [(HardHatDiver, 100)],
    20: [(DrownedMate, 100)],
    25: [(DrownedCaptain, 100)],
    30: [(AbyssalKing, 100)],
    35: [(MonsterOfTheDeep, 100)],
}

corrupted = {
    "name": "Corrupted",
    "color": COLOR.GOLD,
    "text_color": COLOR.LIGHT_PURPLE,
    "final_level": 1,
    1: [(TrojanHorse, 100)]
}

santas_workshop = {
    "name": "Santa's Workshop",
    "color": COLOR.LIGHT_GREEN,
    "text_color": COLOR.WHITE,
    "final_level": 1,
    1: [(Pirate, 100)]
}

haunted_mansion = {
    "name": "Haunted Mansion",
    "color": COLOR.DARK_GREEN,
    "text_color": COLOR.WHITE,
    "final_level": 1,
    1: [(Pirate, 100)]
}