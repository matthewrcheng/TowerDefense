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
    2: [(Undead, 100), (Undead, 30), (Undead, 30), (Undead, 30), (Undead, 30), (Undead, 30), (Undead, 30), (Undead, 30)],
    3: [(Undead, 100), (Undead, 30), (Undead, 20), (Undead, 30), (Undead, 20), (Undead, 30), (Undead, 20), (Undead, 30), (Undead, 20), (Undead, 30), (Undead, 20), (Undead, 30), (Undead, 20)],
    4: [(Undead, 80), (Undead, 20), (Demon, 100), (Undead, 20), (Undead, 20), (Demon, 50), (Demon, 50), (Demon, 50)],
    5: [(Demon, 100), (Undead, 20), (Undead, 20), (Demon, 50), (Undead, 20), (Undead, 20), (Demon, 50)],
    6: [(Demon, 100), (Demon, 50), (Demon, 50), (Demon, 20), (Demon, 20), (Demon, 20), (Demon, 5), (Demon, 5)],
    7: [(Demon, 80), (Demon, 40), (HellHound, 100), (Undead, 20), (Undead, 20), (HellHound, 20), (Demon , 5), (Demon , 5), (Demon , 5), (Demon , 5)],
    8: [(HellHound, 100), (HellHound, 40), (HellHound, 40), (HellHound, 60), (Demon, 20), (Demon, 20)],
    9: [(Imp, 10), (Imp, 30), (Imp, 30), (Demon, 40), (HellHound, 60), (Imp, 60), (Demon, 20), (Demon, 20), (Demon, 20), (Demon, 20), (Imp, 10)],
    10: [(Imp, 10), (Imp, 10), (Imp, 10), (HellHound, 60), (HellHound, 40), (HellHound, 20), (HellHound, 20), (Demon, 40), (Demon, 20), (Demon, 20), (Demon, 20), (Demon, 20), (Imp, 10), (Imp, 10), (Imp, 10)],
    11: [(FallenAngel, 100), (FallenAngel, 60), (FallenAngel, 60), (FallenAngel, 60), (FallenAngel, 60), (FallenAngel, 60)],
    12: [(BloodThrall, 100), (BloodThrall, 60), (BloodThrall, 60), (BloodThrall, 60), (BloodThrall, 40), (Imp, 5), (Imp, 5), (Imp, 5), (BloodThrall, 40), (HellKnight, 40)],
    13: [(FallenAngel, 100), (FallenAngel, 60), (FallenAngel, 60), (FallenAngel, 60), (FallenAngel, 40), (HellKnight, 40), (Imp, 5), (Imp, 5), (Imp, 5), (HellHound, 40)],
    14: [(Immortal, 100), (Immortal, 60), (Immortal, 60), (Immortal, 60), (Immortal, 60)],
    15: [(Immortal, 100), (BloodThrall, 60), (Immortal, 60), (BloodThrall, 60), (Immortal, 60), (HellboundCorpse, 40)],
    16: [(Nightmare, 100), (Nightmare, 60), (Nightmare, 60), (Nightmare, 60), (Nightmare, 60), (HellboundCorpse, 40), (HellboundCorpse, 40)],
    17: [(HellfireMage, 100), (Nightmare, 60), (Nightmare, 30), (Nightmare, 30), (Nightmare, 30), (Immortal, 60), (BloodThrall, 60), (FallenAngel, 30), (Immortal, 30), (FallenAngel, 30)],
    18: [(HellboundCorpse, 50), (HellboundCorpse, 50), (HellboundCorpse, 50), (HellfireMage, 60), (HellfireMage, 60), (HellfireMage, 60), (Nightmare, 60), (Immortal, 60), (BloodThrall, 60), (Immortal, 20), (Immortal, 20), (Immortal, 20)],
    19: [(HellKnight, 100), (HellKnight, 60), (BloodThrall, 30), (HellboundCorpse, 60), (HellfireMage, 60), (Nightmare, 60), (Immortal, 60), (FallenAngel, 30), (BloodThrall, 30), (FallenAngel, 10), (FallenAngel, 10), (FallenAngel, 10)],
    20: [(InfernalSoldier, 100), (InfernalSoldier, 60), (InfernalSoldier, 60), (InfernalSoldier, 60), (InfernalSoldier, 60)],
    21: [(HellBat, 100), (InfernalSoldier, 60), (HellKnight, 60), (HellboundCorpse, 60), (HellfireMage, 60)],
    22: [(BoneGiant, 100), (HellBat, 60), (InfernalSoldier, 60), (HellKnight, 60), (HellboundCorpse, 60)],
    23: [(ShadowDrifter, 100), (BoneGiant, 60), (HellBat, 60), (InfernalSoldier, 60), (HellKnight, 60)],
    24: [(DoomBringer, 100), (ShadowDrifter, 60), (BoneGiant, 60), (HellBat, 60), (InfernalSoldier, 60)],
    25: [(DemonPrince, 100), (DoomBringer, 60), (ShadowDrifter, 60), (BoneGiant, 60), (HellBat, 60)],
    26: [(DemonPrince, 60), (DoomBringer, 60), (ShadowDrifter, 60), (BoneGiant, 60), (Candlebearer, 100)],
    27: [(DemonPrince, 60), (DoomBringer, 60), (DemonPriest, 100), (ShadowDrifter, 60), (Candlebearer, 60)],
    28: [(InfernalLegionnaire, 100), (DemonPriest, 60), (Candlebearer, 60), (DemonPrince, 60), (DoomBringer, 60)],
    29: [(SinCollector, 100), (InfernalLegionnaire, 60), (DemonPriest, 60), (Candlebearer, 60), (DemonPrince, 60)],
    30: [(InfernalGuardian, 100), (SinCollector, 60), (InfernalLegionnaire, 60), (DemonPriest, 60), (Candlebearer, 60)],
    31: [(BoneColossus, 100), (InfernalGuardian, 60), (SinCollector, 60), (InfernalLegionnaire, 60), (DemonPriest, 60)],
    32: [(Revenant, 100), (BoneColossus, 60), (InfernalGuardian, 60), (SinCollector, 60), (InfernalLegionnaire, 60)],
    33: [(GraveTether, 100), (Revenant, 60), (BoneColossus, 60), (InfernalGuardian, 60), (SinCollector, 60)],
    34: [(SoulTether, 100), (GraveTether, 60), (Revenant, 60), (BoneColossus, 60), (InfernalGuardian, 60)],
    35: [(Cerberus, 100), (SoulTether, 60), (GraveTether, 60), (Revenant, 60), (BoneColossus, 60)],
    36: [(IronHellspawn, 100), (Cerberus, 60), (SoulTether, 60), (GraveTether, 60), (Revenant, 60)],
    37: [(Titan, 100), (IronHellspawn, 60), (Cerberus, 60), (SoulTether, 60), (GraveTether, 60)],
    38: [(CursedSoul, 100), (BoneColossus, 20), (Titan, 60), (BoneColossus, 20), (BoneColossus, 20), (IronHellspawn, 60), (BoneColossus, 20), (DemonPrince, 60), (SoulTether, 60), (BoneColossus, 20), (BoneColossus, 20), (BoneColossus, 10), (Candlebearer, 10)],
    39: [(FallenVanguard, 100), (IronHellspawn, 10), (IronHellspawn, 10), (Titan, 10), (IronHellspawn, 10), (IronHellspawn, 10), (Titan, 10), (IronHellspawn, 10), (IronHellspawn, 10), (Titan, 10), (IronHellspawn, 10), (IronHellspawn, 10), (Titan, 10), (IronHellspawn, 10), (IronHellspawn, 10), (CursedSoul, 10), (CursedSoul, 10), (CursedSoul, 10)],
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

def calculate_difficulty(enemy_seed):
    waves = enemy_seed.get("final_level", 0)
    difficulties = {}
    for level in range(1, waves + 1):
        enemies = enemy_seed.get(level, [])
        difficulty = 0
        for enemy_class in enemies:
            enemy, _ = enemy_class
            enemy_instance = enemy()
            difficulty += calculate_enemy_difficulty(enemy_instance)
        difficulties[level] = difficulty
    return difficulties
            
def get_all_enemy_difficulties(enemy_seed):
    waves = enemy_seed.get("final_level", 0)
    enemies = {}
    for level in range(1, waves + 1):
        enemy_list = enemy_seed.get(level, [])
        for enemy_class in enemy_list:
            enemy, _ = enemy_class
            enemy_instance = enemy()
            enemies[enemy_instance.name] = calculate_enemy_difficulty(enemy_instance)
    return enemies

def calculate_enemy_difficulty(enemy_instance):
    # air, metal, and invisible each double difficulty
    difficulty = enemy_instance.max_health / enemy_instance.speed_delay
    if enemy_instance.air_flag:
        difficulty *= 2
    if enemy_instance.metal_flag:
        difficulty *= 2
    if enemy_instance.invisible_flag:
        difficulty *= 2
    defense_multiplier = 1 / (1-enemy_instance.defense)
    difficulty *= defense_multiplier
    return difficulty

if __name__ == "__main__":
    print(calculate_difficulty(hell))
    print("-----")
    print(get_all_enemy_difficulties(hell))